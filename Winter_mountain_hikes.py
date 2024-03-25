from collections import deque
import random

min_huts_count = 99
max_huts_count = 100
min_altitude = 0
max_altitude = 8848

# The function takes input from the user regarding the number of mountain shelters,
# trails, and the maximum altitude that Professor cannot exceed.
# Output: huts_number - number of mountain huts,
#         hiking_trail_number - number of mountain trails,
#         reachable_altitude - the maximum altitude that Professor cannot exceed.
def get_map_parameters_from_keyboard():

    huts_number = int(input("Enter the number of shelters "))

    # Checking if the user has not provided too many mountain trails
    while huts_number <= 0:
        print("There must be at least one shelter!")
        huts_number = int(input("Please enter the number of shelters "))

    hiking_trail_number = int(input("Enter the number of trails "))

    while hiking_trail_number < 0:
        print("The number of trails must be non-negative")
        huts_number = int(input("Enter the number of trails "))

    max_hiking_trail = int(huts_number * (huts_number - 1) / 2)

    # Checking if the user has not provided too many mountain trails
    while hiking_trail_number > max_hiking_trail:
        print("Too many hiking trails!\n"
              f"Remember, there can be a maximum of {max_hiking_trail} bidirectional hiking trails ")
        hiking_trail_number = int(input("Enter the number of trails "))

    reachable_altitude = int(input("Enter the maximum altitude above sea level that the professor can reach "))

    return huts_number, hiking_trail_number, reachable_altitude

# The function randomizes the parameters when the user chooses not to provide them
# Output: huts_number - number of mountain huts,
#         hiking_trail_number - number of mountain trails,
#         reachable_altitude - the maximum altitude that Professor cannot exceed
def get_map_parameters_randomly():

    huts_number = random.randint(min_huts_count, max_huts_count)
    hiking_trail_number = random.randint(1, int(huts_number * (huts_number - 1) / 2))
    reachable_altitude = round(random.uniform(min_altitude, max_altitude), 3)

    return huts_number, hiking_trail_number, reachable_altitude

# The function searches for a pair of two points in the matrix
# Input: matrix - the matrix in which rows with [a, b] or [b, a]
#                 in the first two columns will be searched for
#        a,b - searching for values in the matrix
# Output: True or False
def check_for_pair(matrix, a, b):

    for row in matrix:
        if a == row[0] and b == row[1]:
            return True
    return False

# The function compares two values, 'a' and 'b', with the value 'c'
# Input: a, b - values to be compared with the value 'c'
#        c - the value against which the other numbers are compared
# Output: True or False
def less_than(a, b, c):

    if c >= a >= 0 and c >= b >= 0:
        return True
    else:
        return False

# The function reads a matrix from the user with 3 columns:
# [from which hut we depart, to which hut we are going,
# maximum altitude of the trail between huts]
# Input: huts_number - number of mountain huts
#        hiking_trail_number - number of mountain trails
# Output: matrix (3 x hiking_trail_number)
def matrix_from_keyboard(huts_number, hiking_trail_number):

    matrix = [[-1 for column in range(3)] for row in range(hiking_trail_number)]

    i = 0
    while i < hiking_trail_number:

        # Reading subsequent rows from the console
        row = list(map(int, input().split()))
        row[0] = row[0] - 1
        row[1] = row[1] - 1

        # Checking user inputs
        if less_than(row[0], row[1], huts_number - 1) is not True:
            print("You've entered a shelter that doesn't exist! Remember, we start from 1,"
                  f" and there are {huts_number} shelters.")
        elif row[0] == row[1]:
            print("You cannot route a trail directly back to the same shelter!")
        elif check_for_pair(matrix, row[0], row[1]) is True or\
                check_for_pair(matrix, row[1], row[0]) is True:
            print("A trail already exists between these shelters!")
        else:
            matrix[i] = row
            i += 1

    return matrix

# The function generates a matrix with 3 columns:
# [from which hut we depart, to which hut we are going,
# maximum altitude of the trail between huts]
# Input: huts_number - number of mountain huts
#        hiking_trail_number - number of mountain trails
# Output: matrix (3 x hiking_trail_number)
def matrix_randomly(huts_number, hiking_trail_number):
    matrix = [[-1 for column in range(3)] for row in range(hiking_trail_number)]

    # Maximum number of mountain hut pairs
    max_pairs = int(huts_number * (huts_number - 1) / 2)

    pair_huts = [[-1, -1] for i in range(0, max_pairs)]

    # List of all possible connections between mountain huts
    index = 0
    for i in range(0, huts_number):
        for j in range(i+1, huts_number):
            pair_huts[index] = [i, j]
            index += 1

    i = 0
    while i < hiking_trail_number:
        # Randomizing a pair of mountain huts with a hiking trail between them
        choice_huts = random.choice(pair_huts)

        # Adding mountain hut pairs to a matrix and randomly drawing
        # the maximum elevation of a mountain trail between them
        matrix[i] = [choice_huts[0], choice_huts[1], round(random.uniform(min_altitude, max_altitude), 3)]
        i += 1

        # Removing the pair of mountain huts with a hiking trail between them
        pair_huts.remove(choice_huts)

    return matrix

# This function creates a graph representing connections between mountain
# huts based on a matrix containing information about pairs of huts and
# the maximum altitude of mountain trails between them.
# Input: matrix - [from which hut we depart, to which hut we are going,
#                  maximum altitude of the trail between huts],
#        huts_number - number of mountain huts
# Output: graph
def dictionary_graph(matrix, huts_number):
    graph = [deque() for i in range(0, huts_number)]
    for line in matrix:
        hut_1 = line[0]
        hut_2 = line[1]
        altitude = line[2]
        graph[hut_1].append((hut_2, altitude))
        graph[hut_2].append((hut_1, altitude))
    return graph


def bfs(graph, start_node, max_height):
    # List of visited nodes
    visited = [False for i in range(0, len(graph))]

    # Queue necessary for graph traversal algorithm
    queue = deque()

    # Adding the first element to the queue
    queue.append(start_node)
    # The first element is already visited
    visited[start_node] = True

    while queue:
        node = queue.pop()
        for neighbour in graph[node]:
          if neighbour[1] <= max_height and visited[neighbour[0]] is False:
            visited[neighbour[0]] = True
            queue.append(neighbour[0])

    return visited

while True:
    # The beginning of the program where the user is asked about data randomization
    print("Plan a map of mountain trails for Professor Baltazar's travels.")
    decision_1 = int(input("Choose 1 if you want full control over the number of shelters and the trails connecting them."
                        "\nBy entering 0, you relinquish full control over Baltazar's journey to random numbers "))

    if decision_1 == 1:

        huts_number, hiking_trail_number, reachable_altitude = get_map_parameters_from_keyboard()

        print("\nYour task now is to enter shelters connected by bidirectional trails.\n"
              "The altitude of the trail matters, don't forget about it!\n"
              "\nDo you still want to have control over Baltazar's journey?")
        decision_2 = int(input("Choose 1 if you still want to have control.\n"
                               "By entering 0, you relinquish full control over Baltazar's journey to random numbers "))
        if decision_2 == 1:
            print("\nEnter values in the format: the number of the shelter you're departing from, the number of the"
                  " shelter you're heading to, and the maximum altitude of the trail connecting them. \n"
                  "Example: We're going from shelter 1 to 2, and the maximum altitude is 1200 meters above sea level. Enter in the console: 1 2 1200 \n"
                  "Remember to separate consecutive values with just a space!")
            matrix_trails = matrix_from_keyboard(huts_number, hiking_trail_number)
        elif decision_2 == 0:
            matrix_trails = matrix_randomly(huts_number, hiking_trail_number)
        else:
            raise Exception("You didn't select either 0 or 1. You have only 2 options! Start the hike again!")
    elif decision_1 == 0:
        huts_number, hiking_trail_number, reachable_altitude = get_map_parameters_randomly()
        matrix_trails = matrix_randomly(huts_number, hiking_trail_number)
    else:
        raise Exception("You didn't select either 0 or 1. You have only 2 options! Start the hike again!")

    graph = dictionary_graph(matrix_trails, huts_number)
    visited = bfs(graph, 0, reachable_altitude)

    if decision_1 == 0 or (decision_1 == 1 and decision_2 == 0):
        decision_3 = int(input(
            "\nChoose 1 if you want to print the matrix of all trails along with their maximum altitudes."
            "\nBy entering 0, you skip this procedure. "))
        if decision_3 == 1:
            for line in matrix_trails:
                line[0] += 1
                line[1] += 1
                print(f"{line}", end="\n")

    print("Here is the list of shelters where Professor Baltazar can plan his trip:")
    for i in range(0, len(visited)):
        if visited[i] is True:
            print(f"{i+1} ", end="")

    input("\nPress Enter to continue")