# tinydict = {'Name': 'Zara', 'Age': 7}
#
# keys = tinydict.keys()
#
# tinydict['a'] = 'b'
#
# print(keys)
# print(tinydict)

# import time
#
# localtime = str(time.asctime(time.localtime(time.time())))
# print (str(localtime))

file = open("test.txt", 'w')
file.write(str(type("abc")))
file.close()