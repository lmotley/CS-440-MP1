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
import queue, math, sys

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
    pseudo_start = start
    to_visit = queue.PriorityQueue()
    to_visit.put((1, start, 0)) #(priority, (x,  y), g)
    path_tracker = {start: None}
    objectives = maze.getObjectives()
    num_objectives = len(objectives)
    tracked = []
    path = []
    pseudo_path = []
    visited = []
    end_state = (0,0)
    num_states_explored = 0
    objectives_reached = 0
    end_states = queue.Queue()

    while not to_visit.empty():
        curr_state = to_visit.get()
        #print("state is ", curr_state[1])
        #if curr_state[1] not in visited:
        #end_states.put(curr_state[1])
        visited.append(curr_state[1])
        num_states_explored += 1
        if curr_state[1] in objectives:
            #print("At objective")
            objectives.remove(curr_state[1])
            end_states.put(curr_state[1])
            es = curr_state[1]
            pseudo_path.insert(0,curr_state[1])
            while es!=pseudo_start and es in path_tracker:
            #    print(es)
                pseudo_path.insert(0,es)
                es = path_tracker[es]
            #print(path_tracker)
            pseudo_start = curr_state[1]
            tracked.append(pseudo_path)
            pseudo_path = []
            #print(tracked)
            path_tracker.clear()
            visited = []
            objectives_reached += 1
            if not objectives:
                end_state = curr_state[1]
                print("Reached " , objectives_reached , " out of " , num_objectives )
                break   
        neighbors = maze.getNeighbors(curr_state[1][0], curr_state[1][1])
        for neighbor in neighbors:
            if neighbor not in visited and maze.isValidMove(neighbor[0], neighbor[1]) and neighbor!=curr_state[1]:
                #print("neighbor is ", neighbor)
                to_visit.put((manhattan_dist(neighbor, maze) + curr_state[2] + 1, neighbor, curr_state[2] + 1))
                path_tracker[neighbor] = curr_state[1]
    
    #print(tracked)
    while len(tracked)!=0:
        p = tracked.pop()
        while len(p)!=0:
            path.insert(0,p.pop())
        #print(p)
    #while end_state:
    #    p = tracked[end_state]
    #    print(p)
        #path.insert(0,p)
    #    end_state = p[0]
        
    return path, num_states_explored

def manhattan_dist(pos, maze):
    objectives = maze.getObjectives()
    min_heuristic = sys.maxsize
    for objective in objectives:
        heuristic = abs(pos[0] - objective[0]) + abs(pos[1] - objective[1])
        if heuristic < min_heuristic:
            min_heuristic = heuristic

    return min_heuristic

def heuristic_func(pos,maze):
    objectives = maze.getObjectives()
    min_heuristic = sys.maxsize
    for objective in objectives:
        heuristic = abs(pos[0] - objective[0]) + abs(pos[1] - objective[1]) #placeholder
        if heuristic < min_heuristic:
            min_heuristic = heuristic
    return min_heuristic