'''
given two permutations, see if removing the tail or front end of either n-1 times make a[0]=b[0]

if the front or tail end of a isnt one of the front or tail ends of b, then alice wins
we dont need to play optimally, just shave off both a[0], a[-1] and b[0], b[-1]

2 1 3
1 3 4

'''
t = int(input())

while t:
    n = int(input())
    a=list(map(int, input().split()))
    b=list(map(int, input().split()))
    
    turns = 0
    
    alicePrinted=False
    while turns<n-1:
        #print(a,b)
    
        b_turns = set()
        b_turns.add(b[0])
        b_turns.add(b[-1])
        
        if a[0] not in b_turns or a[-1] not in b_turns:
            print('Alice')
            alicePrinted=True
            break
        else:
            b.pop()
            b.pop(0)
            a.pop()
            a.pop(0)
            
            turns+=2
    
    if not alicePrinted:
        print('Bob')
    
    t-=1