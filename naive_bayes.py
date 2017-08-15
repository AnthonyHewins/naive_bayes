from time import sleep
import pandas
import numpy as np
import pickle
import init_dictionary
from os.path import isfile as file_exists

def get_file_classifications():
	text = init_dictionary.get_files("emails/training_files.txt")
	spam = []
	ham = []
	spam_count = 0
	ham_count = 0
	for i in text:
		if i[0] == 's':
			spam += [i]
			spam_count += 1
		else:
			ham += [i]
			ham_count += 1
	total = spam_count + ham_count
	print("Spam files:", spam_count, "| Ham files:", ham_count, "| Total:", total, "| % spam:", spam_count / total)
	return spam, ham, spam_count, ham_count, total

data_path = "emails/lingspam_public/bare/part1/"
test_path = "emails/lingspam_public/bare/part2/"
spam_list, ham_list, spam_count, ham_count, file_count = get_file_classifications()

def main():
	spam_vector, ham_vector, dictionary, dictionary_set, lookup = train()
	classify(spam_vector, ham_vector, dictionary, dictionary_set, lookup)

def classify(spam_vector, ham_vector, dictionary, dictionary_set, lookup):
	f = open(test_path + "5-1439msg1.txt", 'r')
	correct_answer = "ham" #"spam" if test_files[0][0] == 's' else "ham"
	f.readline();	f.readline()
	email = f.read().split(' ')
	
	#p(y=spam)
	p_y = spam_count / file_count
	print("p(y=spam)=" + str(p_y))
	
	#p(x|y=spam)
	p_x_y_spam = vector_probability(spam_vector, email, dictionary, dictionary_set, spam_count, lookup)
	print("p(x|y=spam)=" + str(p_x_y_spam))
	
	#p(x|y=ham)
	p_x_y_ham = vector_probability(ham_vector, email, dictionary, dictionary_set, ham_count, lookup)
	print("p(x|y=ham)=" + str(p_x_y_ham))
	
	p_x = (p_y * p_x_y_spam) + ((ham_count / file_count) * p_x_y_ham)
	print("p(x)=" + str(p_x))
	prediction = bayes_rule(p_x_y_spam, p_y, p_x)
	final_answer = predict(prediction)
	print("p(y=spam|x) = " + str(prediction * 100) + "% -- " + final_answer)
	
	if final_answer == correct_answer:
		print("Correct!")
	else:
		if final_answer == "push; not enough data to tell.":
			print("Algorithm error, we won't count that...")
		else:
			print("Wrong")
			
	
def train():
	#get the dictionary as a set and a vector
	dictionary_set = fetch_dictionary()
	dictionary = np.array(list(dictionary_set))
	
	#Get some numbers for the bayes calculation
	spam_vector, ham_vector, lookup = parse_words(dictionary, dictionary_set)
	print("Got word vectors for spam and ham and a handy dictionary for word lookup.")

	return spam_vector, ham_vector, dictionary, dictionary_set, lookup

	
def vector_probability(vector, email, dictionary, dictionary_set, classification_count, lookup):
	n = len(dictionary)
	probability = 1
	words = set(email)
	for i in dictionary:
		if i in words:
			r = (vector[lookup[i]] / classification_count)
			if r == 0.0: continue
			probability *= r
		else:
			r = (1 - (vector[lookup[i]] / classification_count))
			if r == 1: continue
			probability *= r
	return probability
	
def parse_words(dictionary, dictionary_set):
	n = len(dictionary)
	lookup = dict()
	spam_vector = [0] * n
	ham_vector = [0] * n

	for i in range(n):
		lookup[dictionary[i]] = i #build dictionary to make this entire function close to ~O(2n)	 

	spam_vector = word_count(spam_list, spam_vector, dictionary_set, lookup)
	ham_vector = word_count(ham_list, ham_vector, dictionary_set, lookup)
	
	return spam_vector, ham_vector, lookup

def word_count(lst, vector, dictionary_set, lookup):
	for i in lst:
		f = open(data_path + i, 'r')
		text = set(f.read().split(' '))
		for i in text:
			if i not in dictionary_set:
				continue
			vector[lookup[i]] += 1
	return vector

def predict(probability):
	if probability < 0.5:
		return "ham"
	elif probability > 0.5:
		return "spam"
	else:
		return "push; not enough data to tell."

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
		init_dictionary.create_dictionary()
		print("Sleeping for a second to avoid conflicts with file IO.")
		sleep(1)		
	try: dictionary = pickle.load(open("dictionary.dict", 'br'))
	except:
		print("File IO error loading dictionary in naive_bayes.py")
		exit()
	print("Successfully loaded dictionary in naive_bayes.")
	return dictionary
	

main()
