#coding=utf-8

import os, sys, string
import xml.etree.ElementTree as ET
from datetime import datetime
from string import Template
import DMObj

#global definition for data model object elements
PARAMETER_ATTRS = ['type', 'access', 'notification', 'needReboot', 'accessList', 'style', 'defaultValue']
XML_OBJ_TYPES = ['Object', 'MultiObject', 'Parameter', 'Instance']
VALUE_TYPES = ('Unsigned', 'dateTime', 'String', 'Int', 'Bool')
OBJNAME_HEAD_TAG='IGD'
DM_OBJ_HEAD_FILE = 'DMObjStructHead.c'

AUTO_GEN_PROMPT_STR = '/*\n\
** Auto generation file. \n\
** Please Do not modify this file manually. \n\
*/\n\n'

DMOBJ_TEMPLATE_STR = 'DM_OBJ_S $TagName =\n\
{\n\
\t\'$TagName\', \n\
\t$NumOfChildParameters,\n\
\t$NumOfChildObjects,\n\
\tNULL\n\
};\n'

def isObject(x):
	if x.get('type') == 'Object':
		return True
	else:
		return False

def isMultiObject(x):
	if x.get('type') == 'MultiObject':
		return True
	else:
		return False

def isInstance(x):
	if x.get('type') == 'Instance':
		return True
	else:
		return False

def isParameter(x):
	type_str = x.get('type')
	return type_str in VALUE_TYPES

def writeFileLinesContent(FileObj, Content):
	if FileObj:
		FileObj.writelines(Content)
	else:
		print("File Obj invalid!!!")
	

def genTempDMObj(pDmObj):
	if pDmObj:
		bufStr = Template(DMOBJ_TEMPLATE_STR)
		
		restr = bufStr.substitute(TagName = pDmObj.name, NumOfChildParameters = pDmObj.numOfChildObj, NumOfChildObjects = pDmObj.numOfChildPara)
		return restr
	else:
		return None
	
def getRootXmlObject(dmFile):
	tree = ET.parse(dmFile)
	return tree.getroot()


def getDMObject(_Obj_):
	#print("RootNumOfChild:%d" % len(_Obj_))
	NumOfChild = len(_Obj_)
	NumOfParas = 0
	name = _Obj_.tag
	ChildParamList = []
	
	for child in _Obj_:
		if True == isParameter(child):
			NumOfParas += 1
			tmpParamObj = DMObj.cDMParas(child.tag, child.get('access'), child.get('notification'), child.get('type'))
			ChildParamList.append(tmpParamObj)
			print('ChildParamListName=%s' % ChildParamList[NumOfParas - 1].name, 'Type=%s' % child.get('type'), 'isObject=%s'%isObject(child))		
	
	if len(ChildParamList) == 0:
		ChildParamList = None
	
	rootObj = DMObj.cDMObj(name, NumOfChild, NumOfParas, 0, ChildParamList)
	
	return rootObj
	
def getChildObjects(Child):
	#print('subChildName=%s' % Child.tag, 'Type=%s' % Child.get('type'))
	
	for subChild in Child:
		#print('objName=%s' % subChild.tag, 'Type=%s' % subChild.get('type'), 'isParameter=%s'%isParameter(subChild))
		#print('items=%s\n' % subChild.items())
		#print('keys=%s\n' % subChild.keys())
		
		if False == isParameter(subChild):	
			print('\nChildObjname=%s,numOfChild:%d' % (subChild.tag,len(subChild)))
			getChildObjects(subChild)
		else:
			print('SubParaName=%s' % subChild.tag)
	

def writeDMObjects(file_object, tmpRootObj):
	if tmpRootObj and file_object:
		strbuf = genTempDMObj(tmpRootObj)

		if strbuf:
			print("strbuf:%s" % strbuf)
			writeFileLinesContent(file_object, strbuf)
		else:
			print('Root Gen failed, exit...')
			file_object.close()	
			sys.exit(1)
	
	
if __name__=='__main__':
	print("Parse xml to generate codes...\n")
	
	root = getRootXmlObject('data_model_tmp_Single.xml')
	
	file_object = open(DM_OBJ_HEAD_FILE, 'w+')
	writeFileLinesContent(file_object, AUTO_GEN_PROMPT_STR)
	
	if not root:  # careful!
		print("Error: Invalid xml file, root not found!\n")
	
	tmpRootObj = getDMObject(root)
	writeDMObjects(file_object, tmpRootObj)
	
	print("\nLoop all sub objects...\n")

	for child in root:	
		if False == isParameter(child):
			print('\nChildObjname=%s,numOfChild:%d' % (child.tag,len(child)))
			#print('items=%s\n' % child.items())
			#print('keys=%s\n' % child.keys())
			getChildObjects(child)
		else:
			#print('Sub parameters:')
			print('RootChildParaName=%s' % child.tag)

	file_object.close()		
			

