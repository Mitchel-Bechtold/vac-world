"""
CS3810 Mini-Project 1 - Part 3: Heuristics (25 points, +10 bonus)
=================================================================

Every heuristic takes (state, problem) and returns a NUMBER: an estimate of
the remaining cost to clean all remaining dirty cells. Keep the signature
even where you do not need `problem` - the search functions call them all
the same way.

Remember what the cost model is. Every move costs 1 AND every CLEAN costs 1,
so a state with k dirty cells remaining always costs at least k. A heuristic
that forgets the CLEAN actions is admissible but weak.

Writing the code is the small half of this part. The report must argue that
h1 and h2 are admissible: say exactly what lower bound each one computes and
why the true remaining cost can never be smaller than it.
"""


def manhattan(a, b):
    """Return the Manhattan distance between two (row, col) positions.

    Note for your admissibility argument: on this grid, the true number of
    moves between two cells is ALWAYS at least their Manhattan distance.
    Obstacles can only force a detour, never a shortcut.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def h0(state, problem):
    """The zero heuristic.

    Always returns 0. This is not a throwaway: with h(n) = 0, A* degenerates
    into uniform-cost search, which is your experimental baseline for "what
    does an uninformed optimal search cost?"
    """
    return 0


def h1(state, problem):
    """Number of dirty cells remaining.

    Admissible because each remaining dirty cell needs at least its own
    CLEAN action, and CLEAN costs 1.
    """
    _, dirty = state
    return len(dirty)


def h2(state, problem):
    """Dirty cells remaining + Manhattan distance to the NEAREST dirty cell.

    Returns 0 when nothing is dirty.

    For the report: explain why adding the distance term keeps the estimate
    a lower bound - the robot must reach at least one dirty cell before it
    can clean anything, and reaching the nearest one is the cheapest way to
    do that.
    """
    pos, dirty = state
    if not dirty:
        return 0
    nearest = min(manhattan(pos, cell) for cell in dirty)
    return len(dirty) + nearest


def h3(state, problem):
    """YOUR heuristic (optional, up to 10 bonus points).

    To earn the bonus it must be:
      1. Admissible - never overestimates the true remaining cost. You must
         argue this in the report. An inadmissible heuristic that finds
         short paths quickly is a different algorithm, not a better
         heuristic, and earns nothing.
      2. Dominant over h2 - h3(s) >= h2(s) for every state s.
      3. Supported by data - show the node counts next to h2's.

    If you are not attempting the bonus, leave this raising NotImplementedError
    and run_tests.py will skip it.

    A place to start thinking: h2 only ever looks at one dirty cell. After
    the robot reaches that cell it still has to get to all the others. What
    is a cheap-to-compute lower bound on THAT remaining travel?
    """
    pos, dirty = state
    if not dirty:
        return 0
    nearest = min(manhattan(pos, cell) for cell in dirty)
    spanning = _mst_weight(dirty)
    return len(dirty) + nearest + spanning


def _mst_weight(points):
    """Return the weight of a minimum spanning tree over `points`, using
    Manhattan distance as the edge weight (Prim's algorithm, O(n^2)).

    For the report: visiting every point in a connected sequence always
    costs at least the MST weight of those points - you cannot touch all
    of them while covering less total distance than the cheapest way to
    connect them. Since Manhattan distance never overestimates a real move
    on this grid (see `manhattan`'s docstring), an MST built from Manhattan
    distances never overestimates the real MST either, so this stays a
    valid lower bound on the travel still needed once the robot arrives at
    the first dirty cell.

    n is at most 9 on the graded grids, so O(n^2) is effectively instant -
    no need for a fancier MST algorithm here.
    """
    points = list(points)
    if len(points) <= 1:
        return 0

    in_tree = {points[0]}
    best_dist = {p: manhattan(points[0], p) for p in points[1:]}
    total = 0

    while len(in_tree) < len(points):
        # Pick the point outside the tree that is closest to some point
        # already inside it - the standard Prim's-algorithm step.
        next_point = min(best_dist, key=best_dist.get)
        total += best_dist.pop(next_point)
        in_tree.add(next_point)
        for p in best_dist:
            d = manhattan(next_point, p)
            if d < best_dist[p]:
                best_dist[p] = d

    return total


# Used by experiments.py and run_tests.py. Do not rename.
HEURISTICS = {'h0': h0, 'h1': h1, 'h2': h2, 'h3': h3}
