import math

def envies(val1, pay1, pay2):
    a = max(val1[0], pay2[0])
    b = min(val1[1], pay2[1])
    return b - a > pay1[1]-pay1[0] + 0.000001


def check_for_envy(intervals, final_cuts):
    n = len(intervals)
    for i in range(n):
        for start, end, person in intervals:
            if person == i:
                val = [start/10**9, end/10**9]
                break
        for k in range(n):
            if final_cuts[k][1] == i:
                pay1 = [0 if k == 0 else final_cuts[k - 1][0], final_cuts[k][0]]
        for j in range(n):
            for k in range(n):
                if final_cuts[k][1] == j:
                    pay2 = [0 if k == 0 else final_cuts[k - 1][0], final_cuts[k][0]]
            if envies(val, pay1, pay2):
                print(1 + i, 1 + j, val, pay1, pay2)

n = int(input())
error = 0.0001
intervals = [[int(float(x)*10**9) for x in input().split(" ")]+[i] for i in range(n)]
intervals.sort()
end_points = {}
for (start, end, person) in intervals:
    end_points[person] = [start, end]
pieces = [[a, a, i] for (a, b, i) in intervals]

final_cuts = []
deleted_parts = [False for _ in range(n)]
while len(pieces) > 0:
#    print(pieces)
#    print(final_cuts)
#    input()
    increase_len = 100*10**9
    no_interval_removed = False
    count = 1
    for i in range(len(pieces)):
        start, end, person = pieces[i]
        if i > 0 and pieces[i-1][1] + error >= start:
            count += 1
        else:
            count = 1
        if (end_points[person][1] - end) / count < increase_len:
            no_interval_removed = False
            increase_len = math.ceil((end_points[person][1] - end) / count)
        if i+1 < len(pieces) and end < pieces[i+1][0]:
            if (pieces[i + 1][0] - end) / count < increase_len:
                no_interval_removed = True
                increase_len = math.ceil((pieces[i + 1][0] - end) / count)
    for i in range(len(pieces)):
        pieces[i][1] += increase_len
        if i+1 < len(pieces) and pieces[i+1][0] <= pieces[i][1]:
            delta = pieces[i+1][1] - pieces[i+1][0]
            pieces[i+1][0] = pieces[i][1]
            pieces[i+1][1] = pieces[i][1] + delta
    if no_interval_removed and increase_len > error:
        continue
    i = len(pieces)
    while i > 0:
        i -= 1
        if pieces[i][1] + error >= end_points[pieces[i][2]][1]:
            union_end = pieces[i][1]
            j = i
            while j > 0 and pieces[j-1][1] + error >= pieces[j][0]:
                j -= 1
            union_start = pieces[j][0]
            for k in range(i, j-1, -1):
                final_cuts.append((pieces[k][1]/10**9, pieces[k][2]))
                deleted_parts[k] = True
            i = j
            for j in range(len(pieces)):
                if pieces[j][0] < union_start:
                    end_points[pieces[j][2]][1] = min(end_points[pieces[j][2]][1], union_start)
                if pieces[j][1] > union_end:
                    end_points[pieces[j][2]][0] = max(end_points[pieces[j][2]][0], union_end)
    pieces = [pieces[k] for k in range(len(pieces)) if not deleted_parts[k]]
    deleted_parts = [False for _ in range(len(pieces))]

final_cuts.sort()
#check_for_envy(intervals, final_cuts)
print(" ".join(str(x) for (x, _) in final_cuts[:-1]))
print(" ".join(str(x+1) for (_, x) in final_cuts))
