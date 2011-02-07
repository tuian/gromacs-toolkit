#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python lipid2lipid.py <FILE> <OLD LIPID TYPE> <NEW LIPID TYPE>
# python lipid2lipid.py bilayer.gro POPC DAPC
# Author: Jan Domanski
# Gro parsing routine by: Clement Arnarez
# Version 1.1
import sys
from optparse import OptionParser

def process(line):
    """
    Process the line according the fixed .gro formatting
    
    Details of the gro file formatting can be found at:
    http://manual.gromacs.org/current/online/gro.html
    """
    list = [int(line[:5]), line[5:10].strip()  , line[10:15].strip(), int(line[15:20]), float(line[21:28]), float(line[29:37]), float(line[37:45])]

    dict = {}
    #dict = { "molecule_id":0, "molecule_name":"", "bead_name":"", "bead_type":0} 
    
    dict["id"] = list[0]
    dict["name"] = list[1]
    dict["type"] = list[2]
    dict["bead"] = list[3]
    dict["x"] = list[4]
    dict["y"] = list[5]
    dict["z"] = list[6]
    
    return dict # a 'bead'


def interpret(lines):
    """
    Input: the lines list read from a .gro file, without the headers
    Output: list of beads grouped by molecule
    """
    
    molecules = {} # list containing all the molecules
    
    for line in lines :
        bead = process(line)
      
        index = bead["id"]
    
        if not molecules.has_key(index) :
            molecules[index] = [bead["name"],[]]
            
        molecules[index][1].append(bead)
    
    return molecules
 
def save(header, molecules, box):

  
    print header,
    print "%i" % (len(molecules.items()))

    count = 0
    for index, [name, beads] in molecules.items():
        for bead in beads:
            count += 1
            try:
                print '%5i%-5s%5s%5i%8.3f%8.3f%8.3f' % (bead["id"], bead["name"], bead["type"], count, bead["x"], bead["y"], bead["z"]) 
            except IOError:
                "Exception: IOError"
    print box,

def post_process(lines):
    return (lines[0], lines[-1])

def remove(molecules, argv):
    """
    Input: bead type, nominator and denominator that determine the frequency of deletions
    """
    
    type = argv[0]
    numerator = int(argv[1])
    denominator = int(argv[2])
    counter = 0
    for k, [v, list] in molecules.items():
        if not v == type:
            continue
        
        counter += 1
        if counter <= numerator:
            del molecules[k]
        if counter >= denominator:

            counter = 0
    
    return molecules

def swap(molecules, argv):
    """
    conf2conf -a swap type new_type numerator denominator
    """
    
    type = argv[0]
    new_type = argv[1]
    numerator = int(argv[2])
    denominator = int(argv[3])
    counter = 0
    for k, [v, list] in molecules.items():
        if not v == type:
            continue
        
        counter += 1
        if counter <= numerator:
            atom_group = molecules[k][1]
            for atom in atom_group:
              atom["name"] = new_type
        if counter >= denominator:

            counter = 0
    
    return molecules
            
def retype(molecules, argv):
    """
    Input: molecule name, beady type (search), bead type (replace, '-' if remove)
    """
    
    molecule = argv[0]
    bead_find = argv[1]
    bead_replace = argv[2]
    counter = 0
    for k, [v, list] in molecules.items():
        if not v == molecule:
            continue
        
	bead_index = -1;
        for bead in list:
	    bead_index += 1
	    if bead["type"] != bead_find:
                continue
            if bead_replace == "-":
                del list[bead_index]
    
    return molecules

def composition(molecules):
    """
    This function dumps the conf file in a format that is suitable for a topology file, counting up all the molecules.
    """
    
    topology = [["", 0],]
    
    for key, [value, beads] in molecules.items():
        if topology[-1][0] == value:
            topology[-1][1] += 1
        else: 
            topology.append([value,1])
    for item in topology:
        print item[0], item[1]
    
def main(argv):
        
    parser = OptionParser()
    # Verbosity
    parser.add_option("-v", action="store_true", dest="verbose", default=True, 
    help="Verbose")
    # Input
    parser.add_option("-f", "--file", dest="filename",
    help="Input - Conf file - .gro", metavar="FILE", default="conf.gro")
    # Output
    parser.add_option("-o", "--output", dest="output",
    help="Output - Conf. file - .gro", metavar="FILE", default="out.gro")
    # Operation
    parser.add_option("-a", "--action", dest="function",
    help="Operation to perform: name, type, remove, composition. Include the operation-arguments afterwards.\n"+
    "Examples:\n\n"+
    "composition    no arguments, dumps the gro contents in a format suitable for a top file\n\n"+
    "name DPPC DUPC     rename DPPC molecules into DUPC molecules\n\n"+
    "type DPPC C4* -    rename a bead within a molecule of a given type, if \"-\" is given, the bead is removed.\n\n"+
    "remove CHOL 1 3    remove molecule of a certain type, with a given frequency. Here, remove 1 in 3 cholesterols"
    , metavar="STRING")

    (options, args) = parser.parse_args()

    # Pre-execution
    input = options.filename
    operation = options.function;
    file=open(input)
    lines = file.readlines()
    molecules = interpret(lines[2:-1])
    
    # Do-exectution
    
    if operation == "remove":
        molecules = remove(molecules, args)

    if operation == "swap":
        molecules = swap(molecules, args)

    if operation == "type":
	    molecules = retype(molecules, args)
        
    if operation == "dump":
        composition(molecules)
        sys.exit(0)

    # Post-execution
    
    
    (header, box) = post_process(lines)
    save(header, molecules, box)
    

if __name__ == "__main__":
    global argv
    argv = sys.argv
    main(argv[1:])

