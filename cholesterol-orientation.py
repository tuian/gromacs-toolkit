from MDAnalysis import *
import scipy
import numpy
import math

conf = "conf.gro"
traj = "traj_cat.xtc"

u = Universe(conf,traj) 

z = numpy.array([0, 0 , 1]) # z-axis vector

def calculate_orientation(molecule_exclude):
    ret = []
    for ts in u.trajectory:
        if (ts.frame < 20) : continue # skip  
        if (ts.frame > 50): break
        
        # select whole cholesterol molecules
        chol_list = u.selectAtoms("resname CHOL")
        #chol_list = u.selectAtoms("byres ((resname CHOL) and not (around 7 resname %s))" % (molecule_exclude) )
        
        chol_list = sort(chol_list) # sorts the cholesterols by resid, such that they are grouped into molecules
        
        print "Frame %d, found %d molecules, not neighbouring with residue %s" % (ts.frame, len(chol_list), molecule_exclude)
            
        for chol in chol_list: 
            # v is the vector between positions of OH and R5 beads in cholesterol
            v = abs(numpy.array(chol[1].pos - chol[5].pos))
            a = angle(v, z) # take abs, since chol can be in one of two leaflets
            #if  a > 90 : a = a - 90.0 
            #print a
            ret.append(a)    
    print "The mean angle is %f, std %f" % (scipy.mean(ret), scipy.std(ret))
    return np.array(ret)


def angle(v1, v2): 
    c = numpy.dot(v1,v2) / numpy.linalg.norm(v1) / numpy.linalg.norm(v2)
    angle_radians = numpy.arccos(c) # if you really want the angle
    return math.degrees(angle_radians)

def sort(atom_group):
    ret = []
    last = 0
    for atom in atom_group:
        if (atom.resid != last):
            last = atom.resid;
            ret.append([atom])
            continue
        ret[-1].append(atom)
    
    return ret

def plot(a, b, c):
    figure();
    hist([a, b, c], 10, normed=True, label=["Starting", "Cholesterol in Lo", "Cholesterol in Ld"])
    legend()
    show()
    
