def checkGrant(username, tablename, param):
	with open('grants.txt', 'r') as f:
		for line in f.readlines():
			data = line.split('#')
			if data[0] == username:
				if data[1] == '*' or data[1] == tablename:
					if param in data[2].replace('\n',''):
						return True
	return False