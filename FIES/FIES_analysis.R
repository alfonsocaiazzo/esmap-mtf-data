install.packages("RM.weights") 
install.packages('psychotools')
install.packages('Hmisc')
source("/Users/chaix/Desktop/Hedera_desk/FIES/RM.weights/R/RM.w.R")
source("/Users/chaix/Desktop/Hedera_desk/FIES/RM.weights/R/prob.assign.R")
library(psychotools)
library(RM.weights)
library(Hmisc)
XX = data.FAO_country1[,1:8]
wt = data.FAO_country1$wt


# IRT: methodology used to analyse responses to survey or test questions.
# Rash model: one of the IRT model, provides set of statistical tools: assess the suitability of a set of survey items for scale construction
# create a scale from the items, and compare performance of a scale in various populations and survey contexts.
# doesn't give an absolute scale but relative one, specific to the given dataset
# items and respondents have relative position on the scale of severity, expressed by their respective parameters.
# that's why: not possible to make direct comparison among several dataset: need to use the step EQUATING
#a respondent who answers yes to a question can be expected to also answer yes all less severe questions.
#a respondent who answers no to a question is expected to also answer no to all more severe questions.
#This means that once the order of severity of the eight questions has been established, 
#specific patterns of responses by individual respondents can be considered more or less 
#to "fit" the logic of the model.
#The item parameter is estimated based on the overall pattern of responses given by all respondents. A question representing a less severe experience will have a smaller parameter value, whereas a question representing a more severe experience will have a larger parameter value.
#The relative severity of the items is determined based upon the understanding that the more severe an item is, the less likely respondents are to report it.
#Another way to understand this concept is that the proportion of affirmative responses to a given item, in any sample, must be inversely related to the severity of the item.
#Another way to understand this concept is that the proportion of affirmative responses to a given item, in any sample, must be inversely related to the severity of the item.
#Characteritic of the scale: no absolute interpretation of the numerical values, also, the scale is specific to a particular application
# The origin: set as the mean if the item severity parameters
# Fit weighted Rasch:
rr = RM.w(XX, wt)
View(rr)
pp = prob.assign(rr, sthres = seq(-5, 5, 0.01))
