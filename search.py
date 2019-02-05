# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
# Modified by Rahul Kunji (rahulsk2@illinois.edu) on 01/16/2019

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""


# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)
import queue, math, sys, copy
def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod)(maze)


def bfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    start = maze.getStart()
    to_visit = queue.Queue()
    to_visit.put(start)
    visited = []
    path = []
    path_tracker = {start: None}
    num_states_explored = 0
    end_state = (0, 0)

    while to_visit:
        curr_state = to_visit.get()

        if curr_state not in visited:

            visited.append(curr_state)
            num_states_explored += 1

            if maze.isObjective(curr_state[0], curr_state[1]):
                end_state = curr_state
                break

            neighbors = maze.getNeighbors(curr_state[0], curr_state[1])
            for neighbor in neighbors:
                if neighbor not in visited and maze.isValidMove(neighbor[0], neighbor[1]):
                    to_visit.put(neighbor)
                    path_tracker[neighbor] = curr_state

    while end_state:
        path.insert(0, end_state)
        end_state = path_tracker[end_state]

    return path, num_states_explored


def dfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    path = []
    num_states_explored = 0
    to_visit = []
    start = maze.getStart()
    to_visit.append(start)
    objectives = maze.getObjectives()

    while to_visit:
        curr_state = to_visit.pop()

        if curr_state not in path:
            path.append(curr_state)
            num_states_explored += 1

            if maze.isObjective(curr_state[0], curr_state[1]):
                break

            for neighbor in maze.getNeighbors(curr_state[0], curr_state[1]):
                to_visit.append(neighbor)

    return path, num_states_explored


def greedy(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    path = []
    num_states_explored = 0
    visited = []
    to_visit = queue.PriorityQueue()
    start = maze.getStart()
    to_visit.put((1, start))
    objectives = maze.getObjectives()

    while not to_visit.empty():
        curr_state = to_visit.get()

        if curr_state[1] not in visited:
            path.append(curr_state[1])
            visited.append(curr_state[1])
            num_states_explored += 1

            if maze.isObjective(curr_state[1][0], curr_state[1][1]):
                break

            for neighbor in maze.getNeighbors(curr_state[1][0], curr_state[1][1]):
                if neighbor not in visited:
                    to_visit.put((manhattan_dist(neighbor, maze), neighbor))

    return path, num_states_explored


def astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    start = maze.getStart()
    to_visit = queue.PriorityQueue()
    to_visit.put((1, start, 0)) #(priority, (x,  y), g)
    path_tracker = {start: None}
    tracked = []
    path = [start]
    path_taken = []
    visited = []
    num_states_explored = 0
    end_state = (0, 0)
    pseudo_start = start
    objectives = maze.getObjectives()
    print(objectives)

    if len(objectives)==1:
 
        print("In single dot")
        while not to_visit.empty():
            curr_state = to_visit.get()

            if curr_state[1] not in visited:
                visited.append(curr_state[1])
            
            num_states_explored += 1

            if maze.isObjective(curr_state[1][0], curr_state[1][1]):
                end_state = curr_state[1]
                break

            neighbors = maze.getNeighbors(curr_state[1][0], curr_state[1][1])
            for neighbor in neighbors:
                if neighbor not in visited and maze.isValidMove(neighbor[0], neighbor[1]):
                    to_visit.put((manhattan_dist(neighbor, maze) + curr_state[2] + 1, neighbor, curr_state[2] + 1))
                    path_tracker[neighbor] = curr_state[1]

        while end_state:
            path.insert(0, end_state)
            end_state = path_tracker[end_state]

        return path, num_states_explored

    else:    
        while not to_visit.empty():
            curr_state = to_visit.get()

            if (curr_state[1], objectives) not in visited:


                num_states_explored += 1

            #print(curr_state[1])
            #print(objectives)

                if curr_state[1] in objectives:
                    objectives.remove(curr_state[1])

                    temp = []
                    end_state = curr_state[1]
                    #print(path_tracker)
                    while end_state and end_state in path_tracker:
                        #print(end_state)
                        temp.insert(0, end_state)
                        end_state = path_tracker[end_state]

                    path += temp
                    path_tracker.clear()
                    path_tracker[curr_state[1]] = None
                    if not objectives:
                        end_state = curr_state[1]
                        break

                visited.append((curr_state[1], objectives[:]))


                neighbors = maze.getNeighbors(curr_state[1][0], curr_state[1][1])
                for neighbor in neighbors:
                    if (neighbor, objectives) not in visited and maze.isValidMove(neighbor[0], neighbor[1]):
                        to_visit.put((heuristic_func(neighbor, maze, objectives) + curr_state[2] + 1, neighbor, curr_state[2] + 1))
                        path_tracker[neighbor] = curr_state[1]

    #print(tracked)
    #while len(tracked)!=0:
     #   p = tracked.pop()
      #  print("p = ", p, '\n')
       # print(tracked)
       # while len(p)!=0:
        #    path.append(p.pop())
    #    print(end_state)
        #print(path_tracker)
        #path.insert(0, end_state)
        #end_state = path_tracker[end_state].pop()
        print(path)
    #print(path_tracker)
        return path, num_states_explored

def manhattan_dist(pos, maze):
    objectives = maze.getObjectives()
    min_heuristic = sys.maxsize
    for objective in objectives:
        heuristic = abs(pos[0] - objective[0]) + abs(pos[1] - objective[1])
        if heuristic < min_heuristic:
            min_heuristic = heuristic

    return min_heuristic

def heuristic_func(pos,maze, objectives):
    #objectives = maze.getObjectives()
    new_maze = copy.deepcopy(maze)
    weighted_objectives = {(pos,pos): 0}
    vertex = [pos]
    visited = [pos]
    seen = {(pos,pos): True}
    #print("objectives in heuristic are ",objectives)
    for objective in objectives:
        if objective not in vertex:
            vertex.append(objective)
    #print(vertex)
    mstSet = [pos]
    print("vertices are ", vertex)
    # i=0
    # j = len(vertex)
    # print(i,j)
    # while i!=j:
    #     while j!=i:

    for objective in vertex:
        for obj in vertex:
            if objective!=obj and ((objective,obj) not in seen or (obj,objective) not in seen):
                seen[(objective,obj)]=True
                seen[(obj,objective)]=True
                new_maze.setStart(objective)
                new_maze.setObjectives([obj])
                print("objective should be ", [obj])
                print("objectives are ",new_maze.getObjectives())
                print("start is ",new_maze.getStart())
                (path,x) = astar(new_maze)
                print(len(path))
                weighted_objectives[(objective,obj)]=len(path)
                weighted_objectives[(obj,objective)]=len(path)
            #(path,x) = astar(new_maze)#abs(obj[0] - objective[0])+ abs(obj[1]-objective[1])
            #weighted_objectives[(objective,obj)] = dist
    #print(min_weight)
    curr_vertex = pos
    path_length = 0
    while len(visited)!=len(vertex):
    #    print(visited)
    #    print(vertex)
        min_weight = 10000000
        goal = None
        for (objective,objs) in weighted_objectives:
            #print(objective)
            if weighted_objectives[(objective,objs)] < min_weight and objective==curr_vertex and objective!=objs and objs not in visited:
                min_weight = weighted_objectives[(objective,objs)]
                goal = objs
                #curr_vertex = objs
        #print('here')
        curr_vertex = goal
        mstSet.append(goal)
        visited.append(goal)
    i=0
    while i < len(mstSet)-1:
        path_length+=weighted_objectives[(mstSet[i],mstSet[i+1])]
        i+=1
    #print(path_length)
    return path_length    
    #print(min(weighted_objectives,weighted_objectives.get))
    #while not weighted_objectives:
    #    min_obj = min(weighted_objectives,weighted_objectives.get)
    #    for key in min_obj:
    #        print(key + " with length " + min_obj[key])
    #return 0

