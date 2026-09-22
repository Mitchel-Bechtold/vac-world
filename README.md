# CS3810 Mini-Project 1 — Vacuum World Search

Extended Vacuum World: a robot must clean every dirty cell on a grid with
obstacles while minimizing total path cost. Implements DFS, A*, and IDA*
search over the state space `((row, col), frozenset(dirty_cells))`, plus
four heuristics (`h0`–`h3`) for the informed searches.

## Requirements

- Python 3.8+ (developed and tested on 3.11)
- `pandas` and `matplotlib` for the Part 4 analysis (`pip install pandas matplotlib tabulate`)
  - `tabulate` is only needed for the Markdown table export in `experiments.py`

Everything else (`dfs_search`, `astar_search`, `idastar_search`, the
`VacuumWorld` class, and all heuristics) uses only the Python standard
library, per the assignment's "no library search implementations" rule.

## File structure

| File | Contents |
|------|----------|
| `vacuum_world.py` | Part 1 — the `VacuumWorld` environment |
| `search.py` | Part 2 — `dfs_search`, `astar_search`, `idastar_search` |
| `heuristics.py` | Part 3 — `h0`, `h1`, `h2`, and the bonus `h3` (MST-based) |
| `experiments.py` | Part 4 — measurement harness, results table, and both plots |
| `test_grids.py` | Provided — the six graded grids, unmodified |
| `priority_queue.py` | Provided — decrease-key priority queue used by A*, unmodified |
| `run_tests.py` | Provided — smoke tests, unmodified |
| `results.csv` | Raw output of the full experiment sweep |
| `results_table.csv` / `results_table.md` | Cleaned-up results table used in the report |
| `figures/scaling.png` | Plot 1 — nodes expanded vs. number of dirty cells |
| `figures/heuristics.png` | Plot 2 — A* nodes expanded by heuristic, per grid |
| `report.pdf` | Design decisions, heuristic proofs, results, discussion, reflection |
| `AI_USE.md` | Required AI-use disclosure |

## Running the smoke tests

```bash
python run_tests.py
```

This should report `17 passed, 0 failed, 0 skipped` (all required tests plus
the `h3` bonus). These are sanity checks, not the grading rubric — passing
them means the code behaves correctly on the documented cases, not that the
report or analysis is complete.

## Running the experiments

```bash
python experiments.py --quick              # 3 smallest grids, fast sanity check
python experiments.py                      # full sweep, all 6 grids, 60s timeout/config
python experiments.py --timeout 120        # more patience for a slower machine
python experiments.py --grids g6_corridor  # rerun just one grid
python experiments.py --analyze            # also (re)build the table and both plots
```

A full `--analyze` run does three things:

1. Sweeps every `(grid, algorithm, heuristic)` combination (54 configurations
   across the 6 graded grids), each in its own subprocess with a timeout, and
   writes the raw results to `results.csv`.
2. Builds a cleaned-up, sorted results table (`results_table.csv` and
   `results_table.md`) via `make_table()`.
3. Renders `figures/scaling.png` (nodes expanded vs. problem size, one line
   per algorithm) and `figures/heuristics.png` (A* nodes expanded by
   heuristic, grouped by grid) via `plot_scaling()` and `plot_heuristics()`.

On the full sweep, expect it to take a few minutes — IDA* with the weaker
heuristics (`h0`, `h1`) on the larger grids expands a lot of nodes, and a
couple of configurations on `g6_corridor` hit the 60-second timeout. That is
an expected, reportable result, not a bug — see `report.pdf` for discussion.

## Notes

- All searches operate on states of the form `((row, col), frozenset(dirty))`,
  which are hashable and immutable; `VacuumWorld.result()` never mutates a
  state in place.
- `get_actions()` always returns actions in the canonical order
  `['MOVE_UP', 'MOVE_DOWN', 'MOVE_LEFT', 'MOVE_RIGHT', 'CLEAN']`, filtered to
  legal moves, so node counts are reproducible.
- `nodes_expanded` counts a node only when it is popped from the frontier
  *and* its successors are generated (a node that turns out to be the goal on
  pop is not counted, since no successors are generated for it).
- The bonus heuristic `h3` combines the dirty-cell count, the distance to the
  nearest dirty cell, and the weight of a minimum spanning tree (Manhattan
  distance) over all remaining dirty cells — a lower bound on the travel
  still required after reaching the first one. See `report.pdf` for the
  admissibility argument and the dominance data versus `h2`.
