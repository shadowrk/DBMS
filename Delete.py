import re
import os
import csv

import Check


def deleteAllData(tableName):
	with open('index.csv', 'r') as f:
		file = csv.reader(f)
		rows = [row for row in file]
		rowSum = 0
		for row in rows:
			if row[0] == tableName:
				rowSum = len(row[1].split(','))-1
				row[1] = ','.join(list())
				row[2] = 0
	try:
		with open('index.csv', 'w', newline='') as f:
			file = csv.writer(f)
			for row in rows:
				file.writerow(row)
		print('DELETE SUCCESSFUL, DELETE '+str(rowSum)+' ROWS')
		return
	except Exception as e:
		print(e)
		return


def getColumnIndex(tableName, param):
	with open(tableName+'.csv', 'r') as f:
		file = csv.reader(f)
		rows = [row for row in file]
		for i in range(len(rows)):
			if rows[i][0] == param:
				return i-1
	return -1


def deleteFilter(tableName, conditions, param):
	new_index = list()
	indexList = list()
	with open('index.csv', 'r') as f:
		file = csv.reader(f)
		rows = [row for row in file]
		for row in rows:
			if row[0] == tableName:
				indexList = row[1].split(',')
				break
		del indexList[0]
		indexList = [int(x) - 1 for x in indexList]
	with open('data.csv', 'r') as f:
		file = csv.reader(f)
		rows = [row for row in file]
	if param == '>=':
		conditions = conditions.split('>=')
		for condition in conditions:
			condition = condition.lstrip().rstrip()
		columnIndex = getColumnIndex(tableName, conditions[0])
		for index in indexList:
			if rows[index][columnIndex] >= conditions[1]:
				new_index.append(index)
		newIndexList = [index for index in indexList if index not in new_index]
	elif param == '<=':
		conditions = conditions.split('<=')
		for condition in conditions:
			condition = condition.lstrip().rstrip()
		columnIndex = getColumnIndex(tableName, conditions[0])
		for index in indexList:
			if rows[index][columnIndex] <= conditions[1]:
				new_index.append(index)
		newIndexList = [index for index in indexList if index not in new_index]
	elif param == '!=':
		conditions = conditions.split('!=')
		for condition in conditions:
			condition = condition.lstrip().rstrip()
		columnIndex = getColumnIndex(tableName, conditions[0])
		for index in indexList:
			if rows[index][columnIndex] == conditions[1]:
				new_index.append(index)
		newIndexList = new_index
	elif param == '>':
		conditions = conditions.split('>')
		for condition in conditions:
			condition = condition.lstrip().rstrip()
		columnIndex = getColumnIndex(tableName, conditions[0])
		for index in indexList:
			if rows[index][columnIndex] > conditions[1]:
				new_index.append(index)
		newIndexList = [index for index in indexList if index not in new_index]
	elif param == '<':
		conditions = conditions.split('<')
		for condition in conditions:
			condition = condition.lstrip().rstrip()
		columnIndex = getColumnIndex(tableName, conditions[0])
		for index in indexList:
			if rows[index][columnIndex] < conditions[1]:
				new_index.append(index)
		newIndexList = [index for index in indexList if index not in new_index]
	elif param == '=':
		conditions = conditions.split('=')
		for condition in conditions:
			condition = condition.lstrip().rstrip()
		columnIndex = getColumnIndex(tableName, conditions[0])
		for index in indexList:
			if rows[index][columnIndex] == conditions[1]:
				new_index.append(index)
		newIndexList = [str(index+1) for index in indexList if index not in new_index]
	else:
		print('DELETE FAILURE')
		newIndexList = [str(index) for index in indexList]
	try:
		newIndexList.insert(0, '')
		with open('index.csv', 'r') as f:
			file = csv.reader(f)
			rows = [row for row in file]
		for row in rows:
			if row[0] == tableName:
				row[1] = ','.join(newIndexList)
				row[2] = len(newIndexList)-1
				break
		with open('index.csv', 'w', newline='') as f:
			file = csv.writer(f)
			for row in rows:
				file.writerow(row)
		print('DELETE SUCCESSFUL, DELETE '+str(len(indexList)+1-len(newIndexList))+' ROWS')
	except Exception as e:
		print(e)
	return






def deleteCondition(tableName, conditions):
	if 'and' not in conditions and 'or' not in conditions:
		if '>=' in conditions:
			deleteFilter(tableName, conditions, '>=')
		elif '<=' in conditions:
			deleteFilter(tableName, conditions, '<=')
		elif '!=' in conditions:
			deleteFilter(tableName, conditions, '!=')
		elif '>' in conditions:
			deleteFilter(tableName, conditions, '>')
		elif '<' in conditions:
			deleteFilter(tableName, conditions, '<')
		elif '=' in conditions:
			deleteFilter(tableName, conditions, '=')
		return


def isTableExist(tableName):
	if os.path.exists(tableName+'.csv'):
		return True
	else:
		return False


def deleteData(username, sql):
	if 'where' not in sql:
		matchObj = re.search(r'^delete from (.*);$', sql)
		if matchObj:
			tableName = matchObj.group(1)
			if not Check.checkGrant(username, tableName, 'delete'):
				print('权限不足')
				return
			isTable = isTableExist(tableName)
			if isTable:
				deleteAllData(tableName)
			else:
				print(tableName+' HAS NOT EXIST')
				return

		else:
			print('SQL 解析失败')
			return
	else:
		matchObj = re.search(r'delete from (.*) where (.*);$', sql)
		if matchObj:
			tableName = matchObj.group(1)
			if not Check.checkGrant(username, tableName, 'delete'):
				print('权限不足')
				return
			conditions = matchObj.group(2)
			isTable = isTableExist(tableName)
			if isTable:
				deleteCondition(tableName, conditions)
			else:
				print(tableName+' HAS NOT EXIST')
				return
		else:
			print('SQL 解析失败')
			return
