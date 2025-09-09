import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator
import random


'''This code can allow the user to select the nodes of the obstacles, the initial point and 
the end point of a grid (workspace) to find the best trajectory between those points by avoiding the obstacles.
A* algorithm
''' 


# Function to find the distance between two points
def heuristic(a, b):
    return np.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)

# Determines the neighboring points surrounding the current node within the specified width and height of the workspace
def get_neighbors(node, width, height):
    x, y = node
    neighbors = [] 
    # Check left neighbor
    if x > 0:
        neighbors.append((x - 1, y))
    # Check right neighbor
    if x < width - 1:
        neighbors.append((x + 1, y))
    # Check upper neighbor
    if y > 0:
        neighbors.append((x, y - 1))
    # Check lower neighbor
    if y < height - 1:
        neighbors.append((x, y + 1))

    # Diagonal neighbors
    if x > 0 and y > 0:
        neighbors.append((x - 1, y - 1))  # Top left
    if x > 0 and y < height - 1:
        neighbors.append((x - 1, y + 1))  # Bottom left
    if x < width - 1 and y > 0:
        neighbors.append((x + 1, y - 1))  # Top right
    if x < width - 1 and y < height - 1:
        neighbors.append((x + 1, y + 1))  # Bottom right
    return neighbors


# Traces back the path from the current node to the start node using the came_from dictionary.
def reconstruct_path(came_from, start, current):
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    return path[::-1] #Returns the path from the start to the end


# Function that finds the shortest path from the start node to the end node while avoiding obstacles (A* algorithm)
def find_path(width, height, obstacles, start, end):
    open_set = [] #A list to store nodes to be evaluated
    closed_set = set() #A set to keep track of visited nodes. Collection which is unordered, unchangeable, and unindexed. Sets do not use keys
    came_from = {} #A dictionary to maintain the path information (each node's parent). To access the node through the node that it comes from (key)

    open_set.append(start) #The starting node is added to open_set for the initial iteration.
    came_from[start] = None #The came_from dictionary is updated to mark the starting node with None as it has no parent.

    while open_set: #This loop continues as long as there are nodes to evaluate in open_set
        current_node = min(open_set, key=lambda node: heuristic(node, end)) #Find the node in open_set with the minimum heuristic value
        open_set.remove(current_node)
        if current_node == end: #If the current node is the destination (end) node, reconstruct and return the path using came_from.
            return reconstruct_path(came_from, start, end)
        closed_set.add(current_node) #Add the current node to closed_set to avoid revisiting it
        for neighbor in get_neighbors(current_node, width, height):
            if neighbor in closed_set or neighbor in obstacles: #if the node is already visited (closed_set) or an obstacle skip it
                continue
            if neighbor not in open_set:
                open_set.append(neighbor)
                came_from[neighbor] = current_node
    return None #If the loop exits without finding the end node, return None to indicate that no valid path exists


#Function to plot the path, the obstacles, the start and end points in the Cartesian Plane using matplotlib
def plot_path(width, height, obstacles, start, end, path):
    # Create a scatter plot for obstacles
    obstacles_x, obstacles_y = zip(*obstacles)
    plt.scatter(obstacles_x, obstacles_y, color='red', marker='s', s=200, label='Obstacles')

    # Create a scatter plot for the path
    path_x, path_y = zip(*path)
    plt.plot(path_x, path_y, color='orange', marker='o', markersize=8, label='Path')

    # Mark start and end points
    plt.scatter(start[0], start[1], color='green', marker='o', s=200, label='Start')
    plt.scatter(end[0], end[1], color='blue', marker='o', s=200, label='End')

    # Set axis labels
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')

    # Set plot title
    plt.title('A* Best Pathfinding')

    # Add legend
    # Move the legend outside the axes
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

    # Add grid with 1 by 1 major locators
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.gca().xaxis.set_major_locator(MultipleLocator(1))
    plt.gca().yaxis.set_major_locator(MultipleLocator(1))

    # Set axis limits
    plt.xlim(0, width)
    plt.ylim(0, height)


    # Show the plot
    plt.show()



# Example
width = 10
height = 10
obstacles = [(2, 2), (3, 4), (3, 3), (7, 7)]
#start_point = (1, 1)
#end_point = (5, 4)

# Generate random start point not in obstacles
start_point = (random.randint(0, width - 1), random.randint(0, height - 1))
while start_point in obstacles:
    start_point = (random.randint(0, width - 1), random.randint(0, height - 1))

# Generate random end point not in obstacles and different from start point
end_point = (random.randint(0, width - 1), random.randint(0, height - 1))
while end_point in obstacles or end_point == start_point:
    end_point = (random.randint(0, width - 1), random.randint(0, height - 1))


path = find_path(width, height, obstacles, start_point, end_point)
if path:
    print("Path found:", path)
    plot_path(width, height, obstacles, start_point, end_point, path)
else:
    print("No path found")
