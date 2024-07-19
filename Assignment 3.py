#Rachel Lee
#0695297
#COIS 4550H
#Assignment #3
#April 11, 2024


#Program Description: This program uses naive bayes for classification. It will split the training and testing to 80% and 20% respectfully.
#it will calculate the test set accuracy 
#this program does not use any library for the inference/classification

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

data_csv = 'adult.csv' #making a data_csv so it can be easily usable for other csv files
class_variable = 'income' #making a class_variable so it can be easily usable for other csv files

#csv obtained is from: https://archive.ics.uci.edu/dataset/2/adult

data_adult_csv = pd.read_csv(data_csv) #loading the data

sample_data = data_adult_csv.sample(frac=0.05)  # this was to sample a very, very small part of the data (5%). The adult.csv was a big chungus and my laptop is a potato :(
training_data, testing_data = train_test_split(sample_data, test_size=0.2)# spliting the data into the trainint and testing sets to be 80/20 respectively 


# creating a method of the naive bayes
#reference: https://www.datacamp.com/tutorial/naive-bayes-scikit-learn
#another reference: https://machinelearningmastery.com/naive-bayes-classifier-scratch-python/
def naive_bayes(training_data, test_instance):

    X_train = training_data.drop(class_variable, axis=1)  #sepearting the class variable. The 'drop' removes 'classvariable' from the data frame
    y_train = training_data[class_variable]  

    class_probabilities = y_train.value_counts(normalize=True)  # calculating the prior probabilities

    likelihoods = {}  # calculating the likelihood probabilities using a dictionary
    for class_ in class_probabilities.index: #looping over each feature in the training data
        likelihoods[class_] = {}
        for feature in X_train.columns:
            likelihoods[class_][feature] = X_train[y_train==class_][feature].value_counts(normalize=True)

    #print ("Class probabilities:",class_probabilities)#testing the class probability by printing it

    output_class = None  # classifying the test instance
    max_posterior_prob = 0
    for class_ in class_probabilities.index: #looping over each class in training data
        posterior_prob = class_probabilities[class_] #calculating the prior probilbity
        for feature in X_train.columns:
            if feature in test_instance and test_instance[feature] in likelihoods[class_][feature]: 
                posterior_prob *= likelihoods[class_][feature][test_instance[feature]] #multplies the probability with the likelikhood
            else:
                posterior_prob *= 1e-5  # smoothing it: making a very small number instead of putting zero to eliminate noises. reference: https://plotly.com/python/smoothing/
        if posterior_prob > max_posterior_prob:
            max_posterior_prob = posterior_prob #updates the maximum probability with the calculated probability
            output_class = class_ #updates the class

    return output_class


predictions = [naive_bayes(training_data, row) for _, row in testing_data.iterrows()] #classifying each instance in the test set. Using iterrows because testing_data is a string. Reference: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iterrows.html

accuracy = accuracy_score(testing_data['income'], predictions) # calculating the accuracy

print('The test set accuracy is:', accuracy) #printing out the accuracy