from collections import deque
n_logs = int(input())

tasks = deque()

for _ in range(n_logs):
    issue = input().split(" ")
    if issue[0] == "SOLVED":
        tasks.popleft()
    else:
        tasks.append(issue[1])

for t in tasks:
    print(t)
