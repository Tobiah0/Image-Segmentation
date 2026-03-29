'''

  ___ __  __    _    ____ _____ 
 |_ _|  \/  |  / \  / ___| ____|
  | || |\/| | / _ \| |  _|  _|  
  | || |  | |/ ___ \ |_| | |___ 
 |___|_|  |_/_/   \_\____|_____|

  ____  _____ ____ __  __ _____ _   _ _____  _  _____ ___ ___  _   _ 
 / ___|| ____/ ___|  \/  | ____| \ | |_   _|/ \|_   _|_ _/ _ \| \ | |
 \___ \|  _|| |  _| |\/| |  _| |  \| | | | / _ \ | |  | | | | |  \| |
  ___) | |__| |_| | |  | | |___| |\  | | |/ ___ \| |  | | |_| | |\  |
 |____/|_____\____|_|  |_|_____|_| \_| |_/_/   \_\_| |___\___/|_| \_|

 
 '''

# YOU WILL NEED TO COMPLETE BOTH THE IMPLEMENTATION OF THE METHODS HERE, AS WELL AS THOSE IN utils.py
# I RECOMMEND YOU START WITH utils.py -- THOUGH IT IS YOUR DECISION

from utils import *
import numpy as np # You'll need to use numpy for this (for speed) -- if you aren't farmiliar, look at the docs
from tqdm import tqdm # This library will make a loading bar for any loop -- use like: for x in tqdm(y): -- useful but not necessary


def convert_image_to_graph(img):
    '''
    Given an image (3d numpy array (3, height, width)), will convert it into a graph with capacities as a function of the pixel values,
    you may decide on that function and can create a helper method for it. The returned graph should be a 2d numpy array.

    :param img: an image you would like to create a graph from, given as a 3d numpy array (3, height, width)
    '''

    # TODO -- May be tested on runtime

    return

def max_flow(graph):
    '''
    Given a graph, as a weighted adjacency matrix (2d numpy array) of capacities, max_flow will return a
    2d array which contains the flow along each of those edges such that the flow is maximized.

    You may convert the graph into a different format, but the function will be tested with an adjacency matrix input
    and you should be careful of the time to convert.
    
    :param graph: a |v| x |v| 2d numpy array of capacities -- the first row will correspond to an array 
    of the edges out of s, and the final row will be an array of the edges out of t (should always be 0 for all).
    The first column will correspond to edges into s (all 0), and the last column will correspond to edges into t.
    A 0 can be considered to represent no edge existing in the graph. 
    '''

    # TODO -- Will be tested on correctness and (wall clock) runtime

    return

def flow_to_mask(max_flow):
    '''
    Given a max flow (2d numpy array) assignment create a mask which has ones
    corresoponding to all the pixels in the foreground and 0s for all the background pixels

    It is up to you to determine the relationship between these things -- hint: consider what aspect of flow could
    be thought of as a binary assignment.
    '''

    # TODO -- Will be tested

    return

def image_segment(dir):
    '''
    Calling this function should do all of the functionality of your image segmenter. It takes a directory to an image,
    and will return a version of it with only the foreground and another with only the background. 
    '''

    foreground = None # Placeholder
    background = None # Placeholder

    # TODO

    return foreground, background


