import re
import csv
import os

import Check


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


def isPrimaryKey(tableName, columnType):
	with open(tableName+'.csv', 'r') as f:
		file = csv.reader(f)
		rows = [row for row in file]
		flag = False
		for i in range(len(rows)):
			if flag:
				if rows[i][0] == columnType and rows[i][2] == str(True):
					return i-1
			flag = True
	return -1


def checkRepeat(isPrimary, tableName, indexList, param):
	dataList = list()
	with open('data.csv', 'r') as f:
		file = csv.reader(f)
		rows = [row for row in file]
		for i in range(len(rows)):
			if i in indexList:
				dataList.append(rows[i])
		for data in dataList:
			if data[isPrimary] == param:
				return True
	return False


def getItemIndex(param, tableName):
	with open(tableName+'.csv', 'r') as f:
		file = csv.reader(f)
		rows = [row for row in file]
		for i in range(len(rows)):
			if rows[i][0] == param:
				return i-1
	return -1


def getUpdateIndex(tableName, conditions):
	updateList = list()
	ItemIndex = getItemIndex(conditions[0], tableName)
	indexList = getIndexList(tableName)
	with open('data.csv', 'r') as f:
		file = csv.reader(f)
		rows = [row for row in file]
	for index in indexList:
		if rows[index][ItemIndex] == conditions[1]:
			updateList.append(index)
	return updateList

def updateItem(tableName, values, conditions):
	indexList = getIndexList(tableName)
	if '=' in conditions:
		conditions = conditions.split('=')
		for condition in conditions:
			condition = condition.lstrip().rstrip()
		for value in values:
			columnType = value.split('=')[0].lstrip().rstrip()
			isPrimary = isPrimaryKey(tableName, columnType)
			if isPrimary>=0:
				isRepeat = checkRepeat(isPrimary, tableName, indexList, value.split('=')[1].lstrip().rstrip())
				if isRepeat:
					print(columnType+' IS NOT REPEAT')
					return None
				else:
					Valueindex = getItemIndex(columnType, tableName)
					conditionindex = getItemIndex(conditions[0], tableName)
					if Valueindex<0:
						print(columnType +' IS NOT EXIST')
						return None
		with open('data.csv', 'r') as f:
			file = csv.reader(f)
			rows = [row for row in file]
		updateList = getUpdateIndex(tableName, conditions)
		for index in updateList:
			for value in values:
				item = value.split('=')[0].lstrip().rstrip()
				itemIndex = getItemIndex(item, tableName)
				rows[index][itemIndex] = value.split('=')[1].lstrip().rstrip()
		try:
			with open('data.csv', 'w', newline='') as f:
				file = csv.writer(f)
				for row in rows:
					file.writerow(row)
			print('CHANGED '+str(len(updateList))+' ROWS')
			return
		except Exception as e:
			print(e)
			return 
	else:
		print('暂未实现该功能')
		return None

def isTableExist(tableName):
	if os.path.exists(tableName+'.csv'):
		return True
	else:
		return False


def updateData(username, sql):
	if 'where' in sql:
		matchObj = re.search(r'^update (.*) set (.*) where (.*);$', sql)
		if matchObj:
			tableName = matchObj.group(1)
			if not Check.checkGrant(username, tableName, 'update'):
				print('权限不足')
				return
			values = matchObj.group(2)
			values = values.split(',')
			for value in values:
				value = value.lstrip().rstrip()
			conditions = matchObj.group(3)
			isTable = isTableExist(tableName)
			if isTable:
				datas = updateItem(tableName, values, conditions)

		else:
			print('sql 解析错误')
			return
	else:
		print('sql 格式错误')
		return
