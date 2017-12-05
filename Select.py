import re
import csv
import os

import Check


def isTableExist(tableName):
    if os.path.exists(tableName+'.csv'):
        return True
    else:
        return False

def filterItem(item):
    for key in item:
        if item[key].startswith("\'") and item[key].endswith("\'"):
            item[key] = item[key][1:-1]
    return item

def getColumns(tableName):
    with open(tableName + '.csv', 'r') as f:
        file = csv.reader(f)
        rows = [row for row in file]
        flag = False
        columns = list()
        for row in rows:
            if flag:
                columns.append(row[0])
            flag = True
        return columns


def getIndexList(tableName):
    with open('index.csv', 'r') as f:
        file = csv.reader(f)
        rows = [row for row in file]
        for row in rows:
            if row[0] == tableName:
                indexList = row[1].split(',')
                break
        del indexList[0]
        indexList = [int(x) - 1 for x in indexList]
        return indexList


def SimpleSelect(tableName, values):
    all_data = list()
    if '*' in values:
        columns = getColumns(tableName)
        indexList = getIndexList(tableName)
        dataList = list()
        with open('data.csv', 'r') as f:
            file = csv.reader(f)
            rows = [row for row in file]
            for i in range(len(rows)):
                if i in indexList:
                    dataList.append(rows[i])
        for d in dataList:
            data = dict()
            for i in range(len(columns)):
                if d[i] is not None:
                    data[columns[i]] = d[i]
                else:
                    data[columns[i]] = ''
            all_data.append(data)
    else:
        columns = getColumns(tableName)
        indexList = getIndexList(tableName)
        dataList = list()
        with open('data.csv', 'r') as f:
            file = csv.reader(f)
            rows = [row for row in file]
            for i in range(len(rows)):
                if i in indexList:
                    dataList.append(rows[i])
        for d in dataList:
            data = dict()
            for i in range(len(columns)):
                if d[i] is not None:
                    data[columns[i]] = d[i]
                else:
                    data[columns[i]] = ''
            all_data.append(data)
        for item in all_data:
            for column in columns:
                if column not in values:
                    del item[column]
    return all_data


def getFilterData(all_data, filters, param):
    new_data = list()
    if param == '!=':
        for data in all_data:
            if not data[filters[0]] == filters[1]:
                new_data.append(data)
        return new_data
    elif param == '>=':
        for data in all_data:
            if data[filters[0]] >= filters[1]:
                new_data.append(data)
        return new_data
    elif param == '<=':
        for data in all_data:
            if data[filters[0]] <= filters[1]:
                new_data.append(data)
        return new_data
    elif param == '>':
        for data in all_data:
            if data[filters[0]] > filters[1]:
                new_data.append(data)
        return new_data
    elif param == '<':
        for data in all_data:
            if data[filters[0]] < filters[1]:
                new_data.append(data)
        return new_data
    elif param == '=':
        for data in all_data:
            if data[filters[0]] == filters[1]:
                new_data.append(data)
        return new_data
    else:
        return all_data


def SimpleSelectCondition(tableName, values, conditions):
    all_data = list()
    columns = getColumns(tableName)
    indexList = getIndexList(tableName)
    dataList = list()
    with open('data.csv', 'r') as f:
        file = csv.reader(f)
        rows = [row for row in file]
        for i in range(len(rows)):
            if i in indexList:
                dataList.append(rows[i])
    for d in dataList:
        data = dict()
        for i in range(len(columns)):
            if d[i] is not None:
                data[columns[i]] = d[i]
            else:
                data[columns[i]] = ''
        all_data.append(data)
    if '!=' in conditions:
        filters = conditions.split('!=')
        filters[0] = filters[0].lstrip().rstrip()
        filters[1] = filters[1].lstrip().rstrip()
        all_data = getFilterData(all_data, filters, '!=')
    elif '>=' in conditions:
        filters = conditions.split('>=')
        filters[0] = filters[0].lstrip().rstrip()
        filters[1] = filters[1].lstrip().rstrip()
        all_data = getFilterData(all_data, filters, '>=')
    elif '<=' in conditions:
        filters = conditions.split('<=')
        filters[0] = filters[0].lstrip().rstrip()
        filters[1] = filters[1].lstrip().rstrip()
        all_data = getFilterData(all_data, filters, '<=')
    elif '>' in conditions:
        filters = conditions.split('>')
        filters[0] = filters[0].lstrip().rstrip()
        filters[1] = filters[1].lstrip().rstrip()
        all_data = getFilterData(all_data, filters, '>')
    elif '<' in conditions:
        filters = conditions.split('<')
        filters[0] = filters[0].lstrip().rstrip()
        filters[1] = filters[1].lstrip().rstrip()
        all_data = getFilterData(all_data, filters, '<')
    elif '=' in conditions:
        filters = conditions.split('=')
        filters[0] = filters[0].lstrip().rstrip()
        filters[1] = filters[1].lstrip().rstrip()
        all_data = getFilterData(all_data, filters, '=')
    elif conditions[0] == str(False):
        all_data.clear()
    elif conditions[0] == str(True):
        all_data
    else:
        print('SQL 语句解析失败')
        return
    if '*' in values:
        return all_data
    else:
        for item in all_data:
            for column in columns:
                if column not in values:
                    del item[column]
        return all_data



def selectData(username, sql):
    # if sql.lstrip().startswith('select * '):
    #     selectAll(sql)
    if 'where' not in sql:
        matchObj = re.search(r'^select (.*) from (.*);$', sql)
        if matchObj:
            tableNames = matchObj.group(2).split(',')
            tableNames = [tableName.lstrip().rstrip() for tableName in tableNames]
            for tableName in tableNames:
                if not Check.checkGrant(username, tableName, 'select'):
                    print('权限不足')
                    return
            values = matchObj.group(1).split(',')
            values = [value.lstrip().rstrip() for value in values]
            if len(tableNames) == 1:
                tableName = tableNames[0]
                isTable = isTableExist(tableName)
                if not isTable:
                    print('TABLE '+tableName+' HAS NOT EXIST')
                    return
                else:
                    datas = SimpleSelect(tableName,values)
                    if len(datas) == 0:
                        print('0 rows')
                    else:
                        for item in datas:
                            print(filterItem(item))
            else:
                print('SQL 语句错误')
                return
        else:
            print('SQL 解析错误')
            return
    else:
        matchObj = re.match(r'^select (.*) from (.*) where (.*);$', sql)
        if matchObj:
            tableNames = matchObj.group(2).split(',')
            tableNames = [tableName.lstrip().rstrip() for tableName in tableNames]
            for tableName in tableNames:
                if not Check.checkGrant(username, tableName, 'select'):
                    print('权限不足')
                    return
            values = matchObj.group(1).split(',')
            values = [value.lstrip().rstrip() for value in values]
            conditions = matchObj.group(3)
            conditions.lstrip().rstrip()
            if len(tableNames) == 1:
                tableName = tableNames[0]
                if 'and' not in conditions and 'or' not in conditions:
                    datas = SimpleSelectCondition(tableName, values, conditions)
                    if len(datas) == 0:
                        print('0 rows')
                    else:
                        for item in datas:
                            print(filterItem(item))
                elif 'and' in conditions:
                    conditions = conditions.split('and')
                    conditions[0] = conditions[0].lstrip().rstrip()
                    conditions[1] = conditions[1].lstrip().rstrip()
                    data1 = SimpleSelectCondition(tableName, values, conditions[0])
                    data2 = SimpleSelectCondition(tableName, values, conditions[1])
                    datas = [data for data in data1 if data in data2]
                    if len(datas) == 0:
                        print('0 rows')
                    else:
                        for item in datas:
                            print(filterItem(item))
                elif 'or' in conditions:
                    conditions = conditions.split('or')
                    conditions[0] = conditions[0].lstrip().rstrip()
                    conditions[1] = conditions[1].lstrip().rstrip()
                    data1 = SimpleSelectCondition(tableName, values, conditions[0])
                    data2 = SimpleSelectCondition(tableName, values, conditions[1])
                    datas = [data for data in data1 if data not in data2]+[data for data in data2 if data not in data1]
                    if len(datas) == 0:
                        print('0 rows')
                    else:
                        for item in datas:
                            print(filterItem(item))
            else:
                print('功能暂未实现')






# select * from student;
# select * from test;
# select * from student where id=1 and name = 'aaa';
# select id from student;
# select id,name from test;
# select name from test;
