# AI Use Disclosure — CS3810 Mini-Project 1

## Tool used

Claude (Anthropic), via an interactive chat/coding session. No other AI tool
(ChatGPT, Copilot, etc.) was used on this project.

## Permission for this level of use

The assignment's default Generative AI Policy (Section 9) does not permit
generating the search algorithm, environment, or heuristic implementations.
For this project, Mitchel Bechtold discussed this with the instructor,
**[Professor NAME — fill in]**, who granted permission to use AI more
broadly than the default policy allows, given that this project is advanced
for students early in an AI course. **[Fill in: date/method this permission
was given — e.g. "verbally after the 9/XX lecture" or "via email on 9/XX" —
and attach or reference confirmation if you have it, so the disclosure is
verifiable.]**

Everything described below beyond the default-permitted uses (explaining
concepts, debugging code I wrote, boilerplate generation, grammar editing)
was done under that permission.

## What Claude was used for

- **`vacuum_world.py` (Part 1):** Claude wrote the full implementation
  (`__init__`, `in_bounds`, `is_passable`, `initial_state`, `is_goal`,
  `get_actions`, `result`, `action_cost`, `render`), explaining the design
  reasoning for each method (state immutability, canonical action ordering,
  hashability) as it was written. I reviewed the code and verified it against
  `run_tests.py` after each method.
- **`heuristics.py` (Part 3):** Claude wrote `manhattan`, `h0`, `h1`, `h2`,
  and the optional bonus `h3` (a minimum-spanning-tree-based heuristic over
  the remaining dirty cells), including the underlying admissibility
  reasoning for each. I did not write the code myself, but the admissibility
  arguments in `report.pdf` are my own writing, informed by that explanation.
- **`search.py` (Part 2):** Claude wrote `dfs_search`, `astar_search`,
  `_reconstruct`, and `idastar_search`, explaining the design of each
  (explicit-stack DFS with an explored set, A* reopening via the provided
  `PriorityQueue`'s decrease-key behavior, and the recursive f-threshold
  structure of IDA*) as it was written.
- **`experiments.py` (Part 4 — measurement plumbing was pre-provided):**
  Claude wrote `make_table`, `plot_scaling`, and `plot_heuristics` (the
  boilerplate the handout explicitly calls out as permitted: pandas table
  construction, matplotlib plotting code). This also generated
  `results.csv`, `results_table.csv`/`.md`, and the two PNG figures by
  running the harness.
- **`README.md` and this `AI_USE.md`:** drafted by Claude and reviewed/edited
  by me.

## What Claude was NOT used for

- **`report.pdf`** — the design-decision write-up, the admissibility proofs
  for `h1`/`h2`/`h3`, the results discussion (all six discussion questions),
  and the reflection — is my own writing. Claude's code-and-concept
  explanations informed my understanding, but the analysis and prose are
  mine, and I can explain any part of the submission if asked.
- I did not use Claude to generate or rewrite any part of the discussion
  questions' reasoning, including the Roomba reflection question.

## Rough extent

Substantial: the majority of the code in `vacuum_world.py`, `search.py`,
`heuristics.py`, and the analysis functions in `experiments.py` was written
by Claude rather than by me, under the instructor permission described
above. The report (70 of the 200 total points) is entirely my own work.
