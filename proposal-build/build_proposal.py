"""Build the proposal .docx from the department template and proposal_content.md.

Usage: python build_proposal.py <template.docx> <figures_dir> <out.docx>
"""
import copy
import re
import sys
from pathlib import Path

import docx
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

TEMPLATE, FIGS, OUT = sys.argv[1], Path(sys.argv[2]), sys.argv[3]
HERE = Path(__file__).parent

TITLE = ("DESIGN AND EVALUATION OF A HYBRID PROMPT-AWARE, MULTI-OBJECTIVE LARGE LANGUAGE "
         "MODEL ROUTING SYSTEM WITH AUTOMATIC FALLBACK")
ID = "[STUDENT ID]"
MEMBERS = ["TERSEER SOLOMON TERZUNGWE-TEMBE", "SODIQ ABDULWARIS", "[FULL NAME: MARYAM]",
           "[FULL NAME: WAHIDA]", "[FULL NAME: KABIRU]", "[FULL NAME: ADRIEL]"]
SUPERVISOR = "[SUPERVISOR'S FULL NAME]"
MONTH = "[MONTH] 2026"
SESSION = "2026/2027"

ABSTRACT = (
    "Applications that use large language models usually send every request to a single model. "
    "This wastes money on requests a cheaper model could answer, and choosing a weaker model instead "
    "loses quality on hard requests. Research routers predict which model should answer each request, "
    "but most choose between two models, optimise only average cost and quality, and are rarely compared "
    "with simple alternatives under the same conditions. Commercial gateways offer failover but publish no "
    "evaluation of their routing decisions. This project aims to design, implement and evaluate a hybrid "
    "prompt-aware routing system that selects, for each request, a model from a mixed pool of local and "
    "hosted models under quality, cost and latency constraints, with automatic fallback when a provider "
    "fails. The study follows Design Science Research, with development in six two-week Scrum sprints. "
    "The router will be built in Python with FastAPI behind one OpenAI-compatible endpoint. It will predict "
    "each model's quality on a prompt by combining a lightweight task classifier with embedding-based "
    "retrieval of scored past prompts, then select the cheapest model whose predicted quality meets a "
    "threshold within the request's cost cap and deadline. A reliability controller with circuit breakers "
    "and bounded retries will handle provider failures. The router will be trained and evaluated offline on "
    "stored, scored outputs from a public routing benchmark, timed on a small capped live pilot, and tested "
    "under injected failures. It will be compared with fixed-model, cheapest-eligible, rule-based and "
    "single-component baselines using paired statistical tests and ablations. Expected outputs are an "
    "open-source routing gateway, a reusable evaluation harness and an evidence-based answer to whether the "
    "hybrid approach lowers cost at acceptable quality compared with simpler routing. A finding that simpler "
    "methods perform as well will also be reported, since it would guide developers choosing a routing method."
)
KEYWORDS = ("Keywords: circuit breaker; cost-aware routing; design science research; "
            "large language models; model selection")

CONTRIB = [
    ("Group leader; routing algorithm and machine learning developer",
     "Suitability predictor and selection policy (3.6.5, 3.7); sprint coordination; supervisor liaison"),
    ("System architect; model integration, API and database developer",
     "Architecture (3.6.1); provider adapters and reliability controller; database design (3.6.4)"),
    ("Backend developer; testing and evaluation developer",
     "Gateway backend; replay and fault-injection harness; evaluation plan (3.9)"),
    ("System architect; documentation lead; testing and evaluation",
     "Requirements (3.2, 3.5); Chapter Two coordination and references; test plan"),
    ("Frontend and backend developer; documentation",
     "Administrator dashboard (3.6.6); requirements extraction; report assembly"),
    ("[Role to be agreed]", "[To be agreed]"),
]
GENAI = [
    ("Claude (Anthropic), Claude Opus 5.5 in Claude Code, November 2026",
     "Drafted the proposal text from the team's research notes, design decisions and literature records; "
     "drew Figures 2.1 and 3.1 to 3.6 with Python scripts; formatted the document in the department template",
     "Front matter; Chapters One to Three",
     "[To be completed by the team: each section read and edited by its owner; every citation, number and figure "
     "checked against the original source]"),
    ("AI-assisted literature summaries (earlier sessions; tool and version to be confirmed)",
     "Reading notes for the 90 studies in the review register",
     "Chapter Two",
     "Summaries not treated as reading; key studies to be read in full and every reported figure checked"),
]
ABBREV = [("API", "Application Programming Interface"), ("AUROC", "Area Under the Receiver Operating Characteristic curve"),
          ("DSR", "Design Science Research"), ("ECE", "Expected Calibration Error"),
          ("ERD", "Entity Relationship Diagram"), ("FR", "Functional Requirement"),
          ("GPU", "Graphics Processing Unit"), ("HTTP", "Hypertext Transfer Protocol"),
          ("k-NN", "k-Nearest Neighbours"), ("LLM", "Large Language Model"),
          ("MoSCoW", "Must, Should, Could, Won't"), ("NDPA", "Nigeria Data Protection Act"),
          ("NFR", "Non-Functional Requirement"), ("p95", "95th percentile"), ("RQ", "Research Question"),
          ("SLO", "Service-Level Objective"), ("TLS", "Transport Layer Security"),
          ("TTFT", "Time To First Token"), ("UML", "Unified Modeling Language"),
          ("VRAM", "Video Random-Access Memory")]

doc = docx.Document(TEMPLATE)
P = doc.paragraphs  # snapshot of front-matter paragraphs by template index


# ---------- helpers ----------
def clean_rpr(rpr):
    if rpr is None:
        return None
    rpr = copy.deepcopy(rpr)
    for tag in ("w:color", "w:i", "w:iCs", "w:highlight"):
        for el in rpr.findall(qn(tag)):
            rpr.remove(el)
    return rpr


def set_text(p, text, keep_format=True):
    runs = p.runs
    rpr = clean_rpr(runs[0]._r.find(qn("w:rPr"))) if (runs and keep_format) else None
    for child in list(p._p):
        if child.tag in (qn("w:r"), qn("w:hyperlink")):
            p._p.remove(child)
    for i, line in enumerate(text.split("\n")):
        r = p.add_run(line)
        if rpr is not None:
            r._r.insert(0, copy.deepcopy(rpr))
        if i < text.count("\n"):
            r.add_break()
    return p


def clone_after(p, text):
    new = copy.deepcopy(p._p)
    p._p.addnext(new)
    np_ = docx.text.paragraph.Paragraph(new, p._parent)
    return set_text(np_, text)


def fill_table(t, rows):
    """rows exclude header; adds or removes body rows to match."""
    while len(t.rows) - 1 < len(rows):
        t._tbl.append(copy.deepcopy(t.rows[-1]._tr))
    while len(t.rows) - 1 > len(rows):
        t._tbl.remove(t.rows[-1]._tr)
    for r, vals in zip(t.rows[1:], rows):
        for c, v in zip(r.cells, vals):
            set_text(c.paragraphs[0], v)
            for extra in c.paragraphs[1:]:
                extra._p.getparent().remove(extra._p)


def replace_in_table(t, old, new):
    for row in t.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                if old in p.text:
                    set_text(p, p.text.replace(old, new))


# ---------- front matter ----------
names_ids = [f"{m} ({ID})" for m in MEMBERS]
set_text(P[0], TITLE)
set_text(P[5], names_ids[0])
set_text(P[6], "\n".join(names_ids[1:]))
set_text(P[16], MONTH)
set_text(P[21], f"PROJECT TITLE: {TITLE}")
set_text(P[22], f"ACADEMIC SESSION: {SESSION}")
set_text(P[23], P[23].text.replace("[FULL NAMES OF ALL GROUP MEMBERS]", ", ".join(MEMBERS)))
TITLE_CASE = ("Design and Evaluation of a Hybrid Prompt-Aware, Multi-Objective Large Language Model "
              "Routing System with Automatic Fallback")
SUP_CASE = "[Supervisor's full name]"
cert = (f'This is to certify that the project titled "{TITLE_CASE}" by ' + ", ".join(names_ids[:-1])
        + f" and {names_ids[-1]} has been read and approved as meeting the requirements for the award of the "
        "degree of Bachelor of Science (B.Sc. Hons) in Software Engineering, Department of Software Engineering, "
        "Faculty of Computing, Nile University of Nigeria, Abuja.")
set_text(P[33], cert)
set_text(P[35], SUP_CASE)
set_text(P[63], SUPERVISOR)
decl = [P[54], P[55], P[56], P[57]]
last = P[57]
for _ in range(len(MEMBERS) - 4):
    last = clone_after(last, P[57].text)
    decl.append(last)
for p, n in zip(decl, names_ids):
    set_text(p, f"Name (Student ID):  {n}   Signature: ………………………")
set_text(P[67], "Each member's planned role and main contributions are listed below. These follow the team's task "
         "distribution; each member will confirm or correct their own entry, in their own words, before signing.")
set_text(P[71], "Generative AI tools were used in preparing this proposal, as declared in the table below. "
         "The team remains responsible for all content and has checked, or will check before submission, "
         "every AI-assisted section against the original sources.")
P[73]._p.getparent().remove(P[73]._p)
set_text(P[77], "We dedicate this project to [to be written by the team].")
set_text(P[95], f"We thank our supervisor, {SUP_CASE}, for guidance throughout this proposal, and the staff "
         "of the Department of Software Engineering, Nile University of Nigeria, for the Research Methodology "
         "modules that shaped its structure. We also thank our families for their support.")
set_text(P[113], ABSTRACT)
set_text(P[114], KEYWORDS)
print("abstract words:", len(ABSTRACT.split()))

TABLES_LIST, FIGS_LIST = [], []  # filled while building the body; written at the end

T = doc.tables
replace_in_table(T[1], "Permanent address of the group leader", "[Permanent address of the group leader]")
replace_in_table(T[1], "Dr. Supervisor", SUP_CASE)
fill_table(T[2], [(str(i + 1), n.title() if not n.startswith("[") else n, ID, role, work, "")
                  for i, (n, (role, work)) in enumerate(zip(MEMBERS, CONTRIB))])
fill_table(T[3], GENAI)
fill_table(T[4], ABBREV)
set_text(P[196], "Each abbreviation is also spelt out in full at its first use in the text.")
list_tables_p, list_figs_p = P[137], P[171]
table_style = T[5].style

# ---------- remove template body (Chapter One to the end) ----------
body = doc.element.body
start = P[199]._p
el = start
while el is not None and el.tag != qn("w:sectPr"):
    nxt = el.getnext()
    body.remove(el)
    el = nxt


# ---------- body builder ----------
def fmt_body(p, indent=True, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    pf = p.paragraph_format
    pf.line_spacing = 1.5
    pf.space_after = Pt(6)
    pf.alignment = align
    if indent:
        pf.first_line_indent = Inches(0.5)


INLINE = re.compile(r"(\*\*[^*]+\*\*|\*[^*]+\*)")


def add_runs(p, text, size=12):
    for part in INLINE.split(text):
        if not part:
            continue
        bold = part.startswith("**")
        ital = not bold and part.startswith("*")
        r = p.add_run(part.strip("*") if (bold or ital) else part)
        r.bold, r.italic = bold or None, ital or None
        r.font.name, r.font.size = "Times New Roman", Pt(size)


def para(text, indent=True, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph(style="Normal")
    add_runs(p, text)
    fmt_body(p, indent, align)
    return p


def caption(text):
    p = doc.add_paragraph(style="Normal")
    add_runs(p, text, 11)
    p.runs[0].bold = True
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    return p


def set_borders(tbl):
    tblPr = tbl._tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{side}")
        e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "4"); e.set(qn("w:color"), "000000")
        b.append(e)
    tblPr.append(b)


def shade(cell, fill="D9E2F3"):
    tcPr = cell._tc.get_or_add_tcPr()
    s = OxmlElement("w:shd")
    s.set(qn("w:val"), "clear"); s.set(qn("w:color"), "auto"); s.set(qn("w:fill"), fill)
    tcPr.append(s)


def table(cap, rows):
    TABLES_LIST.append(cap)
    caption(cap)
    ncol = len(rows[0])
    size = 12 if ncol <= 3 else (10 if ncol <= 5 else 9)
    t = doc.add_table(rows=len(rows), cols=ncol)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_borders(t)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = t.cell(i, j)
            p = cell.paragraphs[0]
            add_runs(p, val, size - (1 if size == 12 else 0))
            p.paragraph_format.line_spacing = 1.0
            if i == 0:
                for r in p.runs:
                    r.bold = True
                shade(cell)
    # column widths proportional to average text length, within the 5.7 in text block
    longest = [max(len(w) for r in rows for w in (r[j].replace('*', '').split() or ['x'])) for j in range(ncol)]
    avg = [max(longest[j] * 1.3 + 3, min(40, sum(len(r[j]) for r in rows) / len(rows))) for j in range(ncol)]
    t.autofit = False
    for j, a in enumerate(avg):
        w = Inches(5.7 * a / sum(avg))
        for cell in t.columns[j].cells:
            cell.width = w
    doc.add_paragraph()


def figure(fname, cap):
    FIGS_LIST.append(cap)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(str(FIGS / fname), width=Inches(5.6))
    caption(cap).paragraph_format.keep_with_next = False


lines = (HERE / "proposal_content.md").read_text(encoding="utf8").splitlines()
i, buf, num, first_chapter = 0, [], 0, True


def flush():
    global buf
    if buf:
        para(" ".join(buf))
        buf = []


while i < len(lines):
    ln = lines[i].rstrip()
    if ln.startswith("%%"):
        i += 1; continue
    if not ln.strip():
        flush(); num = 0; i += 1; continue
    if ln.startswith("# "):
        flush()
        h = doc.add_paragraph(ln[2:], style="Heading 1")
        if ln[2:] in ("REFERENCES", "APPENDICES") or (ln[2:].startswith("CHAPTER") and not first_chapter):
            h.paragraph_format.page_break_before = True
        if ln[2:].startswith("CHAPTER"):
            first_chapter = False
    elif ln.startswith("## "):
        flush(); h = doc.add_paragraph(style="Heading 2"); r = h.add_run(ln[3:])
        r.bold = True; r.font.name, r.font.size = "Times New Roman", Pt(12)
        h.paragraph_format.space_before = Pt(12); h.paragraph_format.keep_with_next = True
    elif ln.startswith("- "):
        flush()
        p = doc.add_paragraph(style="List Paragraph"); add_runs(p, "•\t" + ln[2:])
        fmt_body(p, indent=False)
        p.paragraph_format.left_indent = Inches(0.5); p.paragraph_format.first_line_indent = Inches(-0.25)
    elif ln.startswith("N> "):
        flush(); num += 1
        p = doc.add_paragraph(style="List Paragraph"); add_runs(p, f"{num}.\t" + ln[3:])
        fmt_body(p, indent=False)
        p.paragraph_format.left_indent = Inches(0.5); p.paragraph_format.first_line_indent = Inches(-0.25)
    elif ln.startswith("P> "):
        flush(); para(ln[3:], indent=False)
    elif ln.startswith("C> "):
        flush(); para(ln[3:], indent=False, align=WD_ALIGN_PARAGRAPH.CENTER)
    elif ln.startswith("R> "):
        flush()
        p = para(ln[3:], indent=False, align=WD_ALIGN_PARAGRAPH.LEFT)
        p.paragraph_format.left_indent = Inches(0.5); p.paragraph_format.first_line_indent = Inches(-0.5)
    elif ln.startswith("F> "):
        flush(); f, cap = [s.strip() for s in ln[3:].split("|", 1)]; figure(f, cap)
    elif ln.startswith("T> "):
        flush(); cap = ln[3:].strip(); rows = []
        while i + 1 < len(lines) and lines[i + 1].startswith("|"):
            i += 1
            rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
        table(cap, rows)
    else:
        buf.append(ln.strip())
    i += 1
flush()

# ---------- lists of tables and figures ----------
for anchor, items in ((list_tables_p, TABLES_LIST), (list_figs_p, FIGS_LIST)):
    set_text(anchor, items[0])
    last = anchor
    for it in items[1:]:
        last = clone_after(last, it)

doc.save(OUT)
print("tables:", len(TABLES_LIST), "figures:", len(FIGS_LIST), "->", OUT)
