# this file is used to download issue report
import requests
import json
import csv

file1 = open('data/gfi.csv')
csv_reader = csv.reader(file1)
header = next(csv_reader)  

file2 = open('gfi_description.csv', 'w', newline='')
csv_writer = csv.writer(file2)
csv_writer.writerow(['id', 'title', 'body'])
i = 0
username = '***'
auth_token = '****'
for row in csv_reader:
	i += 1
	request_url = "%s%s%s"%(row[1], '/issues/', row[2])
	print(i, request_url)
	response = requests.get(request_url, auth=(username, auth_token)).text
	info = json.loads(response)
	if 'title' in info.keys() and 'body' in info.keys():
		csv_writer.writerow([row[0], info['title'], info['body']])
	elif 'title' in info.keys():
		csv_writer.writerow([row[0], info['title'], ''])
file1.close()
file2.close()
