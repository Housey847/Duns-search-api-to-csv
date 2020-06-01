# -*- coding: utf-8 -*-
"""
Created on Fri May 29 11:58:54 2020

@author: z003send
"""

import requests
import json
import csv


responses = list() # stores responses 
duns_list = list() # stores duns
csv_columns = ['duns','companyIdentifier','businessIdentifier','nni','entityName','address','entityType','entityTypeDescription','status','statusDescription']
csv_file = "data.csv"
filtered_dictionary = {}
payload = {}
headers = {
        'Authorization': 'Bearer Past JWT here',
        'Cookie': ''
        }
    
    
line_count=0


with open('CRM Duns List.csv') as csv_file_open:
    csv_reader = csv.reader(csv_file_open, delimiter=',')
    for row in csv_reader:
            duns_list.append(f'{row[0]}')
            line_count += 1
    print(f'Processed {line_count} lines.')
#print(duns_list[7:10])
#duns_list=duns_list[5000:5314]
for dun in duns_list:
    url = 'https://express.illion.com.au/api/companysearch/?country=AU&searchType=0&searchCriteria={}'.format(dun)

    try: 
        response = requests.request("GET", url, headers=headers, data = payload)
        data =json.loads(response.text.encode('utf8'))
        data[0]['address']=data[0]['address']['postCode']
        responses.append(data[0])
        print(dun)
#        for key, value in data[0].items():
#            if (key == 'duns' or key == 'businessIdentifier' or key == 'entityName'):filtered_dictionary[key] = value

    except KeyError:
        print(dun + " KeyError")
    except ConnectionError:
        print(dun + " ConnectionError error")
    except:
        print(dun + " Other")

print(responses)



try:
    with open(csv_file, 'w',newline='\n') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames= csv_columns)
        writer.writeheader()
        for data in responses:
            writer.writerow(data)
except IOError:
    print("I/O error")
    

