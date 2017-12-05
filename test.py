import re

# sql = 'id>=1'
# matchObj = re.search(r'(.*)([><=]{1}|[><!]{1}=)(.*)', sql)
# if matchObj:
# 	print(matchObj.group(1))
# 	print(matchObj.group(2))
datas = ['a', 'a']
datas.insert(0, 'b')
for data in datas:
	print(data)