# Thesis_DP

## communting data.ipynb
The data processing file loads in the origin-desination commuting data from the 2016`len` Irish census study carried out by the CSO. 
Data preparation is first carried out. The data is broken into county level and electoral division level. Data visualisation is carried out. Three csv files are produced for the county level and for the ed level. The first is the aggregated data for indivuals in the study, the second is the aggragted data with every possible journey (many have count 0) and the third is the dataset where each row corresponds to an individual. 

## central_dp_laplace.ipynb
This file uses the OpenDP library to run the Laplace Mechanism at the county level and at the electoral level. 

## central_dp_stability_hist.ipynb
This file uses the OpenDP library to run the Stability Histogram Mechanism at the county level and at the electoral level. 
