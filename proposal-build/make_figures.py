import sys, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
plt.rcParams["font.family"] = "Times New Roman"


def canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, w * 10)
    ax.set_ylim(0, h * 10)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, text, fc="#ffffff", fs=10, bold=False, ec="#222222", style="round,pad=0.4"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=style, fc=fc, ec=ec, lw=1.1))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal", wrap=True)
    return (x, y, w, h)


def arrow(ax, x1, y1, x2, y2, label=None, style="-|>", ls="-"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, lw=1.1, color="#222222", linestyle=ls))
    if label:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 1.2, label, ha="center", fontsize=8.5, style="italic")


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=200, bbox_inches="tight")
    plt.close(fig)


# Figure 2.1 conceptual framework
fig, ax = canvas(11, 6.2)
A = "#eef3fb"; B = "#fdf3e6"; C = "#eef7ee"
box(ax, 2, 44, 24, 12, "Request\n(prompt, optional cost cap\nand deadline)", A, bold=True)
box(ax, 2, 26, 24, 12, "Prompt features\ntask category, difficulty,\nembedding similarity", A)
box(ax, 2, 8, 24, 12, "Scored history\npast outcomes per model\non similar prompts", A)
box(ax, 36, 30, 22, 16, "Model-specific\nsuitability estimate\nQ̂(m, q)", B, bold=True)
box(ax, 36, 8, 22, 14, "Cost and latency\nestimates Ĉ(m, q), L̂(m, q)\nfrom prices and timing logs", B)
box(ax, 36, 50, 22, 10, "Hard constraints\ncapability, context, budget,\nhealth", B)
box(ax, 68, 30, 20, 16, "Constrained\nselection policy", C, bold=True)
box(ax, 68, 8, 20, 14, "Reliability control\nhealth, circuit breaker,\nbounded fallback", C)
box(ax, 94, 30, 14, 16, "Observed\nquality, cost,\nlatency, success", "#f4f4f4")
arrow(ax, 14, 44, 14, 38.5); arrow(ax, 14, 26, 14, 20.5)
arrow(ax, 26.5, 32, 35.5, 38); arrow(ax, 26.5, 14, 35.5, 34)
arrow(ax, 26.5, 50, 35.5, 55)
arrow(ax, 58.5, 38, 67.5, 38); arrow(ax, 58.5, 15, 67.5, 33)
arrow(ax, 58.5, 55, 67.5, 44)
arrow(ax, 78, 29.5, 78, 22.5, "execute")
arrow(ax, 88.5, 15, 98, 29.5)
arrow(ax, 101, 29.5, 101, 4, style="-"); arrow(ax, 101, 4, 14, 4, style="-"); arrow(ax, 14, 4, 14, 7.5)
ax.text(58, 1.2, "outcomes logged as new scored evidence (offline updates only)", ha="center", fontsize=8.5, style="italic")
ax.text(70, 58, "Design Science Research lens: artefact evaluated against baselines", fontsize=9, style="italic")
save(fig, "fig2_1.png")

# Figure 3.1 DSR process
fig, ax = canvas(11, 4.6)
steps = [("1. Identify problem", "Ch. 1.2; gaps in 2.7"),
         ("2. Define objectives", "Obj. 1-6; Table 3.2 targets"),
         ("3. Design and develop", "Scrum, six two-week sprints"),
         ("4. Demonstrate", "replay on benchmark data;\ncapped live pilot"),
         ("5. Evaluate", "baselines, ablations,\nfault injection (3.9)"),
         ("6. Communicate", "final report, code,\nexperiment protocol")]
x = 1
for i, (t, s) in enumerate(steps):
    box(ax, x, 18, 15, 14, f"{t}\n\n{s}", ["#eef3fb", "#eef3fb", "#fdf3e6", "#eef7ee", "#eef7ee", "#f4f4f4"][i], fs=9)
    if i < 5:
        arrow(ax, x + 15.6, 25, x + 17.6, 25)
    x += 18
arrow(ax, 81, 17.5, 81, 8, style="-"); arrow(ax, 81, 8, 44, 8, style="-"); arrow(ax, 44, 8, 44, 17.5, "iterate when results miss targets")
save(fig, "fig3_1.png")

# Figure 3.2 architecture and deployment
fig, ax = canvas(11, 7.4)
ax.add_patch(FancyBboxPatch((1, 6), 70, 66, boxstyle="round,pad=0.4", fc="none", ec="#777777", ls="--"))
ax.text(3, 69.5, "Machine 1 (RTX 4070 laptop): router service", fontsize=9, style="italic")
box(ax, 26, 76, 22, 7, "Client application\n(OpenAI-compatible call)", "#f4f4f4", fs=9)
box(ax, 6, 58, 60, 8, "Gateway API (FastAPI): authentication, validation, request IDs", "#eef3fb", fs=9.5, bold=True)
box(ax, 6, 45, 28, 9, "Constraint filter\ncapability, context, budget, health", "#fdf3e6", fs=9)
box(ax, 38, 45, 28, 9, "Prompt analyser\nclassifier + embedding retrieval", "#fdf3e6", fs=9)
box(ax, 6, 32, 28, 9, "Suitability predictor\nQ̂, Ĉ, L̂ per model", "#fdf3e6", fs=9)
box(ax, 38, 32, 28, 9, "Selection policy\nconstrained, versioned", "#fdf3e6", fs=9)
box(ax, 6, 19, 60, 9, "Reliability controller: health tracker, circuit breakers, bounded retry and fallback", "#eef7ee", fs=9.5)
box(ax, 6, 8, 28, 8, "Provider adapters\n(local and hosted)", "#eef7ee", fs=9)
box(ax, 38, 8, 28, 8, "PostgreSQL\nrequests, decisions, attempts", "#f4f4f4", fs=9)
box(ax, 78, 52, 28, 9, "Local model server\n(Ollama, small model)", "#ffffff", fs=9)
box(ax, 78, 38, 28, 9, "Hosted API\nmid-tier model", "#ffffff", fs=9)
box(ax, 78, 24, 28, 9, "Hosted API\nfrontier model", "#ffffff", fs=9)
box(ax, 78, 6, 28, 12, "Machine 2 (RTX 4070 laptop)\nevaluation harness, load generator,\nmock provider for fault injection", "#f4f4f4", fs=8.5)
arrow(ax, 37, 75.5, 37, 66.5)
arrow(ax, 20, 57.5, 20, 54.5); arrow(ax, 52, 57.5, 52, 54.5)
arrow(ax, 20, 44.5, 20, 41.5); arrow(ax, 52, 44.5, 52, 41.5); arrow(ax, 34.5, 36.5, 37.5, 36.5)
arrow(ax, 52, 31.5, 52, 28.5); arrow(ax, 20, 18.5, 20, 16.5); arrow(ax, 52, 18.5, 52, 16.5)
for yy in (56, 42, 28):
    arrow(ax, 66.5, 12, 77.5, yy, style="<|-|>")
arrow(ax, 92, 18.5, 92, 23.5, style="-|>", ls="--")
ax.text(93.5, 20, "test traffic", fontsize=8.5, style="italic")
save(fig, "fig3_2.png")

# Figure 3.3 use case
fig, ax = canvas(11, 7)
ax.add_patch(FancyBboxPatch((24, 3), 60, 64, boxstyle="round,pad=0.4", fc="none", ec="#333333"))
ax.text(54, 64, "Prompt-aware routing system", ha="center", fontsize=10, fontweight="bold")
ucs = [("Send chat request", 56), ("Set cost cap and deadline", 48), ("View routing decision", 40),
       ("Register model and prices", 32), ("Configure policy and fallback", 24), ("View usage dashboard", 16),
       ("Run replay experiment", 8)]
from matplotlib.patches import Ellipse
for t, y in ucs:
    ax.add_patch(Ellipse((54, y + 2), 34, 6.5, fc="#eef3fb", ec="#333333"))
    ax.text(54, y + 2, t, ha="center", va="center", fontsize=9.5)


def actor(x, y, name):
    ax.add_patch(plt.Circle((x, y + 9), 1.6, fc="white", ec="black"))
    ax.plot([x, x], [y + 7.4, y + 3], c="black"); ax.plot([x - 2.5, x + 2.5], [y + 6, y + 6], c="black")
    ax.plot([x, x - 2], [y + 3, y], c="black"); ax.plot([x, x + 2], [y + 3, y], c="black")
    ax.text(x, y - 2.5, name, ha="center", va="top", fontsize=9.5)


actor(8, 44, "Client developer"); actor(8, 18, "Administrator"); actor(100, 6, "Evaluator")
actor(100, 44, "Model provider\n(secondary)")
for y in (58, 50, 42):
    ax.plot([11, 37], [52, y], c="#444444", lw=0.8)
for y in (34, 26, 18):
    ax.plot([11, 37], [25, y], c="#444444", lw=0.8)
ax.plot([97, 71], [12, 10], c="#444444", lw=0.8)
ax.plot([97, 71], [52, 58], c="#444444", lw=0.8)
save(fig, "fig3_3.png")

# Figure 3.4 ERD
fig, ax = canvas(11, 10.6)
cols = (2, 40, 78); rows = (72, 37, 2)
ents = {
    "API_CLIENT": (0, 0, ["PK client_id", "name", "key_hash", "budget_limit"]),
    "REQUEST": (1, 0, ["PK request_id", "FK client_id", "received_at, prompt_hash", "task_category", "difficulty_score", "max_cost, deadline_ms"]),
    "ROUTING_DECISION": (2, 0, ["PK decision_id", "FK request_id", "FK chosen_model_id", "policy_version", "pred_quality, pred_cost", "pred_latency_ms, reason"]),
    "PROVIDER": (0, 1, ["PK provider_id", "name", "base_url", "is_local", "credential_ref"]),
    "MODEL": (1, 1, ["PK model_id", "FK provider_id", "name, revision, tier", "input_price, output_price", "context_window", "capabilities"]),
    "ATTEMPT": (2, 1, ["PK attempt_id", "FK decision_id", "FK model_id", "attempt_no, status", "http_code, error_type", "ttft_ms, latency_ms", "tokens_in, tokens_out, cost"]),
    "HEALTH_EVENT": (1, 2, ["PK event_id", "FK model_id", "breaker_state", "error_type, observed_at"]),
    "QUALITY_SCORE": (2, 2, ["PK score_id", "FK attempt_id", "method, score", "scored_at"]),
}
pos = {}
for name, (c, r, fields) in ents.items():
    x = cols[c]; h = 3.3 * len(fields) + 5; y = rows[r] + (30 - h)
    ax.add_patch(FancyBboxPatch((x, y), 30, h, boxstyle="square,pad=0", fc="#ffffff", ec="#222222", zorder=2))
    ax.add_patch(FancyBboxPatch((x, y + h - 5), 30, 5, boxstyle="square,pad=0", fc="#dfe8f6", ec="#222222", zorder=2))
    ax.text(x + 15, y + h - 2.5, name, ha="center", va="center", fontsize=9, fontweight="bold", zorder=3)
    for i, f in enumerate(fields):
        ax.text(x + 1.2, y + h - 7.5 - 3.3 * i, f, fontsize=8.3, zorder=3)
    pos[name] = (x, y, 30, h)


def edge(n, side):
    x, y, w, h = pos[n]
    return {"r": (x + w, y + h / 2), "l": (x, y + h / 2), "t": (x + w / 2, y + h), "b": (x + w / 2, y),
            "tr": (x + w, y + h - 3), "bl": (x, y + 3)}[side]


def link(a, sa, b, sb, la, lb):
    p1 = edge(a, sa); p2 = edge(b, sb)
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], c="#444444", lw=1, zorder=1)
    for (px, py), (qx, qy), lab in ((p1, p2, la), (p2, p1, lb)):
        ax.text(px + (qx - px) * 0.12 + 0.8, py + (qy - py) * 0.12 + 0.8, lab, fontsize=8.5, color="#aa2222", zorder=3)


link("API_CLIENT", "r", "REQUEST", "l", "1", "N")
link("REQUEST", "r", "ROUTING_DECISION", "l", "1", "1")
link("ROUTING_DECISION", "b", "ATTEMPT", "t", "1", "1..N")
link("PROVIDER", "r", "MODEL", "l", "1", "N")
link("MODEL", "r", "ATTEMPT", "l", "1", "N")
link("MODEL", "b", "HEALTH_EVENT", "t", "1", "N")
link("ATTEMPT", "b", "QUALITY_SCORE", "t", "1", "0..1")
link("MODEL", "tr", "ROUTING_DECISION", "bl", "1", "N")
save(fig, "fig3_4.png")

# Figure 3.5 flowchart
fig, ax = canvas(9.6, 10.5)
cx = 45
nodes = [("Receive request; validate input", 98), ("Filter models on hard constraints", 86),
         ("Any eligible model?", 74), ("Extract features: class, difficulty,\nk nearest scored prompts", 62),
         ("Predict Q̂, Ĉ, L̂ for each eligible model", 50),
         ("Keep models with Q̂ ≥ τ, Ĉ ≤ cap, L̂ ≤ deadline;\nchoose lowest Ĉ (ties: higher Q̂)", 38),
         ("Call model through adapter", 26), ("Retryable failure and\nattempts, budget, time remain?", 14),
         ("Return response with routing metadata; log", 2)]
for t, y in nodes:
    shape = "round,pad=0.4"
    fc = "#fdf3e6" if "?" in t else "#eef3fb"
    box(ax, cx - 22, y, 44, 7, t, fc, fs=9)
for (a, ya), (b, yb) in zip(nodes, nodes[1:]):
    arrow(ax, cx, ya - 0.6, cx, yb + 7.6)
box(ax, 74, 74, 16, 7, "Reject with\nreason code", "#f4f4f4", fs=8.5)
arrow(ax, 67.5, 77.5, 73.5, 77.5, "no")
ax.text(cx + 1.5, 70.5, "yes", fontsize=8.5, style="italic")
box(ax, 74, 22, 16, 11, "Open breaker if\nthreshold hit; mark\nmodel ineligible;\nre-run selection", "#eef7ee", fs=8)
arrow(ax, 67.5, 17.5, 82, 21.5, "yes")
arrow(ax, 82, 33.5, 82, 41, style="-"); arrow(ax, 82, 41, 67.5, 41)
ax.text(cx + 1.5, 10.5, "no: success, or error returned", fontsize=8.5, style="italic")
save(fig, "fig3_5.png")

# Figure 3.6 wireframe
fig, ax = canvas(11, 7)
ax.add_patch(FancyBboxPatch((1, 1), 108, 68, boxstyle="square,pad=0", fc="#ffffff", ec="#333333"))
box(ax, 1, 62, 108, 7, "Router dashboard          Overview | Requests | Models | Policies | Experiments          [admin]", "#dfe8f6", fs=9.5, style="square,pad=0")
for i, (k, v) in enumerate([("Requests today", "1,240"), ("Spend today", "US$ 0.84"), ("p95 latency", "2.9 s"), ("Fallback rate", "1.1%")]):
    box(ax, 4 + i * 27, 48, 24, 10, f"{k}\n{v}", "#f4f4f4", fs=10, style="square,pad=0")
ax.text(4, 44, "Recent requests (sample data)", fontsize=9.5, fontweight="bold")
rows = [("Time", "Task", "Chosen model", "Reason", "Cost", "Latency"),
        ("10:42:07", "code", "frontier", "small model Q̂ below τ", "0.004", "3.1 s"),
        ("10:42:05", "chat", "local-small", "cheapest feasible", "0.000", "0.9 s"),
        ("10:41:58", "maths", "mid-tier", "fallback: frontier timeout", "0.002", "4.4 s")]
for r, row in enumerate(rows):
    for c, cell in enumerate(row):
        ax.text(5 + [0, 12, 22, 38, 60, 70][c], 39 - r * 5, cell, fontsize=8.5, fontweight="bold" if r == 0 else "normal")
ax.plot([4, 80], [37.5, 37.5], c="#999999", lw=0.6)
box(ax, 84, 8, 22, 36, "Model health\n\nlocal-small: closed\nmid-tier: closed\nfrontier: half-open\n\n[open breaker log]", "#eef7ee", fs=8.5, style="square,pad=0")
box(ax, 4, 6, 76, 12, "Cost vs quality chart for the selected period (hybrid policy vs baselines)", "#fbfbfb", fs=9, style="square,pad=0")
save(fig, "fig3_6.png")
print("ok")
