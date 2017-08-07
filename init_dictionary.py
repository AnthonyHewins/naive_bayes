from os import path
from numpy import median
import pickle
import pandas

encoding=""

def get_csv():
	csv = "emails/training_data.csv"
	try: return pandas.read_csv(csv, sep="\t").iloc[0:,1]
	except:
		print("error getting training data, path error")
		exit()

def create_dictionary():
	print("Creating dictionary...")
	dictionary = append_dictionary(get_csv())
	print("Created dictionary. Sanity check:", dictionary[0:10])
	print("Sorting dictionary...")
	dictionary = sorted(dictionary)
	print("Sorted. Sanity check:", dictionary[0:10])
	f = open("dictionary.dict", 'bw')
	pickle.dump(dictionary, f)
	print("Dictionary written. Closing.")

def append_dictionary(allText):
	dictionary = set()
	exists = False
	for i in allText:
		vector = i.split(' ')
		for j in vector:
			dictionary.add(j)
	ordered_dictionary = []
	for i in dictionary:
		ordered_dictionary += [i]
	return ordered_dictionary

if __name__ == "__main__":
	if path.isfile("dictionary.dict"):
		if input("Dictionary already exists, overwrite? (y/n)").lower() != 'y': exit()
	create_dictionary()
