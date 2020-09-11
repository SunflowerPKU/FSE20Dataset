import requests
import json
import csv

file1 = open('issue_url.csv')
csv_reader = csv.reader(file1)
header = next(csv_reader)  

labels = []
file2 = open('gfi_label.csv')
csv_reader2 = csv.reader(file2)
header = next(csv_reader2)  
for row in csv_reader2:
	labels.append(row[0])
print(labels)


file3 = open('issue_labeler.csv', 'a+', newline='')
csv_writer = csv.writer(file3)
csv_writer.writerow(['id', 'labeler_login', 'label_time'])
i = 0
username = '***'
auth_token = '*****'
for row in csv_reader:
	i += 1
	if i > 7571:
		request_url = "%s%s%s%s"%(row[2], '/issues/', row[1], '/events')
		print(i, request_url)
		response = requests.get(request_url, auth=(username, auth_token)).text
		info = json.loads(response)
		if not isinstance(info, list):
			print('Not found!!!')
			continue
		for item in info:
			if item["event"] == "labeled":
				if item["label"]["name"] in labels:
					print([row[0], item["actor"]["login"], item["created_at"]])
					csv_writer.writerow([row[0], item["actor"]["login"], item["created_at"]])
file1.close()
file2.close()
