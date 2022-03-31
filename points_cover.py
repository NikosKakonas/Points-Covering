import itertools
import sys

# Global μεταβλητές
graph = {}
lines = []
vertical_lines = []
horizontal_lines = []
slopes = []
constats = []
s = {}
s_vertical = {}
s_horizontal = {}
s_list = []
s_list_horizontal = []
s_list_vertical = []
universe = set()

# Φτιάχνω τον γράφο
def make_the_graph(file):
    global graph
    count = -1
    with open(file, 'r') as file:
        for row in file:
            count += 1
            u = list(str(x) for x in row.split(' '))
            if '\n' in u[1]:
                u[1] = u[1][:1]
            u[0] = int(u[0])
            u[1] = int(u[1])
            graph[count] = u
    for i in range(1,len(graph)):
        for j in range(len(graph)-1,i-1,-1):
            if graph[j][0] < graph[j-1][0]:
                graph[j],graph[j-1] = graph[j-1],graph[j]
    
# Λίστα με όλες τις πιθανές γραμμές που περνάνε από όλα τα σημεία
def find_all_lines():
    global lines, slopes, constats, vertical_lines
    combs = list(itertools.combinations(graph, 2))
    for i in combs:
        y1 = graph[i[0]][1]
        y2 = graph[i[1]][1]
        x1 = graph[i[0]][0]
        x2 = graph[i[1]][0]
        if x1 != x2:
            slope = (y2 - y1) / (x2 - x1)
            c = (-1) * slope * x1 + y1
            if c > 0:
                line = 'y = ' + str(slope) + ' x + ' + str(c)
            elif c < 0:
                c = c * (-1)
                line = 'y = ' + str(slope) + ' x - ' + str(c)
                c = c * (-1)
            else:
                line = 'y = ' + str(slope) + ' x + ' + str(c)
            if line not in lines:
                lines.append(line)
                slopes.append(slope)
                constats.append(c)
                if y1 == y2:
                    horizontal_lines.append(line)
        elif y1 != y2:
            line = 'x = ' + str(x1)
            if line not in lines:
                lines.append(line)
                vertical_lines.append(line)
                slopes.append('-')
                constats.append(x1)

# Λίστα με όλα σημεία που περνάνε οι ευθείες
def total_S():
    global lines, graph, slopes, constats, s
    count = -1
    for line in lines: # lines --> λίστα με όλες τις ευθείες
        s[line] = set()
        if line in vertical_lines:
            s_vertical[line] = set()
        if line in horizontal_lines:
            s_horizontal[line] = set()
        count += 1
        for dot in graph:
            x0 = graph[dot][0]
            y0 = graph[dot][1]
            if slopes[count] != '-':
                y = slopes[count] * x0 + constats[count]
                if abs(y - y0) <= 0.0000001:
                    s[line].add(dot)
                    if line in horizontal_lines:
                        s_horizontal[line].add(dot)
            else:
                x = constats[count]
                if x == x0:
                    s[line].add(dot)
                    s_vertical[line].add(dot)
    for i in s_vertical:
        if i == set():
            del(i)
    for row in s: # φτιάχνω την s_list
        s_list.append(s[row])
    for row in s_horizontal:
        s_list_horizontal.append(s_horizontal[row])
    for row in s_vertical:
        s_list_vertical.append(s_vertical[row])

# Universe
def sets():
    global graph, universe
    for i in graph:
        universe.add(i)
    
# Εύρεση λιγότερων ευθειών (1ος Αλγόριθμος) έλεχος κάθε πιθανού υποσυνόλου
def algorithm(lista):
    result = list(itertools.chain.from_iterable(itertools.combinations(lista, r) for r in range(len(lista) + 1)))
    solution = []
    point = set()
    z = []
    for i in result:
        lst = list(i)
        for dot in graph:
            flag = False
            for i in lista:
                if dot in i:
                    flag = True
                    break
            if not flag:
                point.add(dot)
        check = set() # Έχει μέσα ενωμένα υποσύνολα
        for j in lst:
            if point != []:
                for i in point:
                    check.add(i)
            check = check | j
        if check == universe:
            solution = lst
            break
    if point != []:
        for i in graph:
            if i in point:
                z.append(graph[i][0])
                z.append(graph[i][1])
                z.append(graph[i][0] + 1)
                z.append(graph[i][1])
    ans = []
    for i in solution:
        ans.append(list(i))
    count = -1
    answer = []
    for i in ans:
        count += 1
        a = sorted(i)
        answer.append(a)
    for i in answer:
        for j in range(len(i)):
            print('(' + str(graph[i[j]][0]) + ',' + ' ' + str(graph[i[j]][1]) + ')' + ' ', end='')
        print()
    if point != []:
        count = 0
        count_ln = 0
        for i in z:
            print('(' + str(z[count]) + ',' + ' ' + str(z[count + 1]) + ')' + ' ', end='')
            count_ln += 1
            count += 2
            if count_ln % 2 == 0:
                print()
            if count == len(z):
                break


# Άπλιστος αλγόριθμος
def greedy_algorithm(lista):
    used = set()
    flag = True
    ans = []
    z = []
    while flag:
        maximum = set()
        for set1 in lista:
            f = False
            for i in set1:
                if i in used:
                    f = True
                    break
            if not f and len(set1) > len(maximum):
                maximum = set1
        k = set()
        a = True
        if maximum == set():
            for dot in graph:
                if dot not in used and a:
                    for i in lista:
                        for j in i:
                            if j == dot:
                                k = i
                                used.add(j)
                                a = False
                                ans.append(k)
                                break
            if k == set():
                for dot in graph:
                    if dot not in used:
                        z.append(graph[dot][0])
                        z.append(graph[dot][1])
                        z.append(graph[dot][0] + 1)
                        z.append(graph[dot][1])
                        used.add(dot)
        else:
            ans.append(maximum)
        for i in maximum:
            used.add(i)
        if used == universe:
            flag = False
            count = -1
            answer = []
            for i in ans:
                count += 1
                a = sorted(i)
                answer.append(a)
            for i in answer:
                for j in range(len(i)):
                    print('(' + str(graph[i[j]][0]) + ',' + ' ' + str(graph[i[j]][1]) + ')' + ' ', end='')
                print()
            # Είναι σωστό απλά να διορθώσω τα print
            if k == set():
                count = 0
                count_ln = 0
                for i in z:
                    print('(' + str(z[count]) + ',' + ' ' + str(z[count + 1]) + ')' + ' ', end='')
                    count_ln += 1
                    if count_ln % 2 == 0:
                        print()
                    count += 2
                    if count == len(z):
                        break


if __name__ == '__main__':
    file = sys.argv[len(sys.argv) - 1]
    make_the_graph(file)
    find_all_lines()
    total_S()
    sets()
    s_list_h_v = []
    for i in s_list_vertical:
        s_list_h_v.append(i)
    for i in s_list_horizontal:
        s_list_h_v.append(i)
    if len(sys.argv) == 4:
        algorithm(lista=s_list_h_v)
    elif len(sys.argv) == 3:
        parameter = sys.argv[1]
        if parameter == '-g':
            greedy_algorithm(lista=s_list_h_v)
        elif parameter == '-f':
             algorithm(lista=s_list)
    elif len(sys.argv) == 2:
        greedy_algorithm(lista=s_list)
    