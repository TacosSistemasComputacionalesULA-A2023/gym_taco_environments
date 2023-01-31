#!/usr/bin/python

import sys
import argparse
from typing import List

def define_parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--size", help="User name", type=int)
    parser.add_argument("-p", "--problem", help="Password", type=str)
        
    return parser.parse_args()

def generate_robot_battery_pmatrix(size : int) -> List[List[float]]:
    result = [[]]
    for _ in range(size**2):
        result.append([])
        
    
    return result

def generate_pmatrix():
    pass

if __name__ == "__main__":
    arguments = define_parse_arguments()
    
    
    
    

    