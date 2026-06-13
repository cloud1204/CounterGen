
lcp = np.zeros((n+1, n+1), dtype=np.int32)
for i in range(n-1, -1, -1):
    for j in range(n-1, -1, -1):
        if T[i]==T[j]:
            lcp[i][j] = lcp[i+1][j+1]+1
