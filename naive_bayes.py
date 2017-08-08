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
	dictionary_set = fetch_dictionary()
	dictionary = np.array(list(dictionary_set))
	spam_vector, ham_vector, num_spam = get_vector(dictionary)
	num_ham = len(train_y) - num_spam
	
	i = test_x[0].split(" ")
	p_x = getp_x(i)

def get_vector(dictionary):
	n = len(dictionary)
	spam_vector = [0] * n
	ham_vector = [0] * n
	num_spam = 0
	for i in data:
		if i[0] == "spam":
			vector = spam_vector
			num_spam += 1
		else:
			vector = ham_vector

		words = set(i[1])
		for j in words:
			for k in range(n):
				if j == dictionary[k]:
					vector[k] += 1
	return spam_vector, ham_vector, num_spam
			
		
	
def getp_x(i):
	c = 0.5 #threshold for p(x) approximation in bayes rule
	
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
