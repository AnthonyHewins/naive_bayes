from os import path
from numpy import median
import pickle
import pandas

email_path = "emails/lingspam_public/bare/part1/"

def get_files(file_path):
	text = open(file_path, 'r').read()
	text = text.split("  ")
	n = len(text)
	for i in range(n):
		r = text[i]
		if "\n" not in r:
			continue
		del text[i]
		x = r.split("\n")
		for j in x:
			text += [j]
	text += ["LINE_TERM"]
	i = 0
	while text[i] != "LINE_TERM":
		if text[i] == '':
			del text[i]
			continue
		text[i] = text[i].strip()
		i += 1
	del text[i]
	return sorted(text)

def create_dictionary():
	print("Creating dictionary...")
	dictionary = append_dictionary(get_files("emails/training_files.txt"))
	print("Created dictionary. Sanity check:", dictionary[0:10])
	print("Cleaning up fucked up words and data that will make no sense...")
	dictionary = clean_up(dictionary)
	print("Shitty words cleaned up.")
	print("Turning into set...")
	dictionary = set(dictionary)
	print("Turned into a set.")
	f = open("dictionary.dict", 'bw')
	pickle.dump(dictionary, f)
	print(dictionary)
	print("Dictionary written. Closing.")
	return dictionary

def clean_up(dictionary):
	delim = "$LINE_DELIMITER$X"
	dictionary += [delim]

	i=0
	while dictionary[i] != delim:
		dictionary[i] = dictionary[i].replace("\n", "")
		try:
			trimmed = dictionary[i].replace(",", "").replace("-", "").replace("/", "")
			int(trimmed)
			del dictionary[i]
		except:
			i += 1
	del dictionary[i]
	return dictionary

def append_dictionary(files):
	dictionary = set()
	exists = False
	for i in files:
		f = open(email_path + i, 'r')
		f.readline();f.readline()
		vector = f.read().split(' ')
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
