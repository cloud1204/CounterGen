
def solve(j, t):
    # returns (tom_wins, min_moves) where Tom plays optimally to win then minimize moves, Jerry plays optimally to make Tom lose, or if forced to lose, maximize moves
    if j == n: return (False, 0)  # Jerry already won
    ...
