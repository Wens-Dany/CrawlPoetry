#! /usr/bin/python
#coding: utf-8
#Author:SW
#Date:17-02-2014 12:23
import json
import jieba
import jieba.analyse

def jiebaParse(array):
	for index in range(len(array)):	
		comments = array[index]["comment"]
		content = array[index]["content"]
		sentence = comments + content
		keys = jieba.analyse.extract_tags(sentence, topK = 30)
		array[index]["keys"] = keys
def Load(filename):
	if filename == '' or filename == None:
		print "Filename is empty"
		return
	f = open(filename, 'r')
	if f == None:
		print "Open file(%s) Failed!"%filename
		return
	jsonstr = f.read()
	array = json.loads(jsonstr)
	f.flush()
	f.close()
	return array

def DumpAsJson(array, filename):
	if array == None:
		print "Array to dump is none!"
		return
	if filename == None or filename == '':
		print "Filename to dump is empty!"
		return
	f = open(filename, 'w')
	if f == None:
		print "Open file(%s) Failed!"%filename
		return
	jsonstr = json.dumps(array)
	f.write(jsonstr)
	f.flush()
	f.close()

def DumpAsTxt(array, filename):
	if array == None:
		print "Array to dump is none!"
		return
	if filename == None or filename == '':
		print "Filename to dump is empty!"
		return
	f = open(filename, 'w')
	if f == None:
		print "Open file(%s) Failed!"%filename
		return
	string = ''
	for element in array:
		string += '{'
		no = str(element["id"])
		string += "id:" + no + "\n"
		title = element["title"]
		string += "title:\n" + title + "\n"
		content = element["content"]
		string += "content:\n" + content + "\n"
		tags = [key + ',' for key in element["keys"]]
		string += "tags:\n" + ''.join(tags) + "\n"
		string += "}\n\n"
	f.write(string)
	f.flush()
	f.close()

def main():
	array = Load("savepoetry1to10000.json")
	jiebaParse(array)
	DumpAsTxt(array, "save1to10000.txt")
	return
if __name__ == "__main__":
	main()
