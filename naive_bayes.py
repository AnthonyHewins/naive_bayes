from time import sleep
import pandas
import numpy as np
import pickle
from init_dictionary import create_dictionary
from os.path import isfile as file_exists

test = pandas.read_csv("emails/test_data.csv", sep="\t")
data = pandas.read_csv("emails/training_data.csv", sep="\t")
test.columns = ["Spam?", "Text"]
data.columns = ["Spam?", "Text"]
train_y, train_x = data.iloc[0:, 0], data.iloc[0:, 1]
test_y, test_x = data.iloc[0:, 0], data.iloc[0:, 1]

def main():
	train()
	classify()

def train():
	dictionary = np.array(fetch_dictionary())
	p_y_is_spam = getp_y()
	p_x = getp_x()

def getp_x():
	c = 0.5 #threshold for p(x) approximation in bayes rule
	
def getp_y():
	count = 0
	for i in train_y:
		if i == "spam":
			count += 1
	return count / len(train_y)
	
def bayes_rule(p_x_given_y, p_y, p_x):
	"""
	       p(x|y)p(y)
	p(y|x)=----------
	          p(x)
	"""
	return float(p_x_given_y * p_y)/float(p_x)
	
def fetch_dictionary():
	if not file_exists("dictionary.dict"):
		print("Dictionary didn't exist, creating...")
		create_dictionary()
		print("Sleeping for a second to avoid conflicts with file IO.")
		sleep(1)		
	try: dictionary = pickle.load(open("dictionary.dict", 'br'))
	except: print("File IO error loading dictionary in naive_bayes.py")
	print("Successfully loaded dictionary in naive_bayes.")
	return dictionary
