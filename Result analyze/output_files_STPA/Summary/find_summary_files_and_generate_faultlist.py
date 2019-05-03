import os
import re


def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result


root_directory = '../'
file_name = 'summary.csv'
search_result = find_all(file_name, root_directory)
result = str(search_result).split(',')

print "search result:\n"

pattern = re.compile(r'\d+')
index =[]
title = []
for line in result:
    line = line.split('/')
    title.append(line[1])
    lineNum = pattern.findall(line[1])
    index.append(int(lineNum[0])) 

for i in range(len(index)-1):
    for j in range(i+1,len(index)):
        if index[i] > index[j]:
            temp =index[i]
            index[i] = index[j]
            index[j] = temp
            temp =title[i]
            title[i]=title[j]
            title[j]=temp
fp =open("fault_list.txt",'w')
for line in title:
    fp.write(line+'\n')
    print line
fp.close

