#!/bin/bash

debugging=0

# ~~~~~~~~~~~~~~~~~~
# Input parameters

model="mspsp-07"
TIMELIMIT="600"
NumInstances="6"

SFList=("1" "0.75" "0.5" "0")
NCList=("1.5" "1.8" "2.1")

SetNumList=("1")
# SFList=("0.5")
# NCList=("2.1")

# SearchList=("start_Then_contrib")
# SearchList=("activity_smallest")
# SearchList=("activity_first_fail")
# SearchList=("activity_naive" "activity_smallest" "activity_smallest_largest" "activity_first_fail")
# SearchList=("default_s" "start_s" "start_Then_assign" "start_Then_contrib" "priority_input_order" "priority_smallest" "priority_smallest_largest" "priority_first_fail")
# SearchList=("default_s" "priority_input_order" "priority_smallest" "priority_smallest_largest" "priority_first_fail")
# SearchList=("priority_smallest" "priority_smallest_load")
SearchList=("priority_smallest")



useTightUB=0

# ~~~~~~~~~~~~~~~~~~
# Iterate over input

# iterate over all specified datasets
for SetNum in "${SetNumList[@]}"
do
	# define number of activities based on the set number
	if [ "$SetNum" == "1" ]; then
		n="20"
	elif [ "$SetNum" == "2" ]; then
		n="40"
	# elif [ "$SetNum" == "3" ]; then
	# 	n="60"
	else
		true
	fi

	# iterate over all specified search strategies
	for search in "${SearchList[@]}"
	do
		# store abbreviation of search strategy for output files
		if [ "$search" == "default_s" ]; then
			searchAbrv="def"
		elif [ "$search" == "assign_s" ]; then
			searchAbrv="a"
		elif [ "$search" == "contrib_s" ]; then
			searchAbrv="c"
		elif [ "$search" == "overlap_s" ]; then
			searchAbrv="o"
		elif [ "$search" == "start_s" ]; then
			searchAbrv="s"
		elif [ "$search" == "assign_Then_start" ]; then
			searchAbrv="as"
		elif [ "$search" == "contrib_Then_start" ]; then
			searchAbrv="cs"
		elif [ "$search" == "start_Then_assign" ]; then
			searchAbrv="sa"
		elif [ "$search" == "start_Then_contrib" ]; then
			searchAbrv="sc"
		elif [ "$search" == "overlap_Then_assign_Then_start" ]; then
			searchAbrv="oas"
		elif [ "$search" == "overlap_Then_start_Then_assign" ]; then
			searchAbrv="osa"
		elif [ "$search" == "overlap_Then_contrib_Then_start" ]; then
			searchAbrv="ocs"
		elif [ "$search" == "overlap_Then_start_Then_contrib" ]; then
			searchAbrv="osc"
		elif [ "$search" == "activity_naive_naive" ]; then
			searchAbrv="actnn"
		elif [ "$search" == "activity_naive" ]; then
			searchAbrv="actn"
		elif [ "$search" == "activity_smallest" ]; then
			searchAbrv="acts"
		elif [ "$search" == "activity_smallest_largest" ]; then
			searchAbrv="actsl"
		elif [ "$search" == "activity_first_fail" ]; then
			searchAbrv="actff"
		elif [ "$search" == "priority_input_order" ]; then
			searchAbrv="priio"
		elif [ "$search" == "priority_smallest" ]; then
			searchAbrv="pris"
		elif [ "$search" == "priority_smallest_largest" ]; then
			searchAbrv="prisl"
		elif [ "$search" == "priority_first_fail" ]; then
			searchAbrv="priff"
		elif [ "$search" == "priority_smallest_load" ]; then
			searchAbrv="prislo"
		fi

		# iterate over skill factor values
		for SF in "${SFList[@]}"
		do
			# calculate m array
			if [ "$n" == "20" ]; then
				if [ "$SF" == "1" ]; then
					mList=("20" "25" "30")
				elif [ "$SF" == "0.75" ]; then
					mList=("10" "20" "25")
				elif [ "$SF" == "0.5" ]; then
					mList=("10" "13" "15")
				else
					mList=("10" "20" "25")
				fi

			elif [ "$n" == "40" ]; then
				if [ "$SF" == "1" ]; then
					mList=("40" "50" "60")
				elif [ "$SF" == "0.75" ]; then
					mList=("30" "38" "45")
				elif [ "$SF" == "0.5" ]; then
					mList=("20" "25" "30")
				else
					mList=("30" "38" "45")
				fi
			elif [ "$n" == "60" ]; then
				if [ "$SF" == "1" ]; then
					mList=("60" "75" "90")
				elif [ "$SF" == "0.75" ]; then
					mList=("45" "55" "61")
				elif [ "$SF" == "0.5" ]; then
					mList=("30" "38" "45")
				else
					mList=("45" "55" "61")
				fi
			else
				true
			fi

			# iterate over network complexity values
			for NC in "${NCList[@]}"
			do
				# iterate over the correct resource values
				for m in "${mList[@]}"
				do
					if [ $NumInstances -ge 1 ]; then
						# solve all instances with the given parameters
						./solve_instance_CP.sh $SetNum $SF $NC $n $m $search $model $TIMELIMIT $NumInstances $useTightUB $debugging

						# print the number of instances where optimality was found
						results="./results/results_set${SetNum}_sf${SF}_nc${NC}_n${n}_m${m}_${searchAbrv}.txt"
						awk -F"," '{x+=$2}END{printf "-> " x}' "$results"
						printf "/%s optimal\n\n" ${NumInstances}
					fi
				done
			done
		done
	done
done