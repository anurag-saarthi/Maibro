import json
import csv
 
with open('config.json',"r") as json_file:
    jsondata = json.load(json_file)
 
data_file = open('config.csv', 'w+', newline='')
csv_writer = csv.writer(data_file)
 
count = 0
for data in jsondata:
    print("done")
    if count == 0:
        header = data.keys()
        csv_writer.writerow(header)
        count += 1
    csv_writer.writerow(data.values())
 
data_file.close()