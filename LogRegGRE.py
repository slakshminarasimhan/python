# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 19:49:07 2018

"""


import pandas as pd
import numpy as np

## Loading data directly from UCLA
#df = pd.read_stata("https://stats.idre.ucla.edu/stat/stata/dae/binary.dta")

## Loading data from our GitHub
df = pd.read_csv("D:\\Users\\Data\\admission.csv")

## Taking a look at the data
df.describe()

## Converting variable to categorical data type (since that what it is)
## and then creating dummy variables
df['rank'] = df['rank'].astype('category')
#without this declaration, raise error issue
rank = df['rank']

df = pd.get_dummies(df)

# Needed to run the logistic regression
import statsmodels.formula.api as smf

# For plotting/checking assumptions
import seaborn as sns

#Logistic regression does not require the continuous IV(s) to be linearly related to the DV. 
#It does require the continuous IV(s) be linearly related to the log odds of the IV though. 

gre = sns.regplot(x= 'gre', y= 'admit', data= df, logistic= True).set_title("GRE Log Odds Linear Plot")
gre.figure.savefig("D:\\Users\\gre log lin.png")

gpa = sns.regplot(x= 'gpa', y= 'admit', data= df, logistic= True).set_title("GPA Log Odds Linear Plot")
gpa.figure.savefig("D:\\Users\\gpa log lin.png")

#Absence of Multicollinearity

df.corr()

#Lack of outliers
#had to be commented. Have raised the issue in the web site. will continue to research why it does not work
#gpa_rank_box = sns.boxplot(data= df[['gpa', 'rank']]).set_title("GPA and Rank Box Plot")
#gpa_rank_box.figure.savefig("D:\\Users\\GPA and Rank Box Plot.png")

gre_box = sns.boxplot(x= 'gre', data= df, orient= 'v').set_title("GRE Box Plot")
gre_box.figure.savefig("D:\\Users\\GRE Box Plot.png")

model= smf.logit(formula='admit ~ gre + gpa + C(rank)', data= df).fit()
model.summary()
    
    
# GETTING THE ODDS RATIOS, Z-VALUE, AND 95% CI
model_odds = pd.DataFrame(np.exp(model.params), columns= ['OR'])
model_odds['z-value']= model.pvalues
model_odds[['2.5%', '97.5%']] = np.exp(model.conf_int())
model_odds
