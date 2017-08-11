#!/bin/bash

debugging=0

# ~~~~~~~~~~~~~~~~~~
# Input parameters

model="mspsp-09"
TIMELIMIT="600"
SetNumList=("5")

# SearchList=("start_Then_contrib" "activity_naive" "activity_smallest" "activity_smallest_largest" "activity_first_fail")
# SearchList=("priority_input_order" "priority_smallest" "priority_smallest_largest" "priority_first_fail")
# SearchList=("priority_smallest")
SearchList=("priority_smallest_load")

useTightUB=0

# ~~~~~~~~~~~~~~~~~~
# Iterate over input

# iterate over all specified datasets
for SetNum in "${SetNumList[@]}"
do

	if [ $SetNum -eq 3 ]; then
		SFList=("0.33" "0.25" "0.2" "0")
		NCList=("1.5" "1.8" "1.93" "2.1" "2.27")
		nList=("10" "12" "14" "16" "18" "20" "30" "60" "90")
		lList=("3" "4" "5" "6")
		mList=("4" "5" "6" "7" "8" "9" "10" "11")

	elif [ $SetNum -eq 4 ]; then
		SFList=("0.33" "0")
		NCList=("2.7" "3.6" "3.7")
		nList=("20" "25")
		lList=("3" "8")
		# mList=("2" "3" "6" "7" "8" "9" "10" "11")
		mList=("6" "7" "8" "9" "10" "11")
	
	elif [ $SetNum -eq 5 ]; then
		SFList=("0")
		NCList=("1.5" "1.8" "1.93" "2.1" "2.27")
		# nList=("30" "60" "90" "120")
		nList=("30" "60")
		lList=("9" "12" "15")
		# mList=("6" "7" "8" "9" "10" "11" "12" "13" "14" "15" "16" "17" "18" "19" "20" "21" "22" "23" "24" "25" "26" "30" "34")
		mList=("6" "7" "8" "9" "10" "11" "12" "13" "14" "15" "16" "17" "18" "19")

	elif [ $SetNum -eq 6 ]; then
		SFList=("0.11" "0.13" "0")
		NCList=("1.5" "1.8" "1.93" "2.1")
		# nList=("20" "30" "60" "90")
		nList=("20" "30")
		lList=("3" "4" "5" "6" "7" "8" "9" "10" "12")
		mList=("4" "6" "8" "10" "15")

	elif [ $SetNum -eq 7 ]; then
		SFList=("0")
		NCList=("1.5" "2.1")
		# nList=("20" "30" "60" "90")
		nList=("20" "30")
		lList=("3" "4" "5" "6" "7" "8" "9" "10" "12")
		mList=("4" "6" "8" "10" "15")

	elif [ $SetNum -eq 8 ]; then
		SFList=("0")
		NCList=("1.65" "1.8" "2.1" "2.45")
		nList=("18" "29" "33")
		lList=("2" "3" "5" "8")
		# mList=("3" "5" "6" "8" "10" "11" "13" "14" "18")
		mList=("5" "6" "8" "9" "10" "11" "13" "14")

	elif [ $SetNum -eq 9 ]; then
		SFList=("0.5" "0" "1.0")
		NCList=("1.5" "1.65" "1.8" )
		# nList=("5" "6" "7" "16" "20" "25" "49")
		nList=("20" "25" "49")
		# lList=("1" "2" "3" "8")
		lList=("2" "3" "8")
		# mList=("5" "6" "7" "10" "11" "22")
		mList=("5" "6" "7" "10" "11")
	fi

	# iterate over all specified search strategies
	for search in "${SearchList[@]}"
	do
		# store abbreviation of search strategy for output files
		if [ "$search" == "start_s" ]; then
			searchAbrv="s"
		elif [ "$search" == "start_Then_contrib" ]; then
			searchAbrv="sc"
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
			# iterate over network complexity values
			for NC in "${NCList[@]}"
			do
				# iterate over numbers of activities
				for n in "${nList[@]}"
				do
					# iterate over numbers of skill
					for l in "${lList[@]}"
					do
						# iterate over numbers of resources
						for m in "${mList[@]}"
						do
							# find the number of instances with these parameter values
							NumInstances=$(find -name "inst_set${SetNum}_sf${SF}_nc${NC}_n${n}_l${l}_m${m}*dzn" | wc -l)

							if [ $NumInstances -ge 1 ]; then
								# solve all instances with the given parameters
								./solve_french_instance_CP.sh $SetNum $SF $NC $n $l $m $search $model $TIMELIMIT $NumInstances $useTightUB $debugging

								# print the number of instances where optimality was found
								results="./results/results_set${SetNum}_sf${SF}_nc${NC}_n${n}_l${l}_m${m}_${searchAbrv}.txt"
								awk -F"," '{x+=$2}END{printf "-> " x}' "$results"
								printf "/%s optimal\n\n" ${NumInstances}
							fi
							
						done
					done
				done
			done
		done
	done
done