from collections import deque

students_que = deque()

n_students = int(input())

for _ in range(n_students):
    action = input().split(" ")

    if action[0] == "READY":
        students_que.appendleft(action[1])
    elif action[0] == "EXTRA":
        s = students_que.pop()
        students_que.appendleft(s)
    else:
        print(students_que.pop())
