import json
import csv

#import data from .json into dictionary
with open('person.json', 'r') as json_file:
  data = json.load(json_file)

#isolate entries data
entries = data['entries']

#create dictionary for pods
pods = {}

#create list for all cores
cores = []

#iter over entries data to extract pods and cores
for e_id, e_info in entries.items():   
    for key in e_info:
        core_list_entry = list(map(int, e_info[key].split(',')))
        cores = cores + core_list_entry
        core_list_entry.sort()
        #add pod with cores to pods dictionary
        pods[key] = core_list_entry
        
#remove duplicats from list of cores
cores = list(set(cores))
        
#import data from .mpstat
with open('r05s05-r32.mpstat', 'r') as json_file:
  data = json.load(json_file)

#isolate statistics data
statistics = data['sysstat']['hosts'][0]['statistics']

#create dictionary for storing timestamps
timestamps = {'time':[]}
for core in cores:
    timestamps[core] = []

#isolate timestamps for cores from cores list
#this is list of all cores used by pods
for i in statistics:
    timestamps['time'].append(i['timestamp'])
    count = 0
    for j in i['cpu-load']:
        if count !=0 :
            if int(j['cpu']) in cores:
                timestamps[int(j['cpu'])].append(100-j['idle'])
        count = count + 1

#show all cores
#from tabulate import tabulate
#print(tabulate(timestamps, headers='keys'))

#save elements based on pods

