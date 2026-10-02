# 1. DFS expands far fewer nodes than A*, yet returns much worse solutions — explain both halves.

# Fewer nodes: DFS has no notion of "better" or "worse" — 
# it commits to one branch, follows it to completion, and 
# stops at the very first sequence of actions that reaches 
# the goal, full stop. It never backtracks to compare 
# alternatives once something works. On g6_corridor, 
# DFS expanded only 195 nodes versus A*/h0's 10,873 — 
# it simply didn't need to look at most of the reachable 
# state space before stumbling onto some working path.

# Worse solutions: that's the exact same mechanism causing 
# the exact same result. Because DFS stops the instant it 
# finds anything that works, whatever path the fixed action 
# order (MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, CLEAN) 
# happens to walk it down first is what you get — however 
# circuitous. On that same corridor grid, DFS's plan cost 
# 121 actions against a true optimum of 32 — nearly 4x longer. 
# The two halves aren't separate phenomena; they're the same 
# cause seen from two angles: no cost-awareness means cheap-to-stop 
# and low-quality-when-stopped are the same coin.

# 2. How does A*'s node count change h0→h1→h2? Does this match dominance?

# grid	h0	h1	h2
# g1_tiny	21	20	13
# g2_open	98	96	76
# g3_blocks	411	331	256
# g4_pillars	1160	850	510
# g5_rooms	2403	2097	1651
# g6_corridor	10873	7665	5797

# Strictly decreasing, on every single grid, no exceptions. 
# This is exactly what dominance predicts: since 
# h2(s) >= h1(s) >= h0(s) for every state s, the estimated 
# total cost f = g + h using a dominant heuristic is never 
# smaller than using a weaker one for the same state. 
# A tighter (larger but still admissible) f means more 
# non-promising states get correctly deprioritized before 
# they're ever popped off the frontier — the search wastes 
# less effort on branches that can't beat the current best.

# 3. IDA* expands more nodes than A* on most grids — why use it anyway? Give a concrete situation.

# At h2: g5_rooms — A* expands 1,651 nodes; IDA* expands 
# 731,040 (about 440x more). g6_corridor — A* expands 5,797; 
# IDA* expands 9,126,492 (about 1,575x more). The premise holds dramatically.

# Why: IDA* remembers nothing between iterations. Every time 
# the f-cost threshold rises, it restarts the entire depth-first 
# dive from scratch, re-discovering and re-expanding the same 
# shallow nodes it already fully explored on every previous pass. 
# A* keeps a persistent g-cost table and frontier, 
# so it essentially never repeats that work.

# Why use it anyway: the whole payoff is memory, not speed. 
# A*'s frontier and cost tables can grow to hold every state 
# it's ever discovered — potentially enormous. IDA* only ever
# linear in solution depth, regardless of how large the state space is. 
# A concrete situation: an embedded controller with genuinely 
# limited RAM — an actual low-cost robot vacuum's onboard chip, 
# an old satellite's flight computer, a microcontroller — 
# where A*'s frontier might not physically fit in available memory at all. 
# There, "runs slower" (IDA*) beats "crashes or can't allocate" 
# (A*) every time; a robot that takes an extra ten seconds to 
# compute a plan is a minor inconvenience, one that runs out of 
# memory mid-computation is a failure.

# 4. Formula for the number of reachable states; why this makes search "blow up."

# Let F = number of free (non-obstacle) cells, 
# k = number of initially dirty cells. A state is (position, dirty_subset). 
# Position can be any of the F free cells. 
# The dirty subset is some subset of the original k dirty cells — 
# since CLEAN only ever removes a cell from the set and nothing 
# ever re-dirties a cell, every reachable dirty-set is one of 
# the 2^k possible subsets of the original k cells.

# 5. Which grid was hardest, and what structural property made it hard?

# g6_corridor, clearly — it's the only grid where anything timed out 
# at all (idastar+h0 and idastar+h1 both hit the 60-second cap), 
# and even its completed runs needed the largest node counts 
# among successful configurations at comparable heuristic strength

# Structural property: look at the grid art —

# R.D..D
# .D....
# #####.
# D..D..
# .D#.D.
# D..#.D

# Row index 2 is a wall of obstacles (#####.) spanning five of six columns — 
# the only passable connection between the top two rows and the 
# bottom three rows is the single cell at column 5. Every plan 
# that needs to clean dirty cells on both sides of that wall 
# (and this grid has dirty cells scattered on both sides) is 
# forced through that one-cell chokepoint. That bottleneck 
# doesn't just narrow the literal path — it removes the search's 
# ability to treat the problem as loosely independent nearby 
# clusters; nearly every plan funnels through the same narrow 
# passage regardless of which order the dirty cells get visited in, 
# so there's less structure for a heuristic to exploit to 
# tell "genuinely different" plans apart early. Combine that with 
# having the most dirty cells of any graded grid (9, giving the 
# largest 2^k term per question 4), and you get both the largest 
# raw state space and a layout that resists easy decomposition — 
# that combination is what pushed it into timeout 
# territory specifically for the weaker heuristics.

# 6. The Roomba question.

# What breaks: every algorithm here computes an entire action 
# sequence up front and implicitly assumes blindly executing 
# it gets you to the goal — result(state, action) is a pure 
# function returning exactly one guaranteed successor. A real 
# robot's MOVE_FORWARD can be thrown off by wheel slip on a rug, 
# an uneven floor, or a bump into unmapped furniture, landing it 
# in a different cell than commanded (or not moving at all). If you 
# execute a precomputed plan open-loop with no feedback, one slip 
# desynchronizes the robot's real position from what the plan believes — 
# every subsequent step, computed for the wrong assumed state, 
# compounds the error, and the robot can end up executing 
# CLEAN in an already-clean cell or walking into what it thinks is open floor.

# What technique is needed instead: you can no longer plan once and execute blindly. 
# Two related fixes: (1) closed-loop replanning — after every action, 
# check the actual resulting position against what was expected, 
# and if they don't match, discard the remaining plan and re-search 
# from the real observed state (online search); or more fundamentally, 
# (2) reformulate the whole problem as a Markov Decision Process — 
# result becomes a probability distribution over possible next 
# states rather than one guaranteed outcome, and the thing you 
# compute is no longer a fixed action sequence but an optimal 
# policy (a rule mapping every possible state to its best action), 
# solved with techniques like value iteration. A policy handles 
# this correctly because it reacts to whichever outcome actually happened, 
# while a fixed sequence has no way to notice it went wrong.