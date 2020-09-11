import string
import pandas as pd
import csv
from gensim import corpora
from stop_words import safe_get_stop_words
from readability import Readability
import textstat

csv.field_size_limit(500 * 1024 * 1024) 
file1 = open('gfi_description.csv')
csv_reader = csv.reader(file1)
header = next(csv_reader) 


file2 = open('gfi_description_attributes.csv', 'w')
csv_writer = csv.writer(file2)
csv_writer.writerow(['id', 'num_url', 'num_image', 'num_code', 'num_comment', 'num_table', 'count_word_title', 'count_word_body', 'readability'])

for item in csv_reader:
	title = item[1]
	body = item[2]
	count_word_title = textstat.lexicon_count(title, removepunct=True)
	count_word_body = textstat.lexicon_count(body, removepunct=True)
	readability = textstat.coleman_liau_index(body)
	print(count_word_title, count_word_body, readability)
	csv_writer.writerow([item[0], item[3], item[4], item[5], item[6], item[7], count_word_title, count_word_body, readability])

file1.close()
file2.close()

