# Set 1

Instances created using the generator, which were made to be equivalent (excluding inherent randomisation) to those created by Almeida *et al.* 2015.

* Set 1'a: (**100% solved**) 216 instances with 22 activities, 4 skills and 10-30 resources.
* Set 1'b: (**12.5% solved**) 216 instances with 42 activities, 4 skills and 20-60 resources.

The next Table summarises each of the subsets of set 1:

|    | Set 1a | Set 1b |
|---:|--------|--------|
| # Instances | 216 | 216 |
| # Activities | 22 | 42 |
| # Skills | 4 | 4 |
| # Resources | 10-30 | 20-60 |
| Network Complexity (NC) | {1.5, 1.8, 2.1} | {1.5, 1.8, 2.1} |
| Skill Factor (SF) | {1,~0.75,~0.5,~variable} | {1,~0.75,~0.5,~variable} |
| Modified Resource Strength (MRS) | Listed below | ... |
| # Resources an Activity Requires | {1,~2,~3} | {1,~2,~3,~4,~5,~6,~7} |
| # Skills a Resource Masters | {1,~2,~3,~4} | {1,~2,~3,~4} |

The next Table defines the Modified Resource Strength Values for each subset.
For a full description of the MRS and its meaning we refer to the 
paper where this complexity measure was introduced: Correia *et al.*,
Project scheduling with flexible resources: formualtions and inequalities (2012).

We note that the modified resource strength is calculated
by the equation:

*MRS = (2* x *m)/(SF* x *l* x *n)*

when SF=variable, we use the value 0.75 as an approximate average.

|   |   | Set 1a |   |   | Set 1b |   |   |
|---|---|--------|---|---|--------|---|---|
|SF=1 | MRS | 0.125 | 0.15625 | 0.1875 | 0.0625 | 0.078125 | 0.09375 |
|     | m   | 20 | 25 | 30 | 40 | 50 | 60 |
|SF=0.75,var | MRS | 0.125 | 0.16667 | 0.1875 | 0.0625 | 0.079167 | 0.09375 |
|            | m   | 10| 20 | 25 | 35 | 38 | 45 |
|SF=0.5 | MRS | 0.125 | 0.1625 | 0.20833 | 0.0625 | 0.078125 | 0.09375 |
|       | m   | 10 | 13 | 15 | 20 | 25 | 30 |