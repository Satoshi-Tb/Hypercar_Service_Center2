from collections import deque

n_ops = int(input())

que = deque()
for _ in range(n_ops):
    op = input().split(" ")
    if op[0] == "DEQUEUE":
        que.popleft()
    else:
        que.append(op[1])

for n in que:
    print(n)