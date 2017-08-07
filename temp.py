f = open("emails/training_data.csv", 'r')
text = f.read().replace("-_+", "\t")
f = open("emails/training_data.csv", 'w')
f.write(text)

f = open("emails/test_data.csv", 'r')
text = f.read().replace("-_+", "\t")
f = open("emails/test_data.csv", 'w')
f.write(text)
