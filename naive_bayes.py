from time import sleep
import pandas
import numpy as np
import pickle
from init_dictionary import create_dictionary
from os.path import isfile as file_exists

test = pandas.read_csv("emails/test_data.csv", sep="\t")
data = pandas.read_csv("emails/training_data.csv", sep="\t")
#test.columns = ["Spam?", "Text"]
#data.columns = ["Spam?", "Text"]
train_y, train_x = data.iloc[0:, 0], data.iloc[0:, 1]
test_y, test_x = data.iloc[0:, 0], data.iloc[0:, 1]

def main():
	train()

def train():
	#get the dictionary as a set and a vector
	dictionary_set = fetch_dictionary()
	dictionary = np.array(list(dictionary_set))
	
	#Get some numbers for the bayes calculation
	n = len(train_x)
	spam_vector, ham_vector, num_spam = get_vector(dictionary)
	num_ham = len(train_y) - num_spam

	#p(y=spam)
	p_y = num_spam / n

	email = test_x[0]
	correct_answer = test_y[0]
	
	#p(x|y=spam)
	p_x_y_spam = vector_probability(spam_vector, email, dictionary, dictionary_set, num_spam)

	#p(x|y=ham)
	p_x_y_ham = vector_probability(ham_vector, email, dictionary, dictionary_set, num_ham)

	print(bayes_rule(p_x_y_spam, p_y, (p_y * p_x_y_spam) + ((num_ham / n) * p_x_y_ham)))
	

def vector_probability(vector, email, dictionary, dictionary_set, classification_count):
	n = len(dictionary)
	probability = 1
	for i in email:
		if i not in dictionary_set:
			continue
		for j in range(n):
			if i == dictionary[j]:
				probability *= (vector[j] / classification_count)
			else:
				probability *= (1 - (vector[j] / classification_count))
	return probability
	
def get_vector(dictionary):
	n = len(dictionary)
	lookup = dict()
	spam_vector = [0] * n
	ham_vector = [0] * n
	num_spam = 0
	for i in range(n):
		if train_y.iat[i] == "spam":
			vector = spam_vector
			num_spam += 1
		else:
			vector = ham_vector

		words = set(train_x.iat[i])
		for j in words:
			if j in lookup:
				vector[lookup[j]] += 1
				continue
			for k in range(n):
				lookup[j] = k
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

main()
