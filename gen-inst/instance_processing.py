# Data61 Summer Internship 2016/17
# Kenneth Young
# Support Functions for the Instance Processing of the Multi-Skill PSP

# This file contains:
# Functions processing a given instance into the desired output format

# Packages
from __future__ import division
import sys, pdb, time
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


#----------------------------------------------------------------------------------------#
# SUPPORT FUNCTIONS

def define_n(SetNum):
	# define correct number of acitivites
	if SetNum == 1:
		n=20
	elif SetNum == 2:
		n=40
	elif SetNum == 3:
		n=60

	return n

def define_m_list(SF,n):

	# define the correct set of m values
	if n==20:
		if SF==1:
			mList = [20, 25, 30]
		elif SF==0.5:
			mList = [10, 13, 15]
		else:
			mList = [10, 20, 25]

	elif n==40:
		if SF==1:
			mList = [40, 50, 60]
		elif SF==0.5:
			mList = [20, 25, 30]
		else:
			mList = [30, 38, 45]

	elif n==60:
		if SF==1:
			mList = [60, 75, 90]
		elif SF==0.5:
			mList = [30, 38, 45]
		else:
			mList = [45, 55, 61]

	return mList

def define_max_res_skill(n):

	if n==20:
		MaxResSkill = 3
	elif n==40:
		MaxResSkill = 7
	elif n==60:
		MaxResSkill = 16		

	return MaxResSkill

def define_MRS(n,m,l,SF):
	# define the pre-chosen value of the MRS for the input parameters
	if SF==0:
		if n==20:
			MRS = m/(n*l*0.75*2)
		elif n==40:
			MRS = m/(n*l*0.75*4)
		elif n==60:
			MRS = m/(n*l*0.75*6)
	else:
		if n==20:
			MRS = m/(n*l*SF*2)
		elif n==40:
			MRS = m/(n*l*SF*4)
		elif n==60:
			MRS = m/(n*l*SF*6)

	return MRS

def find_all_successors(node, PrecGraph, AllSuccessors):
	# finds all successors of a given node
	for s in PrecGraph.successors(node):
		if s not in AllSuccessors:
			AllSuccessors.append(s)
			find_all_successors(s, PrecGraph, AllSuccessors)
	return AllSuccessors

def find_all_predecessors(node, PrecGraph, AllPredecessors):
	# finds all predecessors of a given node
	for p in PrecGraph.predecessors(node):
		if p not in AllPredecessors:
			AllPredecessors.append(p)
			find_all_predecessors(p, PrecGraph, AllPredecessors)
	return AllPredecessors

def find_naive_upper_bound(ProcTime):
	UB = np.sum(ProcTime)
	return UB

def find_naive_lower_bound(n,PrecGraph,ProcTime):

	AllPaths = nx.all_simple_paths(PrecGraph, source=0, target=n+1)
	AllPaths = list(AllPaths)

	PathLengthList = []

	for path in AllPaths:
		PathLength = sum([ ProcTime[act] for act in path ])
		PathLengthList.append(PathLength)

	LB = max(PathLengthList)

	return LB

def find_useful_resources(Resources, ResMastery, SkillSet):

	UsefulRes = []
	for res in Resources:
		for skill in SkillSet:
			if ResMastery[res][skill] == 1:
				UsefulRes.append(res)
				break

	return UsefulRes

def find_potential_activities(Acts, ResReq, SkillSet):

	PotentialAct = []
	for act in Acts:
		for skill in SkillSet:
			if ResReq[act][skill] >= 1:
				PotentialAct.append(act)
				break

	return PotentialAct

def find_unrelated_activities(n, G):

	Acts = range(1,n+1)

	Unrels = []

	# pdb.set_trace()
	for i in Acts:
		# AllSuccs_i = find_all_successors(i, G, [])

		for j in Acts:
			if j > i and not(nx.has_path(G, i, j)):
				Unrels.append((i,j))

	# pdb.set_trace()

	return Unrels

#----------------------------------------------------------------------------------------#
# INSTANCE WRITING

def save_instance_as_dzn(n, m, l, PrecGraph, ResMastery, ProcTime, ResReq, UB, LB, seed, filename, SaveSumOfResReq=False):

	Acts = range(n+2)
	Resources = range(m)
	Skills = range(l)

	# initialise outut instance file in dzn format
	InstFile = open(filename, 'w')


	# store the seed used for the randomisation
	InstFile.write('%% seed = %d\n\n' %(seed))

	InstFile.write('mint = %d;\n' %(LB))
	InstFile.write('%% maxt = %d;\n\n' %(UB))

	# store # of activities and their durations
	InstFile.write('nActs = %d;\n' %(n+2))

	InstFile.write('dur = [0')
	for act in range(1,n+2):
		InstFile.write(',%d' %(ProcTime[act]) )
	InstFile.write('];\n\n')

	# store activities' skill requirements
	InstFile.write('nSkills = %d;\n' %(l))

	InstFile.write('sreq = [| ')
	for act in Acts:
		for skill in Skills:
			InstFile.write('%d,' %(ResReq[act][skill]))
		if act < n+1:
			InstFile.write('\n\t| ')
		else:
			InstFile.write(' |];\n\n')

	if SaveSumOfResReq:
		SumOfResReq = np.sum(ResReq) 
		InstFile.write('%% SumOfsreq = %d;\n\n' %(SumOfResReq))

	# store resources' skill mastery
	InstFile.write('nResources = %d;\n' %(m))

	InstFile.write('mastery = [| ')
	for res in Resources:
		for skill in Skills:
			if ResMastery[res][skill]:
				InstFile.write('true,')
			else:
				InstFile.write('false,')
		if res < m-1:
			InstFile.write('\n\t| ')
		else:
			InstFile.write(' |];\n\n')

	# store precedences
	Edges = PrecGraph.edges()
	nPrec = len(Edges)
	InstFile.write('nPrecs = %d;\n' %(nPrec) )

	InstFile.write('pred = [1')
	for p in range(1,nPrec):
		InstFile.write(',%d' %(Edges[p][0]+1))
		if p == nPrec-1:
			InstFile.write('];\n')

	InstFile.write('succ = [2')
	for p in range(1,nPrec):
		InstFile.write(',%d' %(Edges[p][1]+1))
		if p == nPrec-1:
			InstFile.write('];\n\n')

	# store unrelated activities
	Unrels = find_unrelated_activities(n, PrecGraph)
	nUnrels = len(Unrels)

	InstFile.write('nUnrels = %d;\n' %(nUnrels) )

	# pdb.set_trace()
	InstFile.write('unpred = [')
	for u in range(nUnrels):
		if u == nUnrels-1:
			InstFile.write('%d];\n' %(Unrels[u][0]+1))
		else:
			InstFile.write('%d,' %(Unrels[u][0]+1))

	InstFile.write('unsucc = [')
	for u in range(nUnrels):
		if u == nUnrels-1:
			InstFile.write('%d];\n\n' %(Unrels[u][1]+1))
		else:
			InstFile.write('%d,' %(Unrels[u][1]+1))

	# find the set of useful resoruces for each activity
	InstFile.write('USEFUL_RES = [{},\n\t{')
	for act in Acts[1:]:
		ActSkillSet = [skill for skill in Skills if ResReq[act][skill] > 0]
		UsefulRes = find_useful_resources(Resources, ResMastery, ActSkillSet)
		for resIndex in range(len(UsefulRes)):
			if resIndex < len(UsefulRes)-1:
				InstFile.write('%d,' %(UsefulRes[resIndex]+1))
			else:
				InstFile.write('%d}' %(UsefulRes[resIndex]+1))

		if UsefulRes==[] and act==n+1:
			InstFile.write('}')			

		if act < n+1:
			InstFile.write(',\n\t{')
		else:
			InstFile.write('];\n\n')

	# find the set of potential activities for each resource
	InstFile.write('POTENTIAL_ACT = [{')
	for res in Resources:
		ResSkillSet = [skill for skill in Skills if ResMastery[res][skill] > 0]
		PotentialAct = find_potential_activities(Acts, ResReq, ResSkillSet)

		for actIndex in range(len(PotentialAct)):
			if actIndex < len(PotentialAct)-1:
				InstFile.write('%d,' %(PotentialAct[actIndex]+1))
			else:
				InstFile.write('%d}' %(PotentialAct[actIndex]+1))

		if PotentialAct==[]:
			InstFile.write('}')			
				
		if res < m-1:
			InstFile.write(',\n\t{')
		else:
			InstFile.write('];\n')
	

	InstFile.close()

	return True