
def feasible(T_sorted_asc, nt_sorted_desc, k):
    b = [0]*k
    it, int_ = 0, 0
    while it + int_ < total:
        m = min(b)
        if b[0] == m:
            # bin 0 is at min
            if it < len(T):
                b[0] += T[it]; it += 1
            else:
                # need to add nt
                if b.count(m) == 1:  # bin 0 unique min
                    return False
                # add nt to another min
                ...
        else:
            # bin 0 not min, add nt to some min
            if int_ >= len(nt): return False  # shouldn't happen if total right
            # add nt to a min bin
            ...
