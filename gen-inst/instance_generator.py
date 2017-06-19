# Data61 Summer Internship 2016/17
# Kenneth Young
# Instance Generator for the Multi-Skill PSP

# This file contains:
# Functions to generate all components of an input instance to the MSPSP
# Instance generator driver function

# Packages
from __future__ import division
import sys, pdb, time
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# User-defined functions
from instance_processing import *


#----------------------------------------------------------------------------------------#
# PRECEDENCE GRAPH GENERATION

# input: # of activites, # of start activities, # of end activities, max # of preds and 
#		succs, network complexity
# output: The edges of an AON graph
def generate_prec_graph(debugging, n, nStart, nFinish, MaxPred, MaxSucc, NC):

	count = 0
	while True:
		# Step 0: Initialise
		PrecGraph = initialise_prec_graph(n, nStart, nFinish)
		
		# Step 1: Add predecessors
		[PrecGraph, NonRedEdges] = add_predecessors(n, nStart, nFinish, MaxSucc, PrecGraph)
		
		# Step 2: Add successors
		[PrecGraph, NonRedEdges] = add_successors(n, nStart, nFinish, MaxSucc, PrecGraph, NonRedEdges)
		
		# Step 3: Achieve desired network complexity
		# ReqNumEdges = np.ceil(NC*(n+1)) # required number of edges for the given network complexity
		ReqNumEdges = np.ceil(NC*(n))
		# print NonRedEdges, ' ', ReqNumEdges
		if NonRedEdges > ReqNumEdges:
			PrecGraph = decrease_network_complexity(n, nFinish, NonRedEdges, 
							ReqNumEdges, PrecGraph)
		else:
			PrecGraph = increase_network_complexity(n, nStart, nFinish, MaxPred, MaxSucc, 
							NonRedEdges, ReqNumEdges, PrecGraph)
			if PrecGraph == False:
				print '...unachievable network complexity. Regenerating network... (%d)' %(count)
				count=count+1
			else:
				break

	
	return PrecGraph

# input: # of activites, # of start activities, # of end activities
# output: edge set containing dummy start and end edges
def initialise_prec_graph(n, nStart, nFinish):

	# initialise NetworkX graph data structure
	PrecGraph = nx.DiGraph()
	PrecGraph.add_nodes_from(range(n+2))

	# define dummy edges from node 0 to all start nodes
	for i in range(1,nStart+1):
		PrecGraph.add_edge(0,i)

	# define dummy edges from finish nodes to node n+1
	for i in range(n-nFinish+1,n+1):
		PrecGraph.add_edge(i,n+1)
	
	return PrecGraph

def add_predecessors(n, nStart, nFinish, MaxSucc, PrecGraph):
	# randomly selects a predecessor i for each non-dummy activity

	NonRedEdges = nStart + nFinish # number of non-redundant edges
	j = nStart + 1

	while j < n+1:
		while PrecGraph.predecessors(j) == []:

			if j >= (n - nFinish + 1):
				i = np.random.randint(1,high=n-nFinish+1)
			else:
				i = np.random.randint(1,high=j-1+1)

			if len(PrecGraph.successors(i)) < MaxSucc:
				PrecGraph.add_edge(i,j)
				NonRedEdges = NonRedEdges + 1

		j = j + 1

	return [PrecGraph, NonRedEdges]

def add_successors(n, nStart, nFinish, MaxPred, PrecGraph, NonRedEdges):
	# randomly selects a successor u for each non-dummy activity

	# begin with j as the last possible activity without a successor
	j = n - nFinish

	while j > 0:
		AllPreds = find_all_predecessors(j, PrecGraph, [])
		# print 'j = ', j
		# print 'AllPreds = ', AllPreds

		while PrecGraph.successors(j) == []:

			# if j has no successor then randomly choose a possible successor
			if j <= nStart:
				u = np.random.randint(nStart+1, high=n+1)
			else:
				u = np.random.randint(j+1, high=n+1)

			# compute the set of redundant successors if u in added
			RedSuccs = list(set().union([item for i in AllPreds for item in PrecGraph.successors(i)]))

			if len(PrecGraph.predecessors(u)) < MaxPred and u not in RedSuccs:
				PrecGraph.add_edge(j,u)
				NonRedEdges = NonRedEdges + 1

		j = j - 1

	return [PrecGraph, NonRedEdges]

def is_edge_redundant(i,j,PrecGraph):

	AllPreds_i = find_all_predecessors(i, PrecGraph, [])
	AllSuccs_i = find_all_successors(i, PrecGraph, [])
	AllSuccs_j = find_all_successors(j, PrecGraph, [])

	antecedent = False # store value of the complicated if condition
	for u in AllSuccs_j:
		if list(set(PrecGraph.predecessors(u)) & set(AllPreds_i)) != []:
			antecedent = True
			break

	if ( j in AllSuccs_i or \
		antecedent or \
		set(PrecGraph.predecessors(j)) & set(AllPreds_i) or \
		set(PrecGraph.successors(i)) & set(AllSuccs_j)
		):
		return True

	return False

def increase_network_complexity(n, nStart, nFinish, MaxPred, MaxSucc, NonRedEdges, ReqNumEdges, PrecGraph):
	# add edges to the graph until the required network complexity is achieved

	# only run while loop for MAXLIMIT seconds maximum 
	start_time = time.time()
	TIMELIMIT = 0.05

	while NonRedEdges <= ReqNumEdges:
		# randomly chose a node which can have another successor added
		i = np.random.randint(1, high=n-nFinish+1)
		
		if len(PrecGraph.successors(i)) < MaxSucc:
			
			# randomly chose a node j which can be a new successor of i
			if i <= nStart:
				NonSuccessors = [node for node in range(nStart+1,n+1) if node not in PrecGraph.successors(i)]
				j = np.random.choice(NonSuccessors)
			else:
				NonSuccessors = [node for node in range(i+1,n+1) if node not in PrecGraph.successors(i)]
				if NonSuccessors == []:
					continue
				else:
					j = np.random.choice(NonSuccessors)

			if len(PrecGraph.predecessors(j)) < MaxPred:

				# check if the candidate edge is redundant
				if is_edge_redundant(i,j,PrecGraph):
					continue
				else:
					PrecGraph.add_edge(i,j)
					NonRedEdges = NonRedEdges + 1

		# regenerate precedence graph if network complexity if unattainable
		if time.time() - start_time > TIMELIMIT:
			PrecGraph = False
			break
	
	return PrecGraph


# remove edges from the graph until the required network complexity is achieved
def decrease_network_complexity(n, nFinish, NonRedEdges, ReqNumEdges, PrecGraph):

	while NonRedEdges > ReqNumEdges:
		i = np.random.randint(1, high=n-nFinish+1)
		if len(PrecGraph.successors(i)) > 1:
			j = np.random.choice(PrecGraph.successors(i))
			if len(PrecGraph.predecessors(j)) > 1:
				PrecGraph.remove_edge(i,j)
				NonRedEdges = NonRedEdges - 1

	return PrecGraph

#----------------------------------------------------------------------------------------#
# RESOURCE GENERATION

# input: # of resources, # of skills, maximum # of skills any resource can master
# output: boolean resource mastery array
def generate_resources(debugging, m,l,MaxSkill):

	Resources = range(m)
	Skills = range(l)

	while True:
		ResMastery = np.zeros((m,l), dtype=np.int)
		SkillMastery = np.zeros(l, dtype=np.int)
		for res in Resources:
			# randomly decide how many skills this resource has
			nMast = np.random.randint(1,high=MaxSkill+1)

			Mast = np.random.choice(Skills, size=nMast, replace=False)

			for skill in Mast:
				# print 'res = ', res
				# print 'skill = ', skill
				# print ''
				ResMastery[res][skill] = 1

				# record that this skill has at least one master
				if SkillMastery[skill] == 0:
					SkillMastery[skill] = 1

		# if all skills are now mastered then we are done
		if 0 not in SkillMastery:
			break

	return ResMastery


#----------------------------------------------------------------------------------------#
# ACTIVITY GENERATION

# input: 
# output: 
def generate_activities(debugging, n, m, l, ResMastery, SF, MRS, MinProcTime, MaxProcTime, MaxResAct, MaxResSkill):

	# Step 1: Processing times definition
	ProcTime = generate_processing_times(n, MinProcTime, MaxProcTime)

	# Step 2: Definition of the skill requirements
	[ResReq, rho] = generate_skill_requirements(n, m, l, ResMastery, SF)

	# Step 3: Achieve desired modified resource strength
	ResReq = increase_modified_resource_strength(n, m, l, MRS, ResMastery, ResReq, 
				MaxResAct, MaxResSkill, rho)

	return ProcTime, ResReq

def generate_processing_times(n, MinProcTime, MaxProcTime):
	# generate processing times for all activities

	ProcTime = np.zeros(n+2, dtype=np.int)

	for act in range(1,n+1):
		ProcTime[act] = np.random.randint(MinProcTime, high=MaxProcTime+1)

	return ProcTime

def generate_skill_requirements(n, m, l, ResMastery, SF):
	# give all skills random requirements which are able to be fulfilled

	# initialise resource requirements as zeros
	ResReq = np.zeros((n+2,l), dtype=np.int)

	if SF > 0 and SF <= 1:
		lambd = SF * l

	while (~ResReq.any(axis=0)).any():
		act = 1
		rho = 0 # overall number of already associated resources

		while act < n+1:

			if SF <= 0 or SF > 1:
				# a non-valid SFvalue has been provided, so use a variable value of SF
				lambd = np.random.randint(2,high=l+1)

			# pdb.set_trace()
			while np.sum(ResReq[act]) < lambd:
				skill = np.random.randint(0,high=l)
				# print 'row = ', ResReq[act]
				# print 'lambd = ', lambd
				# print 'act = ', act
				# print 'skill = ', skill
				# print ResReq
				# print ''
				if ResReq[act][skill] != 1:
					ResReq[act][skill] = 1
					rho = rho + 1

			act = act + 1

	return [ResReq, rho]

def increase_modified_resource_strength(n, m, l, MRS, ResMastery, ResReq, MaxResAct, MaxResSkill, rho):
	# adds to the resource requirement of the activities to achieve the given MRS

	Skills = range(l)
	# print rho
	# print np.floor(m/MRS)
	# print ''

	while rho < np.floor(m/MRS):
		act = np.random.randint(1,high=n+1)
		ActSkillSet = [skill for skill in Skills if ResReq[act][skill] > 0]

		# print 'act = ', act
		# print 'skill set = ', [x+1 for x in ActSkillSet]
		# print ''
		# pdb.set_trace()

		if np.sum([ResReq[act][s] for s in ActSkillSet]) < MaxResAct:
			skill = np.random.choice(ActSkillSet)

			if ResReq[act][skill] < MaxResSkill:
				ResReq[act][skill] = ResReq[act][skill] + 1

				if is_flow_feasible(m, ResMastery, ResReq[act], ActSkillSet):
					rho = rho + 1
				else:
					ResReq[act][skill] = ResReq[act][skill] - 1

	return ResReq

def is_flow_feasible(m, ResMastery, SkillReq, SkillSet):

	Resources = range(m)

	# initialise directed graph to run flow algorithm on
	G = nx.DiGraph()
	G.add_node('s', demand=-np.sum(SkillReq)) # source
	G.add_node('t', demand= np.sum(SkillReq)) # sink

	# pdb.set_trace()
	UsefulRes = find_useful_resources(Resources, ResMastery, SkillSet)

	# define resource nodes and edges from the source to resources
	for res in UsefulRes:
		G.add_node(res, demand=0)
		G.add_edge('s', res, weight=0, capacity=1)

	# define required skill nodes and edges from skills to sink node
	for skill in SkillSet:
		# offset the index by the # of res
		G.add_node(skill+m, demand=0)
		G.add_edge(skill+m, 't', weight=0, capacity=SkillReq[skill])

	# define the edges between the resource and the skill nodes
	for res in Resources:
		for skill in SkillSet:
			if ResMastery[res][skill] == 1:
				G.add_edge(res, skill+m, weight=0, capacity=1)

	# pdb.set_trace()
	
	try:
		flowDict = nx.min_cost_flow(G)
	except nx.exception.NetworkXUnfeasible:
		return False

	return True


#----------------------------------------------------------------------------------------#
# DRIVER

# input: 
# output: 
def generate_instance(debugging, n, nStart, nFinish, MaxPred, MaxSucc, NC, m, l, MaxSkill, SF, MRS, MinProcTime, MaxProcTime, MaxResAct, MaxResSkill):


	print 'Generating precedence network...'
	# create the precedence graph for the given parameter values
	PrecGraph = generate_prec_graph(debugging, n, nStart, nFinish, MaxPred, MaxSucc, NC)

	# output graph
	if debugging:
		pos = nx.shell_layout(PrecGraph)
		nx.draw_networkx_nodes(PrecGraph, pos=pos, nodelist = PrecGraph.nodes())
		nx.draw_networkx_edges(PrecGraph, pos=pos, edgelist = PrecGraph.edges())
		nx.draw_networkx_labels(PrecGraph, pos=pos)
		plt.savefig("PrecGraph.png")


	print 'Generating resources...'
	# create the resources and define their skill sets
	ResMastery = generate_resources(debugging, m, l, MaxSkill)

	if debugging:
		print 'Resource Mastery Array:\n', ResMastery, '\n'


	print 'Generating activities...'
	[ProcTime, ResReq] = generate_activities(debugging, n, m, l, ResMastery,
						SF, MRS, MinProcTime, MaxProcTime, MaxResAct, MaxResSkill)

	if debugging:
		print 'Processing Times:\n', ProcTime, '\n'
		print 'Activity Skill Requirement Array:\n', ResReq, '\n'

	# instance = [PrecGraph, ResMastery, ProcTime, ResReq]

	return [PrecGraph, ResMastery, ProcTime, ResReq]


# input: 
# output: 
def main():

	debugging = 0

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# Input Parameters
	SetNum = 1
	NumInstances = 6
	SaveSumOfResReq = False

	n = define_n(SetNum)

	SFList = [1, 0.75, 0.5, 0]
	# NCList = [1.5, 1.8, 2.1]
	# SFList = [0.5, 0]
	NCList = [2.1]

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# Fixed Parameters
	nStart=3
	nFinish=3
	MaxPred=3
	MaxSucc=3

	l=4 # no. of skills
	MaxSkill=3

	MinProcTime = 1
	MaxProcTime = 10
	MaxResSkill = define_max_res_skill(n)

	for SF in SFList:
		for NC in NCList:

			mList = define_m_list(SF,n)

			for m in mList:
				MaxResAct = m	# max no. of resources per activity

				for InstNum in range(NumInstances):

					MRS = define_MRS(n,m,l,SF)
					
					print ' #  | n  | m  | SF\t| NC\t| MRS\t'
					print ' %02d | %d | %d | %4.2f\t| %3.1f\t| %6.5f\t' %(InstNum,n,m,SF,NC,MRS)

					# seed the randomisation
					seed = np.random.randint(1000000, high=9999999)
					np.random.seed(seed)

					# create instance
					[PrecGraph, ResMastery, ProcTime, ResReq] = generate_instance(debugging, n,
								nStart, nFinish, MaxPred, MaxSucc, NC, m, l, MaxSkill, 
								SF, MRS, MinProcTime, MaxProcTime, MaxResAct, MaxResSkill)

					UB = find_naive_upper_bound(ProcTime)

					LB = find_naive_lower_bound(n,PrecGraph,ProcTime)

					# save instance
					filename = 'minizinc-instances/inst_set%s_sf%s_nc%s_n%s_m%s_%02d.dzn' \
							%(str(SetNum), str(SF), str(NC), str(n), str(m), InstNum)

					if debugging:
						print 'Saving instance to path\n\t %s\n' %(filename)
					else:
						print ''

					save_instance_as_dzn(n, m, l, PrecGraph, ResMastery, ProcTime,
							ResReq, UB, LB, seed, filename, SaveSumOfResReq)



if __name__ == "__main__":
	main()

