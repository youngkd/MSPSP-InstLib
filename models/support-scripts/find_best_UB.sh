#!/bin/bash

debugging=0

# ~~~~~~~~~~~~~~~~~~
# Input parameters

model="mspsp-05"
NumInstances="6"

SFList=("1" "0.75" "0.5" "0")
NCList=("1.5" "1.8" "2.1")

SetNumList=("2")
# SFList=("0.5")
# NCList=("2.1")

# SearchList=("start_Then_contrib")
# SearchList=("activity_smallest")
# SearchList=("activity_first_fail")
# SearchList=("activity_naive" "activity_smallest" "activity_smallest_largest" "activity_first_fail")
SearchList=("activity_smallest" "activity_smallest_largest" "activity_first_fail")

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
	elif [ "$SetNum" == "3" ]; then
		n="60"
	else
		true
	fi

	# iterate over all specified search strategies
	for search in "${SearchList[@]}"
	do
		# store abbreviation of search strategy for output files
		if [ "$search" == "assign_s" ]; then
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
		fi

		# iterate over skill factor values
		for SF in "${SFList[@]}"
		do
			# calculate m array
			if [ "$n" == "20" ]; then
				if [ "$SF" == "1" ]; then
					mList=("20" "25" "30")
				elif [ "$SF" == "0.75" ]; then
					mList=("15" "20" "25")
				elif [ "$SF" == "0.5" ]; then
					mList=("10" "13" "15")
				else
					mList=("15" "20" "25")
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
					# Define filename storing best first solutions
					if [ $SetNum -eq 1 ]; then
						BESTFIRSTSOLS="./firstSols-Set1/firstSols_best.txt"
					elif [ $SetNum -eq 2 ]; then
						BESTFIRSTSOLS="./firstSols-Set2/firstSols_best.txt"
					elif [ $SetNum -eq 3 ]; then
						BESTFIRSTSOLS="./firstSols-Set3/firstSols_best.txt"
					fi

					# Create the file if it doesn't already exist
					touch "${BESTFIRSTSOLS}"

					# 
					if [ $SetNum -eq 1 ]; then
						FIRSTSOLS="./firstSols-Set1/firstSols_${searchAbrv}.txt"
					elif [ $SetNum -eq 2 ]; then
						FIRSTSOLS="./firstSols-Set2/firstSols_${searchAbrv}.txt"
					elif [ $SetNum -eq 3 ]; then
						FIRSTSOLS="./firstSols-Set3/firstSols_${searchAbrv}.txt"
					fi

					# Store all instances
					INSTANCES="$(find -name "inst_set${SetNum}_sf${SF}_nc${NC}_n${n}_m${m}*dzn" | sort)"

					for inst in $INSTANCES
					do
						# get current best and candidate UB
						currBestMaxt=$(cat $BESTFIRSTSOLS | grep "$inst" | awk '{a=$2;} END {print a;}')
						candidateMaxt=$(cat $FIRSTSOLS | grep "$inst" | awk '{a=$2;} END {print a;}')

						# test if currBestMaxt is empty
						if [ -z "$currBestMaxt" ]; then
							currBestMaxt=9999999
						fi

						if [ $currBestMaxt -gt $candidateMaxt ]; then
							currBestMaxt=$candidateMaxt

							# replace the previous value
							sed -i 's,'"${inst}"'.*,'"${inst}"' '"${currBestMaxt}"',w changelog.txt' "$BESTFIRSTSOLS"
							# if we havent processed this instance yet, append its value
							if [ -s changelog.txt ]; then
								true
							else
								printf '%s %s\n' "${inst}" "${currBestMaxt}" >> "$BESTFIRSTSOLS"
							fi

						fi

					done
				done
			done
		done
	done
done