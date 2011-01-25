#!/usr/bin/env python
"""
-*- coding: utf-8 -*-
python lipid2lipid.py <FILE> <OLD LIPID TYPE> <NEW LIPID TYPE>
python lipid2lipid.py bilayer.gro POPC DAPC
AUTHOR: Jan Domanski
Version 1.0
Residue has to be changed manually"""
import sys
import re
from optparse import OptionParser

def main(argv):
        
    parser = OptionParser()
    # Input
    parser.add_option("-f", "--file", dest="filename",
    help="Input - Topology file - .itp", metavar="FILE")
    # Output
    parser.add_option("-o", "--output", dest="output",
    help="Output - Conf. file - .gro", metavar="FILE", default="out.gro")
    # Operation
    parser.add_option("-a", "--add", dest="value",
    help="Add given value to each atom in the topology" , metavar="INTEGER")

    (options, args) = parser.parse_args()

    # Pre-execution
    filename = options.filename
    output = options.output
    
    topology = parse_file(options.filename)
    
    topology = append_value(topology, int(options.value))
    
    for k, v in topology.items(): 
        print k
        for i in v:
            print i
    
    
def parse_file(file_name):
    line_list = open(file_name, 'r').readlines()
    
    topology = {}
    
    last_key = ""
        
    for line in line_list:
        if line[0] == "[": 
            line = re.sub(r'\s', '', line)
            topology[line] = []
            last_key = line
            continue
        topology[last_key].append(line)
    
    return topology

def handle_atoms(line_list, value):
    
    ret = []
    
    for line in line_list:
        record = line.split()
        if len(record) == 0: continue
        if record[0] == ';': continue
        record[0]  = str(int(record[0]) + value)
        record[-2] = str(int(record[-2]) + value)
        ret.append("\t".join(record))
        
    return ret

def handle_angles(line_list, value):
    
    ret = []
    
    for line in line_list:
        record = line.split()
        if len(record) == 0: continue
        if record[0] == ';': continue
        record[0]  = str(int(record[0]) + value)
        record[1] = str(int(record[1]) + value)
        record[2] = str(int(record[2]) + value)
        ret.append("\t".join(record))
        
    return ret        

def handle_bonds(line_list, value):
    
    ret = []
    
    for line in line_list:
        record = line.split()
        if len(record) == 0: continue
        if record[0] == ';': continue
        record[0]  = str(int(record[0]) + value)
        record[1] = str(int(record[1]) + value)
        ret.append("\t".join(record))
        
    return ret  

def handle_dihedrals(line_list, value):
    
    ret = []
    
    for line in line_list:
        record = line.split()
        if len(record) == 0: continue
        if record[0] == ';': continue
        record[0]  = str(int(record[0]) + value)
        record[1] = str(int(record[1]) + value)
        record[2] = str(int(record[2]) + value)
        record[3] = str(int(record[3]) + value)
        ret.append("\t".join(record))
        
    return ret  

def handle_exclusions(line_list, value):
    
    ret = []
    
    for line in line_list:
        record = line.split()
        if len(record) == 0: continue
        if record[0] == ';': continue
        
        result = []
        
        for r in record:
            result.append(str(int(r) + value))
        ret.append("\t".join(result))
        
    return ret  

def append_value(top, value):

    topology = {}
    
    for section, list in top.items():
        if section == "[atoms]":
            list = handle_atoms(list, value)
            topology[section] = list
        if section == "[angles]":
            list = handle_angles(list, value)
            topology[section] = list  
        if section == "[bonds]" or section == "[constraints]"  :
            list = handle_bonds(list, value)
            topology[section] = list 
        if section == "[dihedrals]"  :
            list = handle_dihedrals(list, value)
            topology[section] = list 
        if section == "[exclusions]"  :
            list = handle_exclusions(list, value)
            topology[section] = list 
    
    return topology
    

if __name__ == "__main__":
    global argv
    argv = sys.argv
    main(argv[1:])

