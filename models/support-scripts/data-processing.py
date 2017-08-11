# Data61 Summer Internship 2016/17
# Kenneth Young
# Data Processing for the Multi-Skill PSP results

# This file contains:
# Functions to process the results and statistics of the Minizinc output

# Packages
from __future__ import division
import os, sys, pdb, csv
import numpy as np
import subprocess as sub

#----------------------------------------------------------------------------------------#
# IMPORTING FILES

def import_results(ResultsDir, SetNum, n, m, SF, NC, SearchAbrv):

	ResultsFilename = '{}results_set{}_sf{}_nc{}_n{}_m{}_{}.txt'.format(ResultsDir,SetNum,SF,NC,n,m,SearchAbrv)
	try:
		results = csv.DictReader(open(ResultsFilename))
	except IOError:
		results = []

	# results = csv.DictReader(open(ResultsFilename))

	return results

def import_french_results(ResultsDir, SetNum, n, l, m, SF, NC, SearchAbrv, GroupedData):

	if GroupedData:
		ResultsFilename = '{}results_group{}_sf{}_nc{}_n{}_l{}_m{}_{}.txt'.format(ResultsDir,SetNum,SF,NC,n,l,m,SearchAbrv)
		try:
			results = csv.DictReader(open(ResultsFilename))
		except IOError:
			results = []

	# results = csv.DictReader(open(ResultsFilename))

	return results

def import_results_and_stats(ResultsDir,StatsDir, SetNum, n, m, SF, NC, SearchAbrv):

	ResultsFilename = '{}results_set{}_sf{}_nc{}_n{}_m{}_{}_f.txt'.format(ResultsDir,SetNum,SF,NC,n,m,SearchAbrv)

	try:
		results = csv.DictReader(open(ResultsFilename))
	except IOError:
		results = []

	StatsFilename = '{}stats_set{}_sf{}_nc{}_n{}_m{}_{}.txt'.format(StatsDir,SetNum,SF,NC,n,m,SearchAbrv)

	try:
		stats = csv.DictReader(open(StatsFilename))
	except IOError:
		stats = []

	# results = csv.DictReader(open(ResultsFilename))

	# stats = csv.DictReader(open('{}stats_set{}_sf{}_nc{}_n{}_m{}_{}.txt'.format(StatsPath,SetNum,SF,NC,n,m,SearchAbrv)))

	return results, stats

def store_all_instances(SetNum,n,SFList,NCList,ResultsDir,SearchAbrv):

	ResultsList = []

	for SF in SFList:

		mList = define_m_list(SF,n)

		for NC in NCList:
			for m in mList:
				results = import_results(ResultsDir, SetNum, n, m, SF, NC, SearchAbrv)
				results = list(results)

				ResultsList.append(results)

	return ResultsList

def store_all_instances_dict(SetNum,n,SFList,NCList,ResultsDir,SearchAbrv):

	MRSIndexList=[0,1,2]

	ResultsArray = {SF: {NC: {MRSIndex: [] for MRSIndex in MRSIndexList} for NC in NCList} for SF in SFList}

	for SF in SFList:

		mList = define_m_list(SF,n)

		for NC in NCList:
			for m in mList:
				results = import_results(ResultsDir, SetNum, n, m, SF, NC, SearchAbrv)
				results = list(results)

				ResultsArray[SF][NC][mList.index(m)].append(results)

	return ResultsArray

def store_all_instances_MRS(SetNum,n,SFList,NCList,MRSIndex,ResultsDir,SearchAbrv):

	ResultsList = []

	for SF in SFList:

		mList = define_m_list(SF,n)
		m = mList[MRSIndex]

		for NC in NCList:
			# for m in mList:
			results = import_results(ResultsDir, SetNum, n, m, SF, NC, SearchAbrv)
			results = list(results)

			ResultsList.append(results)

	return ResultsList

def store_all_french_instances_as_dict(SetNum,SFList,NCList,nList,lList,mList,ResultsDir,SearchAbrv,GroupedData=False):

	SizeOfDataset = 0
	ResultsArray = {SF: {NC: {n: {l: {m: [] for m in mList} for l in lList} for n in nList} for NC in NCList} for SF in SFList}

	for SF in SFList:
		for NC in NCList:
			for n in nList:
				for l in lList:
					for m in mList:
						results = import_french_results(ResultsDir, SetNum, n, l, m, SF, NC, SearchAbrv, GroupedData)
						results = list(results)

						ResultsArray[SF][NC][n][l][m].append(results)
						if results!=[]:
							SizeOfDataset += len(results)						

	return ResultsArray, SizeOfDataset


# ====================NEEDS COMPLETION==========
def find_SumOfsreq(DataDir):
	# find the relevant dzn file in the DataFrench directory (or elsewhere)
	# rip out the SumOfsreq line from the file and return the numeric value

	SumOfsreq = 0

	return SumOfsreq

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

def find_number_optimal(results):

	numOptimal = 0
	for inst in results:
		numOptimal = numOptimal + int(inst['optimal'])

	return numOptimal

def find_avg_makespan_reduction(results, numInstances):

	ReductionList = []

	for inst in results:
		ReductionList.append(int(inst['UB'])-int(inst['makespan']))

	AvgReduction = sum(ReductionList)/numInstances

	return AvgReduction

def find_avg_percent_reduction(results, numInstances):

	PercReductionList = []

	for inst in results:
		UB=int(inst['UB'])
		PercReductionList.append(((UB-int(inst['makespan']))/UB)*100)

	AvgPercReduction = sum(PercReductionList)/numInstances

	return AvgPercReduction

def find_number_nodes(results):

	TotalNodes = 0
	for inst in results:
		TotalNodes = TotalNodes + int(inst['nodes'])

	return TotalNodes

def find_number_propagations(results):
	TotalProps = 0
	for inst in results:
		TotalProps = TotalProps + int(inst['propagations'])

	return TotalProps

def find_total_runtime(results):

	RuntimeList = []

	for inst in results:
		if int(inst['optimal']) == 1:
			RuntimeList.append(float(inst['runtime']))

	TotalOptRuntime = sum(RuntimeList)

	return TotalOptRuntime

def add_to_running_totals(results,TotalNodes,TotalProps,TotalOpt,TotalNoSol,TotalPercGap,TotalOptRuntime,TotalRuntime):


	for inst in results:
		TotalNodes = TotalNodes + int(inst['nodes'])
		TotalProps = TotalProps + int(inst['propagations'])
		TotalOpt = TotalOpt + int(inst['optimal'])

		NoSol = 0
		if inst['makespan']=='None':
			NoSol = 1

		TotalNoSol = TotalNoSol + NoSol

		LB = float(inst['LB'])

		TotalRuntime = TotalRuntime + float(inst['runtime'])

		if int(inst['optimal'])==1:
			TotalOptRuntime = TotalOptRuntime + float(inst['runtime'])
		else:
			if NoSol == 0:
				TotalPercGap = TotalPercGap + ((float(inst['makespan'])-LB)/LB)*100

	return TotalNodes,TotalProps,TotalOpt,TotalNoSol,TotalPercGap,TotalOptRuntime,TotalRuntime

def find_french_parameter_lists(SetNum,JustUseMontoyaGroups):

	if SetNum==3:
		SFList=[0.33, 0.25, 0.2, 0]
		NCList=[1.5, 1.8, 1.93, 2.1, 2.27]
		nList=[10, 12, 14, 16, 18, 20, 30, 60, 90]
		lList=[3, 4, 5, 6]
		mList=[4, 5, 6, 7, 8, 9, 10, 11]

	elif SetNum==4:
		SFList=[0.33, 0]
		NCList=[2.7, 3.6, 3.7]
		nList=[20, 25]
		lList=[3, 8]
		mList=[2, 3, 6, 7, 8, 9, 10, 11]
	
	elif SetNum==5:
		SFList=[0]
		NCList=[1.5, 1.8, 1.93, 2.1]
		nList=[30, 60, 90, 120]
		lList=[9, 12, 15]
		mList=[6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 30, 34]

	elif SetNum==6:
		SFList=[0.11, 0.13, 0]
		NCList=[1.5, 1.8, 1.93, 2.1]
		nList=[20, 30, 60, 90]
		lList=[3, 4, 5, 6, 7, 8, 9, 10, 12]
		mList=[4, 6, 8, 10, 15]

	elif SetNum==7:
		SFList=[0]
		NCList=[1.5, 2.1]
		nList=[20, 30, 60, 90]
		lList=[3, 4, 5, 6, 7, 8, 9, 10, 12]
		mList=[4, 6, 8, 10, 15]

	elif SetNum==8:
		SFList=[0]
		NCList=[1.67, 1.8, 2.1, 2.45]
		nList=[18, 29, 33]
		lList=[2, 3, 5, 8]
		mList=[3, 5, 6, 8, 10, 11, 13, 14, 18]

	elif SetNum==9:
		SFList=[0.5, 0, 1.0]
		NCList=[1.5, 1.65, 1.8]
		nList=[5, 6, 7, 16, 20, 25, 49]
		lList=[1, 2, 3, 8]
		mList=[5, 6, 7, 10, 11, 22]

	# if JustUseMontoyaGroups:
		# if SetNum==5: # ~~~~Group 2~~~~
		# 	nList=[30, 60]
		# 	lList=[9, 12, 15]
		# 	mList=[6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

		# elif SetNum==6: # ~~~~Group 3~~~~
		# 	nList=[20, 30, 60, 90]
		# 	lList=[3, 4, 5, 6, 7, 8, 9, 10, 12]
		# 	mList=[4, 6, 8, 10, 15]

		# elif SetNum==7: # ~~~~Group 3~~~~
		# 	nList=[20, 30, 60, 90]
		# 	lList=[3, 4, 5, 6, 7, 8, 9, 10, 12]
		# 	mList=[4, 6, 8, 10, 15]
		
		# elif SetNum==8: # ~~~~Group 1~~~~
		# 	nList=[18, 29, 33]
		# 	lList=[2, 3, 5, 8]
		# 	mList=[5, 6, 8, 10, 11, 13, 14]

		# elif SetNum==9: # ~~~~Group 1~~~~
		# 	nList=[20, 25, 49]
		# 	lList=[2, 3, 8]
		# 	mList=[5, 6, 7, 10, 11]

			
	return SFList, NCList, nList, lList, mList

def find_french_parameter_lists_for_group(GroupNum):

	if GroupNum==1:
		SFList=[0.5, 0, 1.0]
		# NCList=[1.5, 1.65, 1.67, 1.8, 2.1, 2.45, 2.7, 3.6, 3.7]
		NCList=[1.5, 1.67, 1.8, 2.1, 2.45, 2.7, 3.6, 3.7] # my original set which missed some values
		nList=[18, 20, 25, 29, 33, 49]
		lList=[2, 3, 5, 8]
		# mList=[5, 6, 7, 8, 9, 10, 11, 13, 14]
		mList=[5, 6, 7, 8, 10, 11, 13, 14] # my original set which missed some values

	elif GroupNum==2:
		SFList=[0]
		# NCList=[1.5, 1.8, 1.93, 2.1, 2.27]
		NCList=[1.5, 1.8, 1.93, 2.1] # my original set which missed some values
		nList=[30, 60]
		lList=[9, 12, 15]
		mList=[6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

	elif GroupNum==3:
		SFList=[0.11, 0.13, 0]
		NCList=[1.5, 1.8, 1.93, 2.1]
		nList=[20, 30]
		lList=[3, 4, 5, 6, 7, 8, 9, 10, 12]
		mList=[4, 6, 8, 10, 15]

	return SFList, NCList, nList, lList, mList

#----------------------------------------------------------------------------------------#
# OUTPUT

# input: results
# output: a latex table format
def output_detailed_latex_table(search,SetNum,SFList,NCList,n,ResultsList,numInstances,TableDir,disj="0",free="0"):

	ResultsIndex = 0

	# find the total number of instances (most likely 216)
	SizeOfDataset = 3*len(SFList)*len(NCList)*numInstances

	# initialise putut instance file in dzn format
	# filename = TableDir + "table_disj{}_f{}_{}.txt".format(disj,free,search)
	# filename = TableDir + "table_search_mod03_{}.txt".format(search)
	filename = TableDir + "table_mod04_set2_time1800.txt".format(search)
	TableFile = open(filename, 'w')

	for SF in SFList:
		if SF == 0:
			TableFile.write("var")
		else:
			TableFile.write("{}".format(SF))
		mList = define_m_list(SF,n)
		for NC in NCList:
			TableFile.write(" & {}".format(NC))
			for m in mList:
				results = ResultsList[ResultsIndex]

				# compute totals
				TotalNodes = find_number_nodes(results)
				TotalProps = find_number_propagations(results)
				TotalOpt = find_number_optimal(results)
				TotalOptRuntime = find_total_runtime(results)

				# define the averages for output
				AvgNodes = TotalNodes/numInstances
				AvgProps = TotalProps/numInstances
				if TotalOpt == 0:
					AvgOptRuntime = 0
				else:
					AvgOptRuntime = TotalOptRuntime/TotalOpt # only count optimal instances for avg runtime

				if mList.index(m)!=0:
					TableFile.write(" & ")

				TableFile.write(" & {} & {:,.0f} & {:,.0f} & {} & {:.2f} \\\\".format(\
							m,AvgNodes,AvgProps,TotalOpt,AvgOptRuntime))

				ResultsIndex = ResultsIndex + 1
				if mList.index(m)==len(mList)-1 and NCList.index(NC)==len(NCList)-1:
					TableFile.write("\hline\n")
				else:
					TableFile.write("\n")

	TableFile.close()

	return True

# input: search strategy's results
# output: a latex table format
def write_brief_latex_table_row(TableFile,n,SFList,NCList,ResultsList,numInstances):

	ResultsIndex = 0

	# find the total number of instances (most likely 216)
	SizeOfDataset = 3*len(SFList)*len(NCList)*numInstances

	# initialise totals for output
	TotalNodes = 0
	TotalProps = 0
	TotalOpt = 0
	TotalNoSol = 0
	TotalPercGap = 0
	TotalOptRuntime = 0
	TotalRuntime = 0

	for SF in SFList:
		mList = define_m_list(SF,n)
		for NC in NCList:
			for m in mList:
				results = ResultsList[ResultsIndex]

				# update totals
				[TotalNodes,TotalProps,TotalOpt,TotalNoSol,TotalPercGap,TotalOptRuntime,TotalRuntime]=add_to_running_totals(results,TotalNodes,TotalProps,TotalOpt,TotalNoSol,TotalPercGap,TotalOptRuntime,TotalRuntime)

				ResultsIndex = ResultsIndex + 1

	# define the averages for output
	AvgNodes = TotalNodes/SizeOfDataset
	AvgProps = TotalProps/SizeOfDataset
	PercOpt = TotalOpt/SizeOfDataset*100

	if TotalOpt == 0:
		AvgOptRuntime = 0
		AvgPercGap = TotalPercGap/SizeOfDataset
	else:
		if TotalOpt < SizeOfDataset:
			AvgPercGap = TotalPercGap/(SizeOfDataset-TotalOpt-TotalNoSol)
		else:
			AvgPercGap = 0
		AvgOptRuntime = TotalOptRuntime/TotalOpt # only count the instances found to optimality

	AvgRuntime = TotalRuntime/SizeOfDataset

	# write the table row
	if TotalNodes == 0:
		TableFile.write(" & - & - & - & - & - & - & - & - \\\\")
	else:
		TableFile.write(" & {:,.0f} & {:,.0f} & {} & {:.2f} & {} & {:.2f} & {:.2f} & {:.2f} \\\\".format(AvgNodes,AvgProps,TotalNoSol,AvgPercGap,TotalOpt,PercOpt,AvgOptRuntime,AvgRuntime))

	return True

def write_MRS_measure_comp_row(TableFile,n,SFList,NCList,MRSIndex,ResultsList,numInstances):

	ResultsIndex = 0

	# find the total number of instances (most likely 216)
	SizeOfDataset = len(SFList)*len(NCList)*numInstances

	# initialise totals for output
	TotalNodes = 0
	TotalProps = 0
	TotalOpt = 0
	TotalNoSol = 0
	TotalPercGap = 0
	TotalOptRuntime = 0
	TotalRuntime = 0

	for SF in SFList:
		mList = define_m_list(SF,n)
		m=mList[MRSIndex]
		for NC in NCList:
			# for m in mList:
			results = ResultsList[ResultsIndex]

			# update totals
			[TotalNodes,TotalProps,TotalOpt,TotalNoSol,TotalPercGap,TotalOptRuntime,TotalRuntime]=add_to_running_totals(results,TotalNodes,TotalProps,TotalOpt,TotalNoSol,TotalPercGap,TotalOptRuntime,TotalRuntime)

			ResultsIndex = ResultsIndex + 1

	# define the averages for output
	AvgNodes = TotalNodes/SizeOfDataset
	AvgProps = TotalProps/SizeOfDataset
	PercOpt = TotalOpt/SizeOfDataset*100

	if TotalOpt == 0:
		AvgOptRuntime = 0
		AvgPercGap = TotalPercGap/SizeOfDataset
	else:
		if TotalOpt < SizeOfDataset:
			AvgPercGap = TotalPercGap/(SizeOfDataset-TotalOpt-TotalNoSol)
		else:
			AvgPercGap = 0
		AvgOptRuntime = TotalOptRuntime/TotalOpt # only count the instances found to optimality

	AvgRuntime = TotalRuntime/SizeOfDataset

	# write the table row
	if TotalNodes == 0:
		TableFile.write(" & - & - & - & - & - & - & - & - \\\\")
	else:
		TableFile.write(" & {:,.0f} & {:,.0f} & {} & {:.2f} & {} & {:.2f} & {:.2f} & {:.2f} \\\\".format(AvgNodes,AvgProps,TotalNoSol,AvgPercGap,TotalOpt,PercOpt,AvgOptRuntime,AvgRuntime))

	return True

def write_instance_detail(TableFile,SetNum,n,SF,NC,SFList,NCList,numInstances,SearchList,SearchAbrvList,NiceSearchAbrvList,ResultsDir,ResultsDirUB,haveUB):

	ResultsIndex = 0

	mList = define_m_list(SF,n)

	for m in mList:

		TableFile.write("\t\t\tm & inst\\# & search & opt & LB & MS & 1st & UB & 1st rt.(ms) & rt.(s) \\\\\hline\n")
		TableFile.write("\t\t\t{} & ".format(m))

		instNum=0
		for instNum in range(numInstances):

			# import all instances and store their results
			currentBestUB=9999999

			for search in SearchList:
				SearchIndex = SearchList.index(search)
				SearchAbrv = SearchAbrvList[SearchIndex]
				NiceSearchAbrv = NiceSearchAbrvList[SearchIndex]
				if NiceSearchAbrv=="smallest":
					haveUB=1
				else:
					haveUB=0

				ResultsList=store_all_instances_dict(SetNum,n,SFList,NCList,ResultsDir,SearchAbrv)
				results=ResultsList[SF][NC][mList.index(m)][0]

				if haveUB:
					ResultsListUB=store_all_instances_dict(SetNum,n,SFList,NCList,ResultsDirUB,SearchAbrv)
					resultsUB=ResultsListUB[SF][NC][mList.index(m)][0]
					# pdb.set_trace()
					instUB = resultsUB[instNum]
					optUB=str(instUB['optimal'])
					if optUB=="0":
						optUB="-"

					makespanUB=str(instUB['makespan'])
					# UB=int(inst['UB'])
					runtimeUB=float(instUB['runtime'])

					if makespanUB=="None":
						optUB="-1"
						makespanUB="-"
						firstSolUB="-"
						timeToFirstSolUB="-"
					else:
						firstSolUB=int(instUB['firstSol'])
						timeToFirstSolUB=int(instUB['timeToFirstSol'])

					# rip out the best upperbound from a text file using some sweet bash
					bestUB = sub.check_output("""cat './firstSols-Set2/firstSols_best.txt' | grep 'sf%s_nc%s_n40_m%s_0%s' | awk '{a=$2;} END {print a;}' | tr '\\n' ' ' """ %(str(SF),str(NC),str(m),str(instNum)), shell=True)

				inst = results[instNum]
				
				if instNum>0 or SearchList.index(search)>0:
					TableFile.write("\t\t\t & ")

				if SearchList.index(search)==0:
					TableFile.write("{} & ".format(instNum))
				else:
					TableFile.write("& ".format(instNum))
					
				opt=int(inst['optimal'])
				LB=int(inst['LB'])
				makespan=int(inst['makespan'])
				firstSol=int(inst['firstSol'])
				UB=int(inst['UB'])
				timeToFirstSol=int(inst['timeToFirstSol'])
				runtime=float(inst['runtime'])

				if firstSol<=currentBestUB:
					currentBestUB=firstSol
					bestSearch=NiceSearchAbrv

				if not(opt):
					opt="-"

				TableFile.write("{} & {} & {} & {} & {} & {} & {:,.0f} & {:.2f}".format(NiceSearchAbrv,opt,LB,makespan,firstSol,UB,timeToFirstSol,runtime))
				if haveUB:
					if makespanUB=="-":
						TableFile.write("\n\t\t\t\\\\ & & {} & {} & {} & {} & {} & {} & {} & {:.2f}".format(NiceSearchAbrv+"\\_UB",optUB,LB,makespanUB,firstSolUB,bestUB,timeToFirstSolUB,runtimeUB))
					else:
						TableFile.write("\n\t\t\t\\\\ & & {} & {} & {} & {} & {} & {} & {:,.0f} & {:.2f}".format(NiceSearchAbrv+"\\_UB",optUB,LB,makespanUB,firstSolUB,bestUB,timeToFirstSolUB,runtimeUB))

				if SearchList.index(search)==len(SearchList)-1:
					if instNum==numInstances-1:
						TableFile.write(" \\\\\t\t\t\hline\hline\n")
					else:
						TableFile.write(" \\\\\hline\n")
				else:
					TableFile.write("\\\\\n")

		ResultsIndex = ResultsIndex + 1

	return True

def write_instance_detail_comp_chuffed(TableFile,SetNum,n,SF,NC,SFList,NCList,numInstances,SearchList,SearchAbrvList,NiceSearchAbrvList,ResultsDir,ResultsDirUB,haveUB,compChuffed):

	ResultsIndex = 0

	mList = define_m_list(SF,n)

	for m in mList:

		TableFile.write("\t\t\tm & inst\\# & search & opt & LB & MS & 1st & UB & 1st rt.(ms) & rt.(s) \\\\\hline\n")
		TableFile.write("\t\t\t{} & ".format(m))

		instNum=0
		for instNum in range(numInstances):

			# import all instances and store their results
			currentBestUB=9999999

			for search in SearchList:
				SearchIndex = SearchList.index(search)
				SearchAbrv = SearchAbrvList[SearchIndex]
				NiceSearchAbrv = NiceSearchAbrvList[SearchIndex]
				if NiceSearchAbrv=="smallest":
					haveUB=1
				else:
					haveUB=0

				if NiceSearchAbrv=="naive" and compChuffed:
					haveUB=0
					ResultsListUB=store_all_instances_dict(SetNum,n,SFList,NCList,ResultsDirUB,SearchAbrv)
					resultsUB=ResultsListUB[SF][NC][mList.index(m)][0]
					# pdb.set_trace()
					instUB = resultsUB[instNum]
					optUB=str(instUB['optimal'])
					if optUB=="0":
						optUB="-"

					makespanUB=str(instUB['makespan'])
					UB=int(instUB['UB'])
					runtimeUB=float(instUB['runtime'])

					firstSolUB=int(instUB['firstSol'])
					timeToFirstSolUB=int(instUB['timeToFirstSol'])

				ResultsList=store_all_instances_dict(SetNum,n,SFList,NCList,ResultsDir,SearchAbrv)
				results=ResultsList[SF][NC][mList.index(m)][0]

				
				inst = results[instNum]
				
				if instNum>0 or SearchList.index(search)>0:
					TableFile.write("\t\t\t & ")

				if SearchList.index(search)==0:
					TableFile.write("{} & ".format(instNum))
				else:
					TableFile.write("& ".format(instNum))
					
				if haveUB:
					optUB=str(inst['optimal'])
					if opt=="0":
						opt="-"

					makespan=str(inst['makespan'])
					# UB=int(inst['UB'])
					runtime=float(inst['runtime'])

					if makespan=="None":
						opt="-1"
						makespan="-"
						firstSol="-"
						timeToFirstSol="-"
					else:
						firstSol=int(inst['firstSol'])
						timeToFirstSol=int(inst['timeToFirstSol'])

					# rip out the best upperbound from a text file using some sweet bash
					bestUB = sub.check_output("""cat './firstSols-Set2/firstSols_best.txt' | grep 'sf%s_nc%s_n40_m%s_0%s' | awk '{a=$2;} END {print a;}' | tr '\\n' ' ' """ %(str(SF),str(NC),str(m),str(instNum)), shell=True)
				else:
					opt=int(inst['optimal'])
					LB=int(inst['LB'])
					makespan=int(inst['makespan'])
					firstSol=int(inst['firstSol'])
					UB=int(inst['UB'])
					timeToFirstSol=int(inst['timeToFirstSol'])
					runtime=float(inst['runtime'])

				if firstSol<=currentBestUB:
					currentBestUB=firstSol
					bestSearch=NiceSearchAbrv

				if not(opt):
					opt="-"

				if NiceSearchAbrv=="smallest":
					if makespan=="-":
						TableFile.write("{} & {} & {} & {} & {} & {} & {} & {:.2f}".format(NiceSearchAbrv,opt,LB,makespan,firstSol,bestUB,timeToFirstSol,runtime))
					else:
						TableFile.write("{} & {} & {} & {} & {} & {} & {:,.0f} & {:.2f}".format(NiceSearchAbrv,opt,LB,makespan,firstSol,bestUB,timeToFirstSol,runtime))
					compChuffed=0
					haveUB=0
				else:
					TableFile.write("{} & {} & {} & {} & {} & {} & {:,.0f} & {:.2f}".format(NiceSearchAbrv+"\\_old",opt,LB,makespan,firstSol,UB,timeToFirstSol,runtime))
				if haveUB:
					if makespanUB=="-":
						TableFile.write("\\\\\n\t\t\t & & {} & {} & {} & {} & {} & {} & {} & {:.2f}".format(NiceSearchAbrv+"\\_UB",optUB,LB,makespanUB,firstSolUB,bestUB,timeToFirstSolUB,runtimeUB))
					else:
						TableFile.write("\\\\\n\t\t\t & & {} & {} & {} & {} & {} & {} & {:,.0f} & {:.2f}".format(NiceSearchAbrv+"\\_UB",optUB,LB,makespanUB,firstSolUB,bestUB,timeToFirstSolUB,runtimeUB))

				if compChuffed:
					TableFile.write("\\\\\n\t\t\t & & {} & {} & {} & {} & {} & {} & {:,.0f} & {:.2f}".format(NiceSearchAbrv,optUB,LB,makespanUB,firstSolUB,UB,timeToFirstSolUB,runtimeUB))


				if SearchList.index(search)==len(SearchList)-1:
					if instNum==numInstances-1:
						TableFile.write(" \\\\\t\t\t\hline\hline\n")
					else:
						TableFile.write(" \\\\\hline\n")
				else:
					TableFile.write("\\\\\n")
				compChuffed=1

		ResultsIndex = ResultsIndex + 1

	return True

def write_summary_row(TableFile,ResultsDict,SizeOfDataset,SFList,NCList,nList,lList,mList):

	# initialise totals for output
	TotalNodes = 0
	TotalProps = 0
	TotalNoSol = 0
	TotalPercGap = 0
	TotalOpt = 0
	TotalOptRuntime = 0
	TotalRuntime = 0

	# iterate over all results stored in ResultsDict
	for SF in SFList:
		for NC in NCList:
			for n in nList:
				for l in lList:
					for m in mList:
						for results in ResultsDict[SF][NC][n][l][m]:
							# update totals
							[TotalNodes,TotalProps,TotalOpt,TotalNoSol,TotalPercGap,TotalOptRuntime,TotalRuntime]=add_to_running_totals(results,TotalNodes,TotalProps,TotalOpt,TotalNoSol,TotalPercGap,TotalOptRuntime,TotalRuntime)

	# define the averages for output
	AvgNodes = TotalNodes/SizeOfDataset
	AvgProps = TotalProps/SizeOfDataset
	PercOpt = TotalOpt/SizeOfDataset*100

	if TotalOpt == 0:
		AvgOptRuntime = 0
		AvgPercGap = TotalPercGap/SizeOfDataset
	else:
		if TotalOpt < SizeOfDataset:
			AvgPercGap = TotalPercGap/(SizeOfDataset-TotalOpt-TotalNoSol)
		else:
			AvgPercGap = 0
		AvgOptRuntime = TotalOptRuntime/TotalOpt # only count the instances found to optimality

	AvgRuntime = TotalRuntime/SizeOfDataset


	# write the table row
	if TotalNodes == 0:
		TableFile.write(" & - & - & - & - & - & - & - & - \\\\")
	else:
		TableFile.write(" {:,.0f} & {:,.0f} & {} & {:.2f} & {}/{} & {:.2f} & {:.2f} & {:.2f} \\\\".format(AvgNodes,AvgProps,TotalNoSol,AvgPercGap,TotalOpt,SizeOfDataset,PercOpt,AvgOptRuntime,AvgRuntime))

	return True

def write_summary_row_summing_n(TableFile,ResultsDict,SizeOfDataset,SFList,NCList,nList,lList,mList,NumLess,NumOptLess,NumGreater,NumOptGreater,nNum):

	# initialise totals for output
	TotalNodes = 0
	TotalProps = 0
	TotalNoSol = 0
	TotalPercGap = 0
	TotalOpt = 0
	TotalOptRuntime = 0
	TotalRuntime = 0

	# iterate over all results stored in ResultsDict
	for SF in SFList:
		for NC in NCList:
			for n in nList:
				for l in lList:
					for m in mList:
						for results in ResultsDict[SF][NC][n][l][m]:
							if n<nNum: # change this line to change the number spat out
								if results != []:
									for inst in results:
										NumLess+=1
										if inst['optimal']=='1':
											NumOptLess+=1
										if results.index(inst)==len(results)-1:
											done=True
							elif n>=nNum:
								if results != []:
									for inst in results:
										NumGreater+=1
										if inst['optimal']=='1':
											NumOptGreater+=1
										if results.index(inst)==len(results)-1:
											done=True
							# update totals
							[TotalNodes,TotalProps,TotalOpt,TotalNoSol,TotalPercGap,TotalOptRuntime,TotalRuntime]=add_to_running_totals(results,TotalNodes,TotalProps,TotalOpt,TotalNoSol,TotalPercGap,TotalOptRuntime,TotalRuntime)
						done=False

	# define the averages for output
	AvgNodes = TotalNodes/SizeOfDataset
	AvgProps = TotalProps/SizeOfDataset
	PercOpt = TotalOpt/SizeOfDataset*100

	if TotalOpt == 0:
		AvgOptRuntime = 0
		AvgPercGap = TotalPercGap/SizeOfDataset
	else:
		if TotalOpt < SizeOfDataset:
			AvgPercGap = TotalPercGap/(SizeOfDataset-TotalOpt-TotalNoSol)
		else:
			AvgPercGap = 0
		AvgOptRuntime = TotalOptRuntime/TotalOpt # only count the instances found to optimality

	AvgRuntime = TotalRuntime/SizeOfDataset

	# write the table row
	if TotalNodes == 0:
		TableFile.write(" & - & - & - & - & - & - & - & - \\\\")
	else:
		TableFile.write(" {:,.0f} & {:,.0f} & {} & {:.2f} & {}/{} & {:.2f} & {:.2f} & {:.2f} \\\\".format(AvgNodes,AvgProps,TotalNoSol,AvgPercGap,TotalOpt,SizeOfDataset,PercOpt,AvgOptRuntime,AvgRuntime))

	return NumLess, NumOptLess, NumGreater, NumOptGreater

#----------------------------------------------------------------------------------------#
# DATA PROCESSING DRIVERS

def main_input_comparison():

	debugging = 0

	# ~~~~~~~~~~~~~~~~~~~~~~
	# Input Parameters
	SetNum = 2
	numInstances = 3
	# SFList = [1, 0.75, 0.5, 0]
	NCList = [1.5, 1.8, 2.1]

	SFList = [1, 0.75, 0.5]
	# NCList = [1.5]

	# SearchList = ["assign_s", "contrib_s", "start_s", \
	# 			"assign_Then_start", "contrib_Then_start", "start_Then_assign", "start_Then_contrib"]
	# SearchAbrvList = ["a","c","o","s","as","cs","sa","sc","oas","osa"]
	# SearchList = ["assign_Then_start", "contrib_Then_start", "overlap_Then_assign_Then_start", "overlap_Then_contrib_Then_start"]
	# SearchAbrvList = ["as","cs","oas","ocs"]
	# SearchList = ["start_s", "start_Then_assign","start_Then_contrib"]
	# SearchAbrvList = ["s","sa","sc"]
	SearchList = ["start_Then_contrib"]
	SearchAbrvList = ["sc"]

	# disj="0"
	# free="1"
	time = "1800"

	# ~~~~~~~~~~~~~~~~~~~~~~
	# I/O Directories
	# ResultsDir = "search-strategy-results-Set%d/" %(SetNum)
	# StatsPath = "search-strategy-stats-Set%d/" %(SetNum)
	# TableDir = "tables-search-strats-Set%d/" %(SetNum)
	# ResultsDir = "results-disj{}-f{}/".format(disj,free)
	# ResultsDir = "results-search-mod03/"
	ResultsDir = "results-mod04-set2-time{}/".format(time)
	# TableDir = "tables-mod03-search-set2-OLD/"
	TableDir = "tables-mod04-set2/"

	n = define_n(SetNum)

	# add looping over model and possibly solvers as well
	for search in SearchList:
		SearchIndex = SearchList.index(search)
		SearchAbrv = SearchAbrvList[SearchIndex]

		# import all instances and store their results
		ResultsList=store_all_instances(SetNum,n,SFList,NCList,ResultsDir,SearchAbrv)

		# create the latex table and save it as a txt file
		output_detailed_latex_table(search,SetNum,SFList,NCList,n,ResultsList,numInstances,TableDir)
		# output_detailed_latex_table(search,SetNum,SFList,NCList,n,ResultsList,numInstances,TableDir,disj,free)

def main_parameter_comparison():

	debugging = 0

	# ~~~~~~~~~~~~~~~~~~~~~~
	# Input Parameters
	SetNum = 2
	numInstances = 6
	SFList = [1, 0.75, 0.5, 0]
	NCList = [1.5, 1.8, 2.1]

	# SFList = [1, 0.75, 0.5]
	# NCList = [1.5, 1.8]

	# SearchList = ["assign_Then_start", "contrib_Then_start", "overlap_Then_assign_Then_start", "overlap_Then_contrib_Then_start"]
	# SearchAbrvList = ["as","cs","oas","ocs"]
	# SearchList = ["overlap_s", "start_s", "start_Then_assign","start_Then_contrib"]
	# SearchAbrvList = ["d", "s","sa","sc"]
	# SearchList = ["start_s", "start_Then_assign","start_Then_contrib"]
	# SearchAbrvList = ["s","sa","sc"]
	# SearchList = ["default", "start_s", "start_Then_assign","start_Then_contrib"]
	# SearchAbrvList = ["d", "s","sa","sc"]
	# SearchList = ["start_s"]
	# SearchAbrvList = ["s"]
	SearchList = ["start_Then_contrib"]
	SearchAbrvList = ["sc"]
	# SearchList = ["start_s", "start_Then_assign","start_Then_contrib", "activity"]
	# SearchAbrvList = ["s", "sa", "sc", "act"]
	# SearchList = ["start_Then_contrib", "activity_naive", "activity_smallest", "activity_smallest_largest", "activity_first_fail"]
	# SearchAbrvList = ["sc", "actn", "acts", "actsl", "actff"]
	# SearchList = ["activity_first_fail"]
	# SearchAbrvList = ["actff"]
	
	# ~~~~~~~~~~~~~~~~~~~~~~
	# Output Directories
	# TableDir = "tables-chuffed-disj-f/"
	# TableDir = "tables-search-chuffed/"
	# TableDir = "tables-search-gecode/"
	# TableDir = "tables-mod03-search-set2-OLD/"
	# TableDir = "tables-mod03-set1/"
	# TableDir = "tables-home-mod03-set1/"
	# TableDir = "tables-home-mod04-set1/"
	# TableDir = "tables-model-comp/"
	# TableDir = "tables-work-set1-search/"
	# TableDir = "tables-mod05/"
	TableDir = "tables-mod04/"

	n = define_n(SetNum)

	# options=["0","1"]	

	# initialise output instance file
	# filename = TableDir + "table_mod03_search_set1_f{}.txt".format(free)
	# filename = TableDir + "table_mod03_disj.txt"
	# filename = TableDir + "table_mod03_cumul.txt"
	# filename = TableDir + "table_mod03_set1_search.txt"
	# filename = TableDir + "table_mod04_set1_search.txt"
	# filename = TableDir + "table_mod04_home.txt"
	filename = TableDir + "table_mod05_home_set2_overall.txt"
	TableFile = open(filename, 'w')

	# for disj in options:
	# for ttef in options:

	# 	for free in options:

			
			
	# ResultsDir = "results-disj{}-f{}/".format(disj,free)
	# ResultsDir = "results-disj-ttef{}-f{}/".format(ttef,free)
	# ResultsDir = "results-cumul-ttef{}-f{}/".format(ttef,free)
	# ResultsDir = "results-search-chuffed-f{}/".format(free)
	# ResultsDir = "results-mod03-search-set2-old/"
	# ResultsDir = "results-mod03-search-set1-f{}/".format(free)
	# ResultsDir = "results-mod03-disj-ttef{}-f{}/".format(ttef,free)
	# ResultsDir = "results-mod03-cumul-ttef{}-f{}/".format(ttef,free)
	# ResultsDir = "results-home-mod03-set1-search/"
	# ResultsDir = "results-home-mod04-set1-search/"
	# ResultsDir = "results-mod03-set2-time1800/"
	# ResultsDir = "results-mod04-set2-time1800/"
	# ResultsDir = "results-home-mod04-set2-time300/"
	# ResultsDir = "results-home-mod04-set2-time3600/"
	# ResultsDir = "results-mod05-laptop-set1-actsearch/"
	# ResultsDir = "results-mod05-laptop-set1-actsearch-TightUB/"
	ResultsDir = "results-mod04-home-set2-time3600/"
	
	# TableFile.write(" & ")
	# TableFile.write("{} & ".format(free))
	# TableFile.write(" & {} & {}".format(ttef,free))

	for search in SearchList:
		SearchIndex = SearchList.index(search)
		SearchAbrv = SearchAbrvList[SearchIndex]

		# if SearchList.index(search)!=0:
		# 	TableFile.write(" & ")

		# TableFile.write(" & {}".format(SearchAbrv))
		TableFile.write("{}".format(SearchAbrv))

		# import all instances and store their results
		ResultsList=store_all_instances(SetNum,n,SFList,NCList,ResultsDir,SearchAbrv)

		write_brief_latex_table_row(TableFile,n,SFList,NCList,ResultsList,numInstances)

		if SearchList.index(search)==len(SearchList)-1:
			TableFile.write("\hline\n")
		else:
			TableFile.write("\n")

	TableFile.close()

def main_measure_comparison():

	debugging = 0

	# ~~~~~~~~~~~~~~~~~~~~~~
	# Input Parameters
	SetNum = 2
	numInstances = 6
	SFList = [1, 0.75, 0.5, 0]
	NCList = [1.5, 1.8, 2.1]

	# SFList = [1, 0.75]
	# NCList = [1.5, 1.8]

	# SearchList = ["start_Then_contrib"]
	# SearchAbrvList = ["sc"]
	# SearchAbrv = "sc"
	# SearchList = ["activity_naive", "activity_smallest", "activity_smallest_largest", "activity_first_fail"]
	# SearchAbrvList = ["actn", "acts", "actsl", "actff"]
	# SearchList = ["priority_smallest", "priority_smallest_load"]
	# SearchAbrvList = ["pris", "prislo"]
	# SearchList = ["activity_smallest"]
	# SearchAbrvList = ["acts"]
	# SearchList = ["activity_naive"]
	# SearchAbrvList = ["actn"]
	# SearchAbrv = SearchAbrvList[0]
	SearchList = ["priority_smallest"]
	SearchAbrvList = ["pris"]
	# SearchList = ["priority_smallest_load"]
	# SearchAbrvList = ["prislo"]
	# SearchList = ["default", "start_s", "start_Then_assign", "start_Then_contrib", "priority_input_order", "priority_smallest",  "priority_smallest_largest", "priority_first_fail"]
	# SearchAbrvList = ["def", "s", "sa", "sc","priio", "pris", "prisl", "priff"]
	# SearchList = ["default", "priority_input_order", "priority_smallest",  "priority_smallest_largest", "priority_first_fail"]
	# SearchAbrvList = ["def", "priio", "pris", "prisl", "priff"]
	
	# ~~~~~~~~~~~~~~~~~~~~~~
	# Output Directories
	# TableDir = "tables-mod04/"
	TableDir = "tables-mod06/"

	n = define_n(SetNum)

	# initialise output instance file
	filename = TableDir + "table_mod06_home_set1b.txt"
	TableFile = open(filename, 'w')

	ResultsDir = "results-mod06-set1b/"
	
	

	for search in SearchList:
		SearchIndex = SearchList.index(search)
		SearchAbrv = SearchAbrvList[SearchIndex]
		
		TableFile.write("""\\begin{table}[H]\n\t\\begin{adjustwidth}{-.9in}{-.9in}
		\\centering
		\\caption{{\\bf %s} - complexity measure comparison}
		\\vspace{2mm}
		\\begin{tabular}{cc|rrrrrrrr}
			\\hline
			measure & value  & \\#nodes & \\#props & \\#no sol & \\%%gap & \\#opt & \\%%opt & rt.(s) &  total rt.(s) \\\\
			\\hline\n""" %(search.replace("_","\\_")))

		TableFile.write("\t\t\tSF & ")

		# write the breakdown of th results for the skill factor
		for SF in SFList:

			if SFList.index(SF)!=0:
				TableFile.write("\t\t\t & ")

			TableFile.write("{}".format(SF))

			SFListTemp = [SF]

			# import all instances and store their results
			ResultsList=store_all_instances(SetNum,n,SFListTemp,NCList,ResultsDir,SearchAbrv)

			write_brief_latex_table_row(TableFile,n,SFListTemp,NCList,ResultsList,numInstances)

			if SFList.index(SF)==len(SFList)-1:
				TableFile.write("\hline\n")
			else:
				TableFile.write("\n")

		TableFile.write("\t\t\tNC & ")

		# write the breakdown of th results for the network complexity
		for NC in NCList:
			
			if NCList.index(NC)!=0:
				TableFile.write("\t\t\t & ")

			TableFile.write("{}".format(NC))

			NCListTemp = [NC]

			# import all instances and store their results
			ResultsList=store_all_instances(SetNum,n,SFList,NCListTemp,ResultsDir,SearchAbrv)

			write_brief_latex_table_row(TableFile,n,SFList,NCListTemp,ResultsList,numInstances)

			if NCList.index(NC)==len(NCList)-1:
				TableFile.write("\hline\n")
			else:
				TableFile.write("\n")

		TableFile.write("\t\t\tMRS & ")

		MRSIndexList = [0,1,2]
		# write the breakdown of th results for the modified resource strength
		for MRSIndex in MRSIndexList:
			
			if MRSIndexList.index(MRSIndex)!=0:
				TableFile.write("\t\t\t & ")

			TableFile.write("\\#{}".format(MRSIndex+1))

			MRSIndexListTemp = [MRSIndex]

			# import all instances and store their results
			ResultsList=store_all_instances_MRS(SetNum,n,SFList,NCList,MRSIndex,ResultsDir,SearchAbrv)

			write_MRS_measure_comp_row(TableFile,n,SFList,NCList,MRSIndex,ResultsList,numInstances)

			if MRSIndexList.index(MRSIndex)==len(MRSIndexList)-1:
				TableFile.write("\hline\n")
			else:
				TableFile.write("\n")

		
		# Write overall summary
		TableFile.write("\t\t\t\hline Overall & ")
		ResultsList=store_all_instances(SetNum,n,SFList,NCList,ResultsDir,SearchAbrv)
		write_brief_latex_table_row(TableFile,n,SFList,NCList,ResultsList,numInstances)
		TableFile.write("\hline\hline")

		TableFile.write("""\n\t\t\end{tabular}\n\t\end{adjustwidth}\n\end{table}\n\n""")

	TableFile.close()

def main_instance_results():

	debugging = 0

	# ~~~~~~~~~~~~~~~~~~~~~~
	# Input Parameters
	SetNum = 2
	numInstances = 6
	SFList = [1, 0.75, 0.5, 0]
	NCList = [1.5, 1.8, 2.1]

	# SFList = [1, 0.75]
	# NCList = [1.5, 1.8]

	haveUB=1
	compChuffed=1

	# SearchList = ["start_Then_contrib", "activity_naive", "activity_smallest", "activity_smallest_largest", "activity_first_fail"]
	# SearchAbrvList = ["sc", "actn", "acts", "actsl", "actff"]
	# SearchList = ["activity_naive", "activity_smallest", "activity_smallest_largest", "activity_first_fail"]
	# SearchAbrvList = ["actn", "acts", "actsl", "actff"]
	# NiceSearchAbrvList = ["naive", "smallest", "small-large", "first-fail"]
	# SearchList = ["acitvity_naive", "activity_smallest", "activity_smallest_largest", "activity_first_fail"]
	# SearchAbrvList = ["actn", "acts", "actsl", "actff"]
	# NiceSearchAbrvList = ["naive", "smallest", "small-large", "first-fail"]
	# SearchList = ["acitvity_naive", "activity_smallest"]
	# SearchAbrvList = ["actn", "acts"]
	# NiceSearchAbrvList = ["naive", "smallest"]
	SearchList = ["activity_smallest"]
	SearchAbrvList = ["acts"]
	NiceSearchAbrvList = ["smallest"]
	
	# ~~~~~~~~~~~~~~~~~~~~~~
	# Output Directories
	TableDir = "tables-mod05/"

	n = define_n(SetNum)

	# initialise output instance file
	# filename = TableDir + "table_mod05_home_set1_overall.txt"
	# filename = TableDir + "table_mod05_home_set2_instance_detail.txt"
	filename = TableDir + "table_mod05_home_set2_ubuntu_instance_detail.txt"
	TableFile = open(filename, 'w')

	# ResultsDir = "results-mod05-laptop-set1-actsearch/"
	# ResultsDirUB = "results-mod05-laptop-set1-actsearch-TightUB/"

	# ResultsDir = "results-mod05-home-set2-actSearches/"
	# ResultsDirUB = "results-mod05-home-set2-actSearches-TightUB/"

	ResultsDir = "results-mod05-home-set2-ubuntu-actSearches/"
	ResultsDirUB = "results-mod05-home-set2-ubuntu-actSearches-newChuffed/"


	
	for SF in SFList:
		for NC in NCList:
			mList = define_m_list(SF,n)

			# write the beginning of the table
			TableFile.write("""\\begin{table}[H]
	\\begin{adjustwidth}{-.9in}{-.9in}
	\\centering
	\\ssmall
	\\vspace{1mm}
	\\begin{tabular}{ccc|rrrrrrr}
			\\hline\n
			n & SF & NC & & & & & & & \\\\\\hline
			%d & %s & %.1f & & & & & & & \\\\
			\\hline\\hline
	""" %(n,str(SF),NC))

			# write_instance_detail(TableFile,SetNum,n,SF,NC,SFList,NCList,numInstances,SearchList,SearchAbrvList,NiceSearchAbrvList,ResultsDir,ResultsDirUB,haveUB)
			if compChuffed:
				write_instance_detail_comp_chuffed(TableFile,SetNum,n,SF,NC,SFList,NCList,numInstances,SearchList,SearchAbrvList,NiceSearchAbrvList,ResultsDir,ResultsDirUB,haveUB,compChuffed)
			else:
				write_instance_detail(TableFile,SetNum,n,SF,NC,SFList,NCList,numInstances,SearchList,SearchAbrvList,NiceSearchAbrvList,ResultsDir,ResultsDirUB,haveUB)

			# write the end of the table
			TableFile.write("""	\\end{tabular}
	\\end{adjustwidth}
	\\end{table}

	""")

	TableFile.close()

def main_reformat_results():
	
	# ~~~~~~~~~~~~~~~~~~~~~~
	# Input Parameters
	SetNum = 2
	numInstances = 6
	SFList = [1, 0.75, 0.5, 0]
	NCList = [1.5]

	SearchList = ["assign_Then_start", "contrib_Then_start", "overlap_Then_assign_Then_start", "overlap_Then_contrib_Then_start"]
	SearchAbrvList = ["as","cs","oas","ocs"]

	ResultsDir = "results-fixed/"
	StatsDir = "stats/"

	OutputDir = "results-final/"

	n = define_n(SetNum)

	for search in SearchList:
		SearchIndex = SearchList.index(search)
		SearchAbrv = SearchAbrvList[SearchIndex]

		ResultsList = []

		for SF in SFList:

			mList = define_m_list(SF,n)

			for NC in NCList:
				for m in mList:
					[results,stats] = import_results_and_stats(ResultsDir, StatsDir, SetNum, n, m, SF, NC, SearchAbrv)
					results = list(results)
					stats = list(stats)

					filename = OutputDir + "results_set{}_sf{}_nc{}_n{}_m{}_{}.txt".format(SetNum,SF,NC,n,m,SearchAbrv)
					ResultsFile = open(filename, 'w')

					# write header
					ResultsFile.write("instNum,optimal,UB,makespan,runtime,nodes,propagations\n")

					for instNum in range(numInstances):

						optimal = stats[instNum]['optimal']
						UB = results[instNum]['UB']
						makespan = results[instNum]['makespan']
						runtime = stats[instNum]['seconds search time']
						nodes = stats[instNum]['nodes']
						propagations = stats[instNum]['propagations']

						ResultsFile.write("%s,%s,%s,%s,%s,%s,%s\n" %(instNum,optimal,UB,makespan,runtime,nodes,propagations))



					ResultsFile.close()					

def french_group_summary():

	CompareInstancesByNumOfActs = True

	# ~~~~~~~~~~~~~~~~~~~~~~
	# Input Parameters

	GroupNumList = [1, 2, 3]
	# GroupNumList = [2, 3]
	GroupedData = True
	
	modelNum = 6
	search = "priority_smallest"
	SearchAbrv = "pris"
	
	# ~~~~~~~~~~~~~~~~~~~~~~
	# Directories
	TableDir = "tables-mod06/"
	# TableDir = "tables-mod{:02d}/".format(modelNum)
	# TableDir = "tables-model-comp/"

	# initialise output table file
	# filename = TableDir + "table_mod{:02d}_home_french_600_group123_summary.txt".format(modelNum)
	filename = TableDir + "table_mod06_french_groups.txt"
	TableFile = open(filename, 'w')

	# ResultsDir = "results-mod{:02d}-home-groups123-pris/".format(modelNum)
	ResultsDir = "results-mod06-french/"
	
	# DataDir = "../Model/DataFrench/French-Set-%d" %(GroupNum)
	
	# write table header
	TableFile.write("""\\begin{table}[H]\n\t\\begin{adjustwidth}{-.9in}{-.9in}
	\\centering
	\\caption{{\\bf %s} - our CP model applied to french data}
	\\vspace{2mm}
	\\begin{tabular}{c|rrrrrrrr}
		\\hline
		group \\#  & \\#nodes & \\#props & \\#no sol & \\%%gap & \\#opt & \\%%opt & rt.(s) &  total rt.(s) \\\\
		\\hline\n\t\t""" %(search.replace("_","\\_")))

	if CompareInstancesByNumOfActs:
		NumLess=0
		NumOptLess=0
		NumGreater=0
		NumOptGreater=0
		nNum=40

	for GroupNum in GroupNumList:

		SFList, NCList, nList, lList, mList = find_french_parameter_lists_for_group(GroupNum)
		ResultsDict, SizeOfGroup = store_all_french_instances_as_dict(GroupNum,SFList,NCList,nList,lList,mList,ResultsDir,SearchAbrv,GroupedData)
		# pdb.set_trace()

		# Write summary of group results
		TableFile.write(" %d & " %(GroupNum))
		if CompareInstancesByNumOfActs:
			NumLess,NumOptLess,NumGreater,NumOptGreater=write_summary_row_summing_n(TableFile,ResultsDict,SizeOfGroup,SFList,NCList,nList,lList,mList,NumLess,NumOptLess,NumGreater,NumOptGreater,nNum)
		else:
			write_summary_row(TableFile,ResultsDict,SizeOfGroup,SFList,NCList,nList,lList,mList)
		TableFile.write("\n\t\t")

	if CompareInstancesByNumOfActs:
		print('\nOptimal # of instances with...')
		print('\tless than %d activities:\t%d/%d' %(nNum,NumOptLess,NumLess))
		print('\tgreater than %d activities:\t%d/%d' %(nNum,NumOptGreater,NumGreater))

	# write table footer
	TableFile.write("""\hline\n\t\end{tabular}\n\t\end{adjustwidth}\n\end{table}\n\n""")

	TableFile.close()


if __name__ == "__main__":
	# main_input_comparison()
	# main_parameter_comparison()
	# main_measure_comparison()
	# main_instance_results()
	# main_reformat_results()
	french_group_summary()