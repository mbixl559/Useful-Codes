#! /usr/bin/env python3
import sys
import os


def main():
	# make sure that we are given a filename on the command line
	if len(sys.argv) < 2:
		print("usage: inserttoupdate.py <sql script>")
		exit(1)
	statements = []
	file = open(sys.argv[1])
	for lineStr in file:
		line = parseInsert(lineStr)
		if len(line) > 0 and line[0] == "INSERT":
			table = line[2]
			values = line[5]
			values = values[1::][:-2].split(',')
			path = values[0]
			val = values[1]
			stmt = "UPDATE {} SET `value` = {} WHERE `path` = {};\n\n\n".format(table, val, path)
			statements.append("/* {} */\n".format(lineStr))
			statements.append(stmt)
			print(stmt)
		else:
			statements.append(lineStr)
	file.close()	
	update = open('update.sql', 'w+')
	for stmt in statements:
		update.write(stmt)
	update.close()

def parseInsert(insertStmt: str) -> list:
	lastChar = insertStmt[0]
	curPart = ''
	ret = []
	start = 0
	for i in range(len(insertStmt)):
		if insertStmt[i] == ' ':
			if lastChar == ' ': #skip over whitespace
				continue
			curPart = insertStmt[start:i]
			if curPart.upper() == 'VALUES': #once we hit the keyword 'VALUES' we can just grab the rest of the string.
				ret.append(curPart)
				ret.append(insertStmt[i+1:])
				break
			ret.append(curPart)
			start = i+1
	return ret

if __name__ == "__main__":
	main()