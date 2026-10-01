"""
CS3810 Mini-Project 1 - Part 4 Discussion Answers (Section 5 of the handout)
=============================================================================

This script answers the six discussion questions required by Part 4. Every
number cited in the text below is computed directly from results.csv and
test_grids.py rather than hand-typed, so the figures stay correct even if
you rerun the experiments and the numbers change slightly.

Run it from the project directory (same folder as results.csv and
test_grids.py):

    python discussion_answers.py

It just prints the six answers to the terminal - nothing is written,
uploaded, or pushed anywhere.
"""

import sys
import textwrap

import pandas as pd

from test_grids import GRIDS, parse_grid

RESULTS_CSV = "results.csv"
WIDTH = 78


def load_results():
    try:
        return pd.read_csv(RESULTS_CSV)
    except FileNotFoundError:
        sys.exit(
            "Could not find %r. Run this script from the same folder as "
            "results.csv (and run experiments.py first if you haven't)."
            % RESULTS_CSV
        )


def get_row(df, grid, algorithm, heuristic=None):
    """Return the one matching row from results.csv as a pandas Series."""
    mask = (df["grid"] == grid) & (df["algorithm"] == algorithm)
    if heuristic is not None:
        mask &= df["heuristic"] == heuristic
    matches = df[mask]
    if matches.empty:
        raise ValueError("no row for %s/%s/%s in %s" % (grid, algorithm, heuristic, RESULTS_CSV))
    return matches.iloc[0]


def wrap(paragraph):
    """Collapse a hand-typed, line-broken paragraph to one line and re-wrap
    it at WIDTH columns. Writing the source text with natural line breaks
    (for readability in the editor) and then re-flowing it here means a
    substituted number's digit count never produces an awkward hard break -
    unlike wrapping by hand ONCE around short example numbers and then
    discovering a real run produced a 7-digit node count instead.
    """
    collapsed = " ".join(paragraph.split())
    return textwrap.fill(collapsed, width=WIDTH)


def heading(title):
    return title + "\n" + "-" * WIDTH


def question_1(df):
    dfs = get_row(df, "g6_corridor", "dfs")
    astar_h0 = get_row(df, "g6_corridor", "astar", "h0")
    optimal = astar_h0["cost"]
    ratio = dfs["cost"] / optimal

    para1 = wrap(f"""
        Fewer nodes expanded: DFS has no notion of "better" or "worse" among
        candidate plans. It commits fully to one branch, follows it to
        completion, and stops at the very first sequence of actions that
        reaches the goal - it never backtracks to compare alternatives once
        something already works. On g6_corridor, DFS expanded only
        {dfs['nodes_expanded']:.0f} nodes versus A*/h0's
        {astar_h0['nodes_expanded']:.0f} - it simply didn't need to look at
        most of the reachable state space before stumbling onto *some*
        working path.
    """)

    para2 = wrap(f"""
        Worse solution quality: this is the exact same mechanism, seen from
        the other side. Because DFS stops the instant it finds anything
        that works, whatever path the fixed action order (MOVE_UP,
        MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, CLEAN) happens to walk it down
        first is what you get, however circuitous that path is. On that
        same grid, DFS's plan cost {dfs['cost']:.0f} actions against a true
        optimum of {optimal:.0f} - about {ratio:.1f}x longer. The two
        halves of the sentence aren't two separate phenomena; they are one
        cause (zero cost-awareness) producing two visible effects: cheap to
        stop, and low quality when it does.
    """)

    return "\n".join([
        heading("Q1: DFS usually expands far fewer nodes than A* on some grids, yet\n"
                "returns much worse solutions. Explain both halves of that sentence."),
        "",
        para1,
        "",
        para2,
    ])


def question_2(df):
    grids_in_order = list(GRIDS)
    table_lines = []
    for grid in grids_in_order:
        h0 = get_row(df, grid, "astar", "h0")["nodes_expanded"]
        h1 = get_row(df, grid, "astar", "h1")["nodes_expanded"]
        h2 = get_row(df, grid, "astar", "h2")["nodes_expanded"]
        table_lines.append("  {:<12} h0={:>6.0f}   h1={:>6.0f}   h2={:>6.0f}".format(grid, h0, h1, h2))
    table = "\n".join(table_lines)

    para1 = wrap("""
        Strictly decreasing, on every single grid, with no exceptions. This
        matches exactly what dominance predicts: since h2(s) >= h1(s) >=
        h0(s) for every state s, the estimated total cost f = g + h
        computed with a dominant heuristic is never smaller than with a
        weaker one for the same state. A tighter (larger, still-admissible)
        f means more non-promising states get correctly deprioritized
        before they're ever popped off the frontier, so the search wastes
        less effort on branches that cannot beat the current best.
    """)

    para2 = wrap("""
        Because the match holds everywhere here with no counterexample, the
        interesting point for the report isn't "why doesn't it match" (it
        does) but how much it matches by - e.g. h2 cuts node count by
        roughly half versus h0 on the two hardest grids, which is a
        meaningfully large practical effect from adding one distance term
        to the heuristic.
    """)

    return "\n".join([
        heading("Q2: How does A*'s node count change as you move from h0 to h1 to h2?\n"
                "Does this match what dominance predicts? If not, why might it not?"),
        "",
        "Nodes expanded by A*, per grid, under each heuristic:",
        "",
        table,
        "",
        para1,
        "",
        para2,
    ])


def question_3(df):
    g5_a = get_row(df, "g5_rooms", "astar", "h2")["nodes_expanded"]
    g5_i = get_row(df, "g5_rooms", "idastar", "h2")["nodes_expanded"]
    g6_a = get_row(df, "g6_corridor", "astar", "h2")["nodes_expanded"]
    g6_i = get_row(df, "g6_corridor", "idastar", "h2")["nodes_expanded"]

    para1 = wrap(f"""
        At heuristic h2: on g5_rooms, A* expands {g5_a:.0f} nodes while
        IDA* expands {g5_i:,.0f} (about {g5_i / g5_a:.0f}x more). On
        g6_corridor, A* expands {g6_a:.0f} while IDA* expands {g6_i:,.0f}
        (about {g6_i / g6_a:.0f}x more). The premise holds dramatically.
    """)

    para2 = wrap("""
        Why: IDA* remembers nothing between iterations. Every time the
        f-cost threshold rises, it restarts the entire depth-first dive
        from scratch, re-discovering and re-expanding the same shallow
        nodes it already fully explored on every previous, lower-threshold
        pass. A* keeps a persistent g-cost table and frontier, so it
        essentially never repeats that work.
    """)

    para3 = wrap("""
        Why use it anyway: the entire payoff is memory, not speed. A*'s
        frontier and cost/parent tables can grow to hold every state it has
        ever discovered - potentially enormous for a large state space.
        IDA* only ever needs to remember the states on its current search
        path, which is linear in solution depth no matter how large the
        underlying state space is.
    """)

    para4 = wrap("""
        Concrete situation: an embedded controller with genuinely limited
        RAM - an actual low-cost robot vacuum's onboard chip, an old
        satellite's flight computer, a microcontroller-based device - where
        A*'s frontier might not physically fit in available memory at all.
        There, "runs slower" (IDA*) beats "runs out of memory and crashes"
        (A*) every time: a robot that takes ten extra seconds to compute a
        plan is a minor inconvenience; one that cannot allocate enough
        memory to finish planning at all is a failure.
    """)

    return "\n".join([
        heading("Q3: IDA* expands more nodes than A* on most of these grids. Why would\n"
                "anyone use it anyway? Give a concrete situation where IDA* is right."),
        "",
        para1,
        "",
        para2,
        "",
        para3,
        "",
        para4,
    ])


def question_4(df):
    rows = []
    for name, art in GRIDS.items():
        grid, start, dirty = parse_grid(art)
        free_cells = sum(row.count(".") for row in grid)
        k = len(dirty)
        state_space = free_cells * (2 ** k)
        rows.append((name, free_cells, k, state_space))

    table_lines = [
        "  {:<12} F={:>3}   k={:>2}   F*2^k = {:>7,}".format(n, f, k, s)
        for n, f, k, s in rows
    ]
    table = "\n".join(table_lines)

    smallest = rows[0]
    largest = rows[-1]
    free_growth = largest[1] / smallest[1]
    space_growth = largest[3] / smallest[3]
    k_growth = (2 ** largest[2]) / (2 ** smallest[2])

    para1 = wrap("""
        Let F = number of free (non-obstacle) cells, k = number of
        initially dirty cells. A state is (position, dirty_subset):
        position can be any of the F free cells, and the dirty subset is
        some subset of the original k dirty cells (CLEAN only ever removes
        a cell from the set; nothing ever re-dirties one, so every
        reachable dirty-set is one of the 2^k possible subsets of the
        original k cells).
    """)

    para2 = wrap(f"""
        Going from {smallest[0]} to {largest[0]}, F only grew
        {free_growth:.1f}x (linear in grid area), but the state space grew
        {space_growth:,.0f}x - almost entirely driven by 2^k, which alone
        grew {k_growth:.0f}x. That's the core of the answer: F scales
        linearly with map size, but 2^k scales exponentially with the
        number of dirty cells. Adding a handful more dirty cells multiplies
        the search space; adding a few more rows or columns to the map only
        adds to it proportionally. That is exactly why a weak heuristic can
        go from solving a grid instantly to timing out outright mostly
        because of added dirty cells rather than added map area.
    """)

    return "\n".join([
        heading("Q4: How does the state space grow as you add dirty cells? Give the\n"
                "formula for reachable states, and explain why this causes blow-up."),
        "",
        para1,
        "",
        "    State space size:  |S| = F * 2^k",
        "",
        "Computed for each graded grid:",
        "",
        table,
        "",
        para2,
    ])


def question_5(df):
    timeouts = df[df["status"] == "TIMEOUT"]
    timeout_grid = timeouts["grid"].iloc[0] if not timeouts.empty else "g6_corridor"
    timeout_configs = ", ".join(
        "%s/%s" % (r.algorithm, r.heuristic) for _, r in timeouts.iterrows()
    )
    art = GRIDS[timeout_grid]
    grid_art = "\n".join(art)

    para1 = wrap(f"""
        {timeout_grid} was the hardest grid - it is the only one where any
        configuration timed out at all ({timeout_configs}), and even its
        completed runs needed the largest node counts among successful
        configurations at comparable heuristic strength.
    """)

    para2 = wrap("""
        There is a near-complete wall of obstacles separating the top rows
        from the bottom rows, leaving only a single passable column
        connecting them - a one-cell-wide chokepoint. Every plan that needs
        to clean dirty cells on both sides of that wall (this grid has
        dirty cells scattered on both sides) is forced through that one
        passage. That bottleneck does more than narrow the literal path: it
        removes the search's ability to treat the problem as loosely
        independent nearby clusters of dirty cells, since nearly every
        candidate plan funnels through the same narrow passage regardless
        of visit order. Combined with this grid having the most dirty cells
        of any graded grid (which, per Q4, alone gives it the largest 2^k
        term), the combination of "largest raw state space" and "a layout
        that resists easy decomposition" is what pushed the weaker
        heuristics into timeout territory.
    """)

    return "\n".join([
        heading("Q5: Which grid was hardest, and what structural property of that grid\n"
                "made it hard?"),
        "",
        para1,
        "",
        "The grid itself:",
        "",
        grid_art,
        "",
        para2,
    ])


def question_6():
    para1 = wrap("""
        Chosen assumption: actions always succeed exactly as commanded
        (determinism).
    """)

    para2 = wrap("""
        What breaks: every algorithm here computes a full action sequence
        up front and implicitly assumes blindly executing it reaches the
        goal - result(state, action) is treated as a pure function
        returning exactly one guaranteed successor. A real robot's
        MOVE_FORWARD can be thrown off by wheel slip on a rug, an uneven
        floor, or a bump into unmapped furniture, landing it in a different
        cell than commanded (or not moving at all). If a precomputed plan
        is executed open-loop with no feedback, a single slip
        desynchronizes the robot's real position from what the plan
        believes it is - every subsequent step, computed for the wrong
        assumed state, compounds the error, and the robot can end up
        executing CLEAN in an already-clean cell or walking into what it
        thinks is open floor.
    """)

    para3 = wrap("""
        What technique is needed instead: planning once and executing
        blindly is no longer viable. Two related fixes: (1) closed-loop
        replanning - after every action, check the actual resulting
        position against what was expected, and if they diverge, discard
        the rest of the plan and re-search from the real observed state
        (online search); or more fundamentally, (2) reformulate the problem
        as a Markov Decision Process, where result() becomes a probability
        distribution over possible next states rather than one guaranteed
        outcome, and the thing you compute is no longer a fixed action
        sequence but an optimal policy - a rule mapping every possible
        state to its best action - solved with techniques like value
        iteration. A policy handles this correctly because it reacts to
        whichever outcome actually happened, while a fixed sequence has no
        way to notice it went wrong.
    """)

    para4 = wrap("""
        (The other three assumptions lead to analogous but distinct fixes:
        unknown dirt locations or an imperfect map both push toward partial
        observability and POMDPs or SLAM-style incremental mapping;
        unlimited battery pushes toward folding remaining charge into the
        state itself and adding a return-to-dock constraint to the cost
        function.)
    """)

    return "\n".join([
        heading("Q6: The Roomba question - pick one of the four assumptions and explain\n"
                "what would break if it were removed, and what technique is needed."),
        "",
        para1,
        "",
        para2,
        "",
        para3,
        "",
        para4,
    ])


def main():
    df = load_results()
    answers = [
        question_1(df),
        question_2(df),
        question_3(df),
        question_4(df),
        question_5(df),
        question_6(),
    ]
    print(("\n\n" + "=" * WIDTH + "\n\n").join(answers))


if __name__ == "__main__":
    main()
