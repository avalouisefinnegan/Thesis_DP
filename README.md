# Thesis_DP

## communting data.ipynb
The data processing file loads in the origin-desination commuting data from the 2016`len` Irish census study carried out by the CSO. 
Data preparation is first carried out. The data is broken into county level and electoral division level. Data visualisation is carried out. Three csv files are produced for the county level and for the ed level. The first is the aggregated data for indivuals in the study, the second is the aggragted data with every possible journey (many have count 0) and the third is the dataset where each row corresponds to an individual. 

## To run the workflow, set parameters in main.ipynb file and run. If save = True then this will save a csv file with the values of the true counts alongwith the differentially private counts for each value of epsilon. 
