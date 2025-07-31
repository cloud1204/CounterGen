for _ in range(int(input())):
  n = int(input())
  a = list(map(int,input().split()))
  b = list(map(int,input().split()))
  if a==b or a==list(reversed(b)):
    print("Bob")
  else:
    print("Alice")