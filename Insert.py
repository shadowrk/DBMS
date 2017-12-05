import csv
import re
import os

import Check


def checkTable(tableName):
	if not os.path.exists(tableName+'.csv'):
		return False
	else:
		return True


def getNotNull(tableName):
	with open(tableName+'.csv', 'r') as f:
		file = csv.reader(f)
		flag = False
		for item in file:
			if flag:
				if not (item[3] == str(True)):
					return item[0]
			flag = True
	return None


def getColumns(tableName):
	with open(tableName+'.csv', 'r') as f:
		file = csv.reader(f)
		flag = False
		columns = []
		for item in file:
			if flag:
				columns.append(item[0])
			flag = True
		return columns


def getIndex():
	with open('data.csv', 'r') as f:
		return len(f.readlines())


def isPrimaryKey(tableName, item):
	with open(tableName+'.csv', 'r') as f:
		file = csv.reader(f)
		rows = [row for row in file]
		for i in range(len(rows)):
			if rows[i][0] == item and rows[i][2] == str(True):
				return i
	return -1


def hasRepeat(tableName, param, isPrimary):
	with open('index.csv', 'r') as f:
		index = -1
		file = csv.reader(f)
		rows = [row for row in file]
		for row in rows:
			if row[0] == tableName:
				indexList = row[1].split(',')
				break
	with open('data.csv', 'r') as f:
		file = csv.reader(f)
		rows = [row for row in file]
		for i in range(len(rows)):
			if str(i+1) in indexList:
				if rows[i][isPrimary-1] == param:
					return True
	return False

def writeData(tableName, columns, values):
	temp = dict()
	for i, j in zip(columns, values):
		temp[i] = j
	data = []
	table_columns = getColumns(tableName)
	for item in table_columns:
		isPrimary = isPrimaryKey(tableName, item)
		if isPrimary >= 0:
			if item in temp:
				isRepeat = hasRepeat(tableName, temp[item], isPrimary)
				if isRepeat:
					print(item + ' IS NOT REPEAT')
					return
				else:
					if item in temp:
						data.append(temp[item])
					else:
						data.append(None)
			else:
				print('PRIMARY KEY IS NOT  NULL')
				return
		else:
			if item in temp:
				data.append(temp[item])
			else:
				data.append(None)
	try:
		with open('data.csv', 'a', newline='') as f:
			file = csv.writer(f)
			file.writerow(data)
		index = getIndex()
		# 建立映射
		with open('index.csv', 'r') as f:
			file = csv.reader(f)
			rows = [row for row in file]
			t_sum = -1;
			for row in rows:
				if row[0] == tableName:
					row[1] = row[1].split(',')
					row[1].append(str(index))
					row[1] = ','.join(row[1])
					row[2] = int(row[2]) + 1
					t_sum = int(row[2])
		with open('index.csv', 'w', newline='') as f:
			file = csv.writer(f)
			for row in rows:
				file.writerow(row)
		print('SUCCESSFUL TO INSERT,TOTAL=' + str(t_sum))
	except Exception as e:
		print(e)
		return


def insertData(username, sql):
	matchObj = re.search(r'^insert into (.*) (\(.*\)) values (.*);$', sql, re.I)
	if matchObj:
		tableName = matchObj.group(1)
		if not Check.checkGrant(username, tableName, 'insert'):
			print('权限不足')
			return
		columns = (matchObj.group(2)[1:-1]).split(',')
		values = (matchObj.group(3)[1:-1]).split(',')
		for value in values:
			value = value.lstrip().rstrip()
		if checkTable(tableName):
			not_null_key = getNotNull(tableName)
			if not_null_key is not None:
				if not_null_key not in columns:
					print(not_null_key+' IS NOT NULL')
					return
				else:
					writeData(tableName, columns, values)
			else:
				writeData(tableName, columns, values)

		else:
			print('TABLE NOT EXIST')
			return


#insert into student (id,name) values (1,'aaa');
#insert into test (id) values (1,'test');
#insert into student (id,name) values (1,'aaa');
#insert into student (id,name) values (1,'aaa');
#insert into student (name) values ('aaa');

