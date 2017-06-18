# Multi-Skill Project Scheduling Problem Instance Library

Library of instances of the Multi-Skill Project Scheduling Problem (MSPSP).

## Format

Each instance is provided as an individual DataZinc file (dzn) which are naturally compability with the modelling language MiniZinc. New instances can be created in any desired format by editting the instance generator as you see fit (refer to Python scripts in the `gen-inst\` directory).

## Instances

All instances can be found in the `instances\` directory. The instances are divided into two primary sets, which are further divided into a total of five subsets.

### Set 1'

This data set was generated using the instance generator. For the full specification of the two subsets generated we refer you to Almeida *et al.* 2015.

* Set 1'a: (**100% solved**) 216 instances with 22 activities, 4 skills and 10-30 resources.
* Set 1'b: (**12.5% solved**) 216 instances with 42 activities, 4 skills and 20-60 resources.

Note, because we were unable to get in contact with the original creators of the instance generator and access their data, we instead generated our own set of instances with identical input parameters as their benchmark data. If the original data set is denoted by Set 1, we denote our equivalent data set by Set 1'.

### Set 2

This data set is a selection of the available benchmark instances used by the literature. For the full specification of the three subsets we refer you to Montoya *et al.* 2014.

* Set 2a: (**73.64% solved**) 110 instances with 20-51 activities, 2-8 skills and 5-14 resources.
* Set 2b: (**81.82% solved**) 77 instances with 32-62 activities, 9-15 skills and 5-19 resources.
* Set 2c: (**100% solved**) 91 instances with 22-32 activities, 3-12 skills and 4-15 resources.

## Instance Generator

The instance generator was developed by Young *et al.* 2017 and it was originally created by Almeida *et al.* 2015.

*To be completed*

## Solutions

The full results found by Young *et al.* 2017 can be found in the `results\` directory. 

*To be completed*

## References

1. Kenneth D. Young, Andreas Schutt, Thibaut Feydy. Constraint Programming applied to the Multi-Skill Project Scheduling Problem. In *Proceedings of Principles and Practice of Constraint Programming - CP2017*, 2017.
2. Almeida, B. F., Correia, I., Saldanha-da Gama, F. An instance generator for the multi-skill resource-constrained project scheduling problem, 2015.
3. Montoya, C., Bellenguez-Morineau, O., Pinson, E., Rivreau, D. Branch-and-price approach for the multi-skill project scheduling problem. *Optimization Letters 8(5), 1721–1734*, 2014.