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
import queue

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
    visited = [start]
    path = [start]
    list(map(to_visit.put, maze.getNeighbors(start[0], start[1])))
    states_explored = 1

    while not to_visit.empty():
        curr_state = to_visit.get()

        if curr_state not in visited:

            path.append(curr_state)
            visited.append(curr_state)
            states_explored += 1

            if maze.isObjective(curr_state[0], curr_state[1]):
                break

            neighbors = maze.getNeighbors(curr_state[0], curr_state[1])
            for neighbor in neighbors:
                if neighbor not in visited and maze.isValidMove(neighbor[0], neighbor[1]):
                    to_visit.put(neighbor)

    return path, states_explored


def dfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    path = []
    num_states_explored = 0
    stack = []
    startPos = maze.getStart()
    stack.append(startPos)
    objectives = maze.getObjectives()
    while stack:
        pos = stack.pop()
        if pos not in path:
            path.append(pos)
            num_states_explored += 1
            if pos in objectives:
                objectives.remove(pos)
                if len(objectives) == 0:
                    return path, num_states_explored
            for neighbor in maze.getNeighbors(pos[0], pos[1]):
                stack.append(neighbor)

    return path, num_states_explored


def greedy(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0


def astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0
