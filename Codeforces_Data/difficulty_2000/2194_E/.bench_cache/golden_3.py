import sys
input=sys.stdin.readline

def solve():
    n,m=map(int,input().split())
    a=[list(map(int,input().split())) for _ in range(n)]
    NEG=float('-inf')
    f=[[0]*m for _ in range(n)]
    g=[[0]*m for _ in range(n)]
    f[0][0]=a[0][0]
    for j in range(1,m): f[0][j]=f[0][j-1]+a[0][j]
    for i in range(1,n):
        f[i][0]=f[i-1][0]+a[i][0]
        for j in range(1,m):
            f[i][j]=max(f[i-1][j],f[i][j-1])+a[i][j]
    g[n-1][m-1]=a[n-1][m-1]
    for j in range(m-2,-1,-1): g[n-1][j]=g[n-1][j+1]+a[n-1][j]
    for i in range(n-2,-1,-1):
        g[i][m-1]=g[i+1][m-1]+a[i][m-1]
        for j in range(m-2,-1,-1):
            g[i][j]=max(g[i+1][j],g[i][j+1])+a[i][j]
    # for each diagonal d=i+j, collect v
    diag_max1={}
    diag_max2={}
    diag_count1={}
    for i in range(n):
        for j in range(m):
            d=i+j
            v=f[i][j]+g[i][j]-a[i][j]
            if d not in diag_max1:
                diag_max1[d]=v
                diag_max2[d]=NEG
                diag_count1[d]=1
            else:
                if v>diag_max1[d]:
                    diag_max2[d]=diag_max1[d]
                    diag_max1[d]=v
                    diag_count1[d]=1
                elif v==diag_max1[d]:
                    diag_count1[d]+=1
                elif v>diag_max2[d]:
                    diag_max2[d]=v
    ans=float('inf')
    for i in range(n):
        for j in range(m):
            d=i+j
            v=f[i][j]+g[i][j]-a[i][j]
            through_flip=v-2*a[i][j]
            if v==diag_max1[d]:
                if diag_count1[d]>1:
                    avoid=diag_max1[d]
                else:
                    avoid=diag_max2[d]
            else:
                avoid=diag_max1[d]
            res=max(through_flip,avoid)
            if res<ans: ans=res
    print(ans)

t=int(input())
for _ in range(t): solve()
