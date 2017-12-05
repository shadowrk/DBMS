import operator
import re
import os
import csv
import getpass
import Create, Insert, Select
import Delete
import Update


def login(username, password):
    with open('users.txt', 'r') as f:
        for line in f.readlines():
            user = (line.strip().split('#')[0].replace('\n', ''), line.strip().split('#')[1])
            if operator.eq(user, (username, password)):
                return True
    return False


def CreateUser(sql):
	matObj = re.search('^create user (.*) with password (.*);$', sql)
	if matObj:
		username = matObj.group(1)
		password = matObj.group(2)
		with open('users.txt', 'r') as f:
			for line in f.readlines():
				if username == line.strip().split('#')[0].replace('\n', ''):
					print('用户已存在')
					return
		try:
			with open('users.txt', 'a') as f:
				f.write('\n'+username + '#' + password)
			print('用户创建成功')
		except Exception as e:
			print(e)
		return

	else:
		print('操作失败')
		return


def tableGrant(tableName, username):
	with open('grants.txt', 'r') as f:
		for line in f.readlines():
			if line.strip().split('#')[0] == username:
				if line.strip().split('#')[1] == '*' or tableName == line.strip().split('#')[1]:
					return True
	return False


def hasGrant(username, grant):
	with open('grants.txt', 'r') as f:
		for line in f.readlines():
			if grant in line.split('#')[2]:
				return True
	return False


def isUserExist(user):
	with open('users.txt', 'r') as f:
		for line in f.readlines():
			if line.split('#')[0] == user:
				return True
	return False

def RevokeGrant(sql, username):
	matchObj = re.match(r'^revoke (.*) on (.*) from (.*);$', sql)
	if matchObj:
		grants = matchObj.group(1).split(',')
		tableNames = matchObj.group(2)
		user = matchObj.group(3)
		isUser = isUserExist(user)
		if not isUser:
			print('用户不存在')
			return
		if username == user:
			print('无法收回自己的权限')
			return
		else:
			tableName = tableNames.split(',')
			for table in tableName:
				if not tableGrant(table, username):
					print('本用户没有操作'+table+'的权限，无法收回')
					return
			grants = [grant.strip() for grant in grants]
			for grant in grants:
				if not hasGrant(user, grant):
					print('该用户没有该项权限')
					return
			try:
				with open('grants.txt', 'r') as f:
					lines = f.readlines()
				new_lines = list()
				for line in lines:
					if line.split('#')[0] == user and line.split('#')[1] in tableName:
						old_grant = line.split('#')[2].split(',')
						old_grant = [grant.replace('\n', '') for grant in old_grant]
						new_grant = [grant for grant in old_grant if grant not in grants]
						new_lines.append(user+'#'+line.split('#')[1]+'#'+','.join(new_grant)+'\n')
					else:
						new_lines.append(line)
				with open('grants.txt', 'w') as f:
					for line in new_lines:
						f.write(line)
				print('修改权限成功')
			except Exception as e:
				print(e)
			return

	else:
		print('SQL 解析失败')
		return
def GrantUser(sql, username):
	matchObj = re.match(r'^grant (.*) on (.*) to (.*);$', sql)
	if matchObj:
		grants = matchObj.group(1).split(',')
		tableName = matchObj.group(2)
		user = matchObj.group(3)
		isUser = isUserExist(user)
		if not isUser:
			print('该用户不存在')
			return 
		if user.strip() == username:
			print('无法授予本用户权限')
			return
		else:
			new_grants = list()
			tableNames = tableName.split(',')
			for table in tableNames:
				if not tableGrant(table, username):
					print('本用户没有操作'+table+'的权限')
					return
			grants = [grant.strip() for grant in grants]
			for grant in grants:
				if hasGrant(username, grant):
					new_grants.append(grant)
				else:
					print('本用户没有该项权限')
					return
			try:
				for tableName in tableNames:
					with open('grants.txt', 'a') as f:
						f.write('\n'+user+'#'+tableName+'#'+','.join(new_grants))
					print('用户权限授予成功')
			except Exception as e:
				print(e)
	else:
		print('用户授予权限失败')
		return
def HelpTable(sql):
	matchObj = re.search(r'^help table (.*);$',sql)
	if matchObj:
		tableName = matchObj.group(1)
		if os.path.exists(tableName+'.csv'):
			with open(tableName+'.csv', 'r') as f:
				file = csv.reader(f)
				rows = [row for row in file]
				flag = False
				for row in rows:
					if flag:
						data = row
						if data[2] == str(True):
							key = 'PRIMARY KEY'
						else:
							key = ''
						if data[3] == str(False):
							n_null = 'NOT NULL'
						else:
							n_null = ''
						temp = data[0]+' '+data[1]+' '+key+' '+n_null
						print(temp)
					flag = True
		else:
			print('数据表不存在')
			return
	else:
		print('解析失败')
		return 

if __name__ == '__main__':
    create_sql = 'create table '
    insert_sql = 'insert into '
    select_sql = 'select '
    update_sql = 'update '
    delete_sql = 'delete '
    create_user = 'create user '
    grant_sql = 'grant '
    revoke_sql = 'revoke '
    help_sql = 'help table '
    username = input("username:")
    password = getpass.getpass("password:")
    if login(username, password):
        while True:
            sql = input('>')
            if sql.lstrip().startswith(create_sql):
                Create.createTable(username, sql)
            elif sql.lstrip().startswith(insert_sql):
                Insert.insertData(username, sql)
            elif sql.lstrip().startswith(select_sql):
                Select.selectData(username, sql)
            elif sql.lstrip().startswith(update_sql):
                Update.updateData(username, sql)
            elif sql.lstrip().startswith(delete_sql):
                Delete.deleteData(username, sql)
            elif sql.lstrip().startswith(create_user):
                CreateUser(sql)
            elif sql.lstrip().startswith(grant_sql):
                GrantUser(sql, username)
            elif sql.lstrip().startswith(revoke_sql):
            	RevokeGrant(sql, username)
            elif sql.lstrip().startswith(help_sql):
            	HelpTable(sql)
            elif sql == 'exit()':
            	break
    else:
        print('false')
        


