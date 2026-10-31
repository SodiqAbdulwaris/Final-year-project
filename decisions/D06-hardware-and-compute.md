Status: DRAFT
Depends on: Owner proposal-building instructions, 31 October 2026
Sources: proposal-drafts/_meta/decisions-applied.md
Open items: Only residual implementation/evidence details stated in current register

# D06 current outcome

Two RTX 4070 machines, desktop and laptop; minimal API budget, capped pilot and local failure tests.

The owner has supplied this decision; do not re-ask the historical question below. [Applied register](../proposal-drafts/_meta/decisions-applied.md).

## Historical question and recommendation (superseded)

# D06: Hardware, GPU access and API budget

| | |
|---|---|
| Status | **OPEN, needs your decision** |
| Who decides | You and the team |
| Blocks | E5 (local backends), any live-load work, vLLM use |
| Default used meanwhile | Assume no dedicated GPU server; mock providers for failure tests |

## The question
What GPU/server access and API credit do you actually have?

## What I found
- vLLM needs a CUDA GPU; Ollama/LM Studio/llama.cpp run on CPU or small GPUs.
- The guide warns not to load several models on an 8 GB GPU to mimic a production pool and not to claim every local server exposes queue-depth metrics.
- Failure/overhead tests can use a mock provider (guide, E4) without any GPU.

## Options
| Option | Notes |
|---|---|
| Laptop + Ollama | Cheap, enough for E5 basics |
| Free/cheap cloud GPU for vLLM | Needed only for vLLM `/metrics` and load tests |
| Mock providers only for load/failure | Zero cost; cannot show real latency |

## Recommendation
Laptop + Ollama for the local deployment, hosted APIs for the others, a mock provider for E4 and fault injection, and a short rented GPU session only if you commit to the live-load extension (D01).

## Consequences and things to watch
State exact hardware in Table 4.1; results are not transferable without it.

## Where this shows up in the files
`proposal-drafts/03-methodology-design/00-overview.md`, `ch4-ch5-skeletons.md` (Table 4.1)
