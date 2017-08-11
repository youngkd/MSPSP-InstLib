#!/bin/bash


SFList=("1" "0.75" "0.5" "0")
NCList=("1.5" "1.8" "2.1")

SetNumList=("1")

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
				INSTANCES="$(find -name "inst_set${SetNum}_sf${SF}_nc${NC}_n${n}_m${m}*dzn" | sort)"
				for inst in $INSTANCES
				do
					sed -i 's/maxt/% maxt/' $inst
				done
				
			done
		done
	done
done