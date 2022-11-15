# will be using A* algoritm

import math
import numpy as np
import time

t1 = time.perf_counter()

# checks if node exists
def exists(img, x, y, width, height):
    if x < width and x >= 0 and y < height and y >= 0:
        return True
    else:
        return False


# checks if the node is traversable
def is_traversable(img, x, y):
    r = img[y][x][0]
    g = img[y][x][1]
    b = img[y][x][2]
    # white and green path
    if r >= 250 and g >= 250 and b >= 250:
        return True
    if r < 10 and g > 220 and b < 10:
        return True
    else:
        return False


# checks if the destination has been reached
def is_destination(img, x, y, ending_position):
    if x == ending_position[0] and y == ending_position[1]:
        return True
    else:
        return False


# calculates heuristics (diagonal)
def heuristics(img, x, y, ending_position):
    # getting V/H distance
    r = img[y][x][0]
    g = img[y][x][1]
    b = img[y][x][2]
    if r >= 250 and g >= 250 and b >= 250:
        d1 = 100  # 1 * 10
        x_end = ending_position[0]
        y_end = ending_position[1]
        x_distance = abs(x - x_end)
        y_distance = abs(y - y_end)

        # getting diagonal distance
        d2 = 140  # sqrt(2) * 10
        diag_distance = abs(x_distance - y_distance)
        #diag_distance = math.sqrt(x_distance * x_distance + y_distance * y_distance)
        h = min(x_distance, y_distance) * d1 + diag_distance * d2

        #diag_distance = math.sqrt(x_distance * x_distance + y_distance * y_distance)
        #h = (x_distance + y_distance) * d1 + diag_distance * d2

        #h = (x_distance + y_distance) * d1 + min(x_distance, y_distance) * (d2 - 2 * d1)

    elif r < 10 and g > 220 and b < 10:
        d1 =1  # 1 * 10
        x_end = ending_position[0]
        y_end = ending_position[1]
        x_distance = abs(x - x_end)
        y_distance = abs(y - y_end)

        # getting diagonal distance
        d2 = 1.4 # sqrt(2) * 10
        #diag_distance = math.sqrt(x_distance * x_distance + y_distance *y_distance)
        diag_distance = abs(x_distance - y_distance)
        h = min(x_distance, y_distance) * d1 + diag_distance * d2

        #h = (x_distance+ y_distance) * d1 + diag_distance * d2

        #h = (x_distance + y_distance) * d1 +min(x_distance, y_distance) *(d2 - 2 * d1)

    return h


# finds the optimized path using the parent coords in node details
# sets the path to the color green
# sets the start and end to the color red
def print_path(img, starting_position, ending_position, path_color, node_details):
    endpoint_color = (255, 0, 0)
    start_x = starting_position[0]
    start_y = starting_position[1]
    end_x = ending_position[0]
    end_y = ending_position[1]
    parent_x = node_details[end_x][end_y][3]
    parent_y = node_details[end_x][end_y][4]
    img[parent_y][parent_x] = path_color
    img[parent_y+1][parent_x+1] = path_color
    img[parent_y+1][parent_x-1] = path_color
    img[parent_y-1][parent_x-1] = path_color
    img[parent_y-1][parent_x+1] = path_color
    img[parent_y + 1][parent_x ] = path_color
    img[parent_y ][parent_x - 1] = path_color
    img[parent_y - 1][parent_x ] = path_color
    img[parent_y ][parent_x + 1] = path_color

    # will loop until the parent x and y are the starting position
    while True:
        if parent_x == start_x and parent_y == start_y:
            img[start_y][start_x] = endpoint_color
            img[end_y][end_x] = endpoint_color
            return

        # getting the parent coords and then setting the coords to the path color
        temp_x = parent_x
        temp_y = parent_y
        parent_x = node_details[temp_x][temp_y][3]
        parent_y = node_details[temp_x][temp_y][4]
        img[parent_y][parent_x] = path_color
        img[parent_y + 1][parent_x + 1] = path_color
        img[parent_y + 1][parent_x - 1] = path_color
        img[parent_y - 1][parent_x - 1] = path_color
        img[parent_y - 1][parent_x + 1] = path_color
        img[parent_y + 1][parent_x] = path_color
        img[parent_y][parent_x - 1] = path_color
        img[parent_y - 1][parent_x] = path_color
        img[parent_y][parent_x + 1] = path_color


# A* alg
def find(img,  width, height, starting_position, ending_position, path_color):

    # if the user chose the starting and ending position to be the same
    if is_destination(img, starting_position[0], starting_position[1], ending_position):
        print("The starting and ending position you have chosen is the same.")
        print("Exiting program.")
        exit()


    # creating a list to hold the f, g, and h-values and the parent coords for each node
    # 5 for f, g, h values and parent x, y values
    node_details = np.full((width, height, 5), -1)

    # create a 2D-list that marks all nodes that have been evaluated by 1, 0 if not
    closed_list = np.zeros((width, height))

    # creating an open list that will contains nodes with calculated f costs
    # each index will contain: [f, [x, y]]
    open_list = []

    # putting the starting position in open list with its f as 0
    open_list.append([0, [starting_position[0], starting_position[1]]])

    while len(open_list) != 0:
        # set current equal to node with the lowest f-value
        if len(open_list) == 1:
            current = open_list[0]
        else:
            current = open_list[0]
            for node in open_list:
                node_x = node[1][0]
                node_y = node[1][1]
                cur_x = current[1][0]
                cur_y = current[1][1]

                if node[0] < current[0]:
                    current = node
                # if f-values are equal
                elif node[0] == current[0]:
                    # setting current equal to node if the h-value is lower
                    node_h = node_details[node_x][node_y][2]
                    current_h = node_details[cur_x][cur_y][2]
                    if node_h < current_h:
                        current = node

                        # current node coords vars
        cur_x = current[1][0]
        cur_y = current[1][1]

        r = img[cur_y][cur_x][0]
        g = img[cur_y][cur_x][1]
        b = img[cur_y][cur_x][2]

        # removing current node from open list
        open_list.remove(current)

        # marking node as 1 in closed list
        closed_list[cur_x][cur_y] = 1

        # checking if current node is the destination
        if is_destination(img, cur_x, cur_y, ending_position):
            print("Path was successfully found.")
            print_path(img, starting_position, ending_position, path_color, node_details)
            return

        # getting the neighbor nodes// 8 neighbors
        else:
            neighbor_list = [(cur_x - 1, cur_y), (cur_x + 1, cur_y), (cur_x, cur_y + 1), (cur_x, cur_y - 1),
                             (cur_x - 1, cur_y + 1), (cur_x - 1, cur_y - 1), (cur_x + 1, cur_y + 1),
                             (cur_x + 1, cur_y - 1)]
            direction_counter = 0

            for neighbor in neighbor_list:
                # neighbor node x and y vars
                n_x = neighbor[0]
                n_y = neighbor[1]




                # check that neighbor exists, is traversable and is marked as 0 in closed list
                if (exists(img, n_x, n_y, width, height) and is_traversable(img, n_x, n_y) and  closed_list[n_x][n_y] == 0):

                    # checking if current node is starting position in order to get right value g
                    if current[1] == starting_position:
                        if direction_counter <= 3 and r >= 250 and g >= 250 and b >= 250:
                            g = 100

                        elif direction_counter > 3 and r >= 250 and g >= 250 and b >= 250:
                           g = 140

                        elif direction_counter <= 3  and  r < 10 and g > 220 and b < 10:
                            g = 1

                        else:
                           g = 1.4
                    else:
                        if direction_counter <= 3 and r >= 250 and g >= 250 and b >= 250:
                            g = node_details[cur_x][cur_y][1] + 100


                        elif direction_counter > 3 and r >= 250 and g >= 250 and b >= 250:
                           g = node_details[cur_x][cur_y][1] + 140

                        elif direction_counter <= 3 and  r < 10 and g > 220 and b < 10:
                            g = node_details[cur_x][cur_y][1] + 1

                        else:
                            g = node_details[cur_x][cur_y][1] + 1.4

                    # getting other values
                    h = heuristics(img, n_x, n_y, ending_position)
                    print(h)
                    f = g + h
                    print(g)
                    print(f)

                    # checking if neighbor needs to be updated
                    # checking if f-cost to neighbor is shorter or if neighbor not in open list
                    update = True
                    in_open = False
                    index = -1
                    count = 0
                    for node in open_list:
                        node_f = node[0]
                        node_x = node[1][0]
                        node_y = node[1][1]
                        if n_x == node_x and n_y == node_y:
                            in_open = True
                            index = count
                            if f >= node_f:
                                update = False
                        count += 1

                    # update node_details and updating open list
                    if update == True:
                        # storing details in node details
                        node_details[n_x][n_y][0] = f
                        node_details[n_x][n_y][1] = g
                        node_details[n_x][n_y][2] = h
                        node_details[n_x][n_y][3] = cur_x
                        node_details[n_x][n_y][4] = cur_y

                        # if neighbor is not in open, then append neighbor, else just update f-value
                        if in_open == False:
                            open_list.append(([f, [n_x, n_y]]))
                        else:
                            open_list[index][0] = f

                direction_counter += 1
               # print( direction_counter )
               # print(f)

    print("Path was not found. Exiting program.")
    exit()
