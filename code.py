r'''

  ___ __  __    _    ____ _____ 
 |_ _|  \/  |  / \  / ___| ____|
  | || |\/| | / _ \| |  _|  _|  
  | || |  | |/ ___ \ |_| | |___ 
 |___|_|  |_/_/   _\_\____|_____|

  ____  _____ ____ __  __ _____ _   _ _____  _  _____ ___ ___  _   _ 
 / ___|| ____/ ___|  \/  | ____| \ | |_   _|/ \|_   _|_ _/ _ \| \ | |
 \___ \|  _|| |  _| |\/| |  _| |  \| | | | / _ \ | |  | | | | |  \| |
  ___) | |__| |_| | |  | | |___| |\  | | |/ ___ \| |  | | |_| | |\  |
 |____/|_____|____|_|  |_|_____|_| \_| |_/_/   _\_\_| |___\___/|_| \_| 

 
 '''

# YOU WILL NEED TO COMPLETE BOTH THE IMPLEMENTATION OF THE METHODS HERE, AS WELL AS THOSE IN utils.py
# I RECOMMEND YOU START WITH utils.py -- THOUGH IT IS YOUR DECISION

from utils import *
import numpy as np # You'll need to use numpy for this (for speed) -- if you aren't farmiliar, look at the docs
from collections import deque

def convert_image_to_graph(img):
    '''
    Given an image (3d numpy array (3, height, width)), will convert it into a graph with capacities as a function of the pixel values,
    you may decide on that function and can create a helper method for it. The returned graph should be a 2d numpy array.

    :param img: an image you would like to create a graph from, given as a 3d numpy array (3, height, width)
    '''

    # TODO -- May be tested on runtime
    '''
    Plan: 
    - Go from top left and only mark capacitance to pixels down and right. 
        - The capacitance will be calculated based on RGB similarity. 
    - Set near-infinite capacity on user-marked nodes.
    - The graph will be an adjacency list. Each node will have dictionaries for every path to another node.
        - The dictionary will store: Node traveled to, flow (set to 0), capacity, and reverse flow (since it will be a residual graph)
    '''

    channels, height, width = img.shape

    graph = [[] for _ in range(height*width + 2)] 

    imgAsFloat = img.astype(np.float32)
    maxCapacity = 10000

    for y in range(height):
        for x in range(width):
            
            nodeNum = (y*width + x) # Assign a number to each node
            pixelRGBColor = imgAsFloat[:, y, x]

            if x + 1 < width:
                v_right = nodeNum + 1
                similarity = np.linalg.norm(pixelRGBColor - imgAsFloat[:, y, x + 1])
                capacity = int(maxCapacity / (1 + similarity))
                capacity = max(capacity, 1)
                graph[nodeNum].append([v_right, capacity, 0, len(graph[v_right])])
                graph[v_right].append([nodeNum, capacity, 0, len(graph[nodeNum]) - 1])
                
            if y + 1 < height:
                v_down = nodeNum + width
                similarity = np.linalg.norm(pixelRGBColor - imgAsFloat[:, y + 1, x])
                capacity = int(maxCapacity / (1 + similarity))
                capacity = max(capacity, 1)
                graph[nodeNum].append([v_down, capacity, 0, len(graph[v_down])])
                graph[v_down].append([nodeNum, capacity, 0, len(graph[nodeNum]) - 1])

    return graph


def BFS(graph, layeredNetwork):
    #Goal: To create a layered network with source starting at 0 and each neighbor incrementing by 1. 
    for i in range(len(layeredNetwork)):
        layeredNetwork[i] = -1
    
    layeredNetwork[len(layeredNetwork) - 2] = 0 #source
    queue = deque([len(layeredNetwork) - 2]) #using a queue to speed up

    while queue: #queue returns false if empty
        n = queue.popleft()

        for neighbor in graph[n]: #find neighbords of currentNodeent node and increment them by a level
            remaining_capacity = neighbor[1] - neighbor[2]

            if (layeredNetwork[neighbor[0]] == -1 and remaining_capacity > 0):
                layeredNetwork[neighbor[0]] = layeredNetwork[n] + 1
                queue.append(neighbor[0])

    return layeredNetwork[len(layeredNetwork) - 1] != -1 #return true if we reached the sink because that means there is a path still available

def DFS(graph, layeredNetwork, failedPaths):
    numNodes = len(graph)
    source = numNodes - 2
    sink = numNodes - 1
    
    while True:
        stack = []
        currentNode = source
        
        while currentNode != sink:
            noDeadendBool = False
            for i in range(failedPaths[currentNode], len(graph[currentNode])):
                neighbor = graph[currentNode][i]
                neighborNum = neighbor[0]
                res_cap = neighbor[1] - neighbor[2]
                
                if layeredNetwork[neighborNum] == layeredNetwork[currentNode] + 1 and res_cap > 0:
                    stack.append((currentNode, i))
                    currentNode = neighborNum
                    noDeadendBool = True
                    break
                else:
                    failedPaths[currentNode] += 1
            
            if not noDeadendBool:
                if not stack:
                    return # No more augmenting paths in the currentNodeent layered network
                
                back_node, neighbor_idx = stack.pop()
                failedPaths[back_node] += 1
                currentNode = back_node
        
        # When a path is found we have to calculate the 'bottleneck' aka the minimum
        # found capacity. Once we find it we can then do the 'update' pahse
        bottleneck = 1000000000.00
        for node, index in stack:
            neighbor = graph[node][index]
            bottleneck = min(bottleneck, neighbor[1] - neighbor[2])
        
        #Update phase: This is fixing the flow for all the nodes in the path we found. 
        for node, index in stack:
            neighbor = graph[node][index]
            v = neighbor[0]
            rev_idx = neighbor[3]
            
            neighbor[2] += bottleneck
            graph[v][rev_idx][2] -= bottleneck
            
        currentNode = source



def max_flow(graph):
    numNodes = len(graph)
    layeredNetwork = [-1] * numNodes
    
    while BFS(graph, layeredNetwork):
        failedPaths = [0] * numNodes
        DFS(graph, layeredNetwork, failedPaths)
        
    return graph



def flow_to_mask(graph):
    '''
    Given a max flow (2d numpy array) assignment create a mask which has ones
    corresoponding to all the pixels in the foreground and 0s for all the background pixels

    It is up to you to determine the relationship between these things -- hint: consider what aspect of flow could
    be thought of as a binary assignment.
    '''
    numNodes = len(graph)
    source = numNodes - 2
    
    #foreground array keeps track of all nodes that can reach the sink. This should theoretically be the foreground
    foreground = [0] * numNodes
    foreground[source] = 1
    queue = deque([source])
    
    while queue: #BFS
        node = queue.popleft()

        for neighbor in graph[node]:
            v = neighbor[0]
            cap = neighbor[1] - neighbor[2]            
            if not foreground[v] and cap > 0:
                foreground[v] = 1
                queue.append(v)
                
    return np.array(foreground[:source], dtype=np.uint8)

def image_segment(dir):
    img = dir_to_img(dir) 
    
    _, height, width = img.shape
    
    graph = convert_image_to_graph(img)

    foreground_markings = User_interface(img, 'Foreground: mark the object to keep')
    background_markings = User_interface(img, 'Background: mark the area to remove')
    
    source = height * width
    sink = height * width + 1
    
    for y in range(height):
        for x in range(width):
            nodeNum = (y * width + x)
            
            if foreground_markings[y, x] == 1:
                graph[source].append([nodeNum, 1000000, 0, len(graph[nodeNum])])
                graph[nodeNum].append([source, 0, 0, len(graph[source]) - 1])

            if background_markings[y, x] == 1:
                graph[nodeNum].append([sink, 1000000, 0, len(graph[sink])])
                graph[sink].append([nodeNum, 0, 0, len(graph[nodeNum]) - 1])
    
    max_flow(graph)

    markArray = flow_to_mask(graph)
    mask2dArray = markArray.reshape((height, width))

    foreground, background = apply_masks(img, mask2dArray)

    return foreground, background
