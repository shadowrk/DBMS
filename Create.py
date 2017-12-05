import re
import csv
import os


def isPrimaryKey(item):
    if 'PRIMARY KEY' in item:
        return True
    else:
        return False

def isNull(item):
    if 'NOT NULL' in item:
        return False
    else:
        return True

def createTable(username, sql):
    matchObj = re.search(r'^create table (.*) \(.*\);$', sql, re.I)
    if matchObj:
        tableName = matchObj.group(1)
        index = sql.find('(')
        tableKeys = sql[index+1:-2]
        tableKeys = tableKeys.split(', ')
        if not os.path.exists(tableName+'.csv'):
            try:
                with open(tableName+'.csv', 'w', newline='') as f:
                    file = csv.writer(f)
                    tableHeader = ['key', 'type', 'isPrimary', 'isNull']
                    file.writerow(tableHeader)
                    KeyList = list()
                    for item in tableKeys:
                        item.lstrip()
                        item.rstrip()
                        key = item.split(' ')[0]
                        k_type = item.split(' ')[1]
                        isPrimary = isPrimaryKey(item)
                        is_null = isNull(item)
                        KeyList.append([key, k_type, isPrimary, is_null])
                    for i in KeyList:
                        file.writerow(i)
                with open('data.csv', 'w', newline='') as f:
                    file = csv.writer(f)
                    # file.writerow(['--'+tableName+'--'])
                with open('index.csv', 'a', newline='') as f:
                    # table_name, index, sum
                    file = csv.writer(f)
                    l = list()
                    file.writerow([tableName, ','.join(l), 0])
                    print('CREATE TABLE '+tableName+' SUCCESSFUL')
                    return
            except Exception as e:
                print(e)
                return
        else:
            print('TABLE '+tableName+' HAS EXIST')
            return
    else:
        print('sql 语句格式错误')
        return

#create table student (id int NOT NULL PRIMARY KEY, name char(20));
# create table test (id int, name char(20));