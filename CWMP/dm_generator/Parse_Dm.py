#coding=utf-8

import os, sys, string
import xml.etree.ElementTree as ET
from datetime import datetime
from string import Template
import DMObj

DATA_MODEL_XML_FILE = 'data_model_tmp_Single.xml'

#global definition for data model object elements
PARAMETER_ATTRS = ['type', 'access', 'notification', 'needReboot', 'accessList', 'style', 'defaultValue']
XML_OBJ_TYPES = ['Object', 'MultiObject', 'Parameter', 'Instance']
VALUE_TYPES = ('Unsigned', 'dateTime', 'String', 'Int', 'Bool')
OBJNAME_HEAD_TAG='IGD'
DM_OBJ_HEAD_FILE = 'dm_objects_tb.c'

AUTO_GEN_PROMPT_STR = '/*\n\
** Auto generation file. \n\
** Please Do not modify this file manually. \n\
*/\n'

DMOBJ_CHILD_OBJS_TEMPLATE_STR_HEAD = '\n\nDM_OBJ_S $TagName =\n\
{\n'

DMOBJ_CHILD_OBJS_TEMPLATE_STR_BODY = '\
\t$TagName,\n'


DMOBJ_PARAMETER_TEMPLATE_STR_HEAD = '\n\nDM_PARAMETER_S $TagName =\n\
{\n\
'

DMOBJ_PARAMETER_TEMPLATE_STR_BODY = '\
\t{\n\
\t\t\"$TagName\", \n\
\t\t\"$access\",\n\
\t\t\"$value_type\",\n\
\t\t\"$notification\",\n\
\t},\n'

DMOBJ_TEMPLATE_STR = '\n\nDM_OBJ_S $ObjTagName =\n\
{\n\
\t\"$TagName\", \n\
\t$NumOfChildParameters,\n\
\t$NumOfChildObjects,\n\
\t$ChildObjects,\n\
\t$ChildParas\n\
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
	
def genTempDMChildObjs(pDmObj):
	if pDmObj and pDmObj.childObjs:
		numOfChildObjs = len(pDmObj.childObjs)		
		ObjBufStr = Template(DMOBJ_CHILD_OBJS_TEMPLATE_STR_HEAD)
		restr = ObjBufStr.substitute(TagName = pDmObj.name.replace('.', '_')+'ChildObjs[]')
		
		print('restr=%s' % restr)
		for id in range(numOfChildObjs):
			ObjBufStr = Template(DMOBJ_CHILD_OBJS_TEMPLATE_STR_BODY)
			rs = ObjBufStr.substitute(TagName = pDmObj.childObjs[id].tag.replace('.', '_'))
			print('restr=%s' % rs)
			restr += rs
			
		restr += '};\n'
		
		return restr
	else:
		return None

def genTempDMParams(pDmObj):
	if pDmObj and pDmObj.childParams:
		numOfChildPara = len(pDmObj.childParams)		
		ParaBufStr = Template(DMOBJ_PARAMETER_TEMPLATE_STR_HEAD)
		restr = ParaBufStr.substitute(TagName = pDmObj.name.replace('.', '_')+'ChidParams[]')
		
		#print('restr=%s' % restr)
		for id in range(numOfChildPara):
			ParaBufStr = Template(DMOBJ_PARAMETER_TEMPLATE_STR_BODY)
			rs = ParaBufStr.substitute(TagName = pDmObj.childParams[id].name, access = pDmObj.childParams[id].access, value_type = pDmObj.childParams[id].type, notification = pDmObj.childParams[id].notification)
			#print('restr=%s' % rs)
			restr += rs
			
		restr += '};\n'
		
		return restr
	else:
		return None
		
def genTempDMObj(pDmObj):
	if pDmObj:		
		ObjBufStr = Template(DMOBJ_TEMPLATE_STR)
		ChildObjsRefTag = 'NULL'
		ChildParamRefTag = 'NULL'
		
		if len(pDmObj.childParams) > 0:
			ChildParamRefTag = '&' + pDmObj.name.replace('.', '_') + 'ChildParams'
		
		if pDmObj.numOfChildObj > 0:
			ChildObjsRefTag = '&' + pDmObj.name.replace('.', '_') + 'ChildObjs'
			
		restr = ObjBufStr.substitute(ObjTagName = pDmObj.name.replace('.', '_'), TagName = pDmObj.name, NumOfChildParameters = pDmObj.numOfChildObj, NumOfChildObjects = pDmObj.numOfChildPara, ChildObjects = ChildObjsRefTag, ChildParas = ChildParamRefTag)
		return restr
	else:
		return None
	
def getRootXmlObject(dmFile):
	tree = ET.parse(dmFile)
	return tree.getroot()


def getDMObject(_Obj_):
	#print("ObjNumOfChild:%d" % len(_Obj_))
	NumOfChild = len(_Obj_)
	NumOfParas = 0
	name = _Obj_.tag
	ChildParamList = []
	ChildObjList   = []
	
	for child in _Obj_:
		if True == isParameter(child):
			NumOfParas += 1
			tmpParamObj = DMObj.cDMParas(child.tag, child.get('access'), child.get('notification'), child.get('type'))
			ChildParamList.append(tmpParamObj)
			#print('ChildParamListName=%s' % ChildParamList[NumOfParas - 1].name, 'Type=%s' % child.get('type'), 'isObject=%s'%isObject(child))		
		else:			
			ChildObjList.append(child)
			print("=====ChildObjName:%s=====" % child.tag)
			
	#print('\n####%s,len(ChildParamList)=%d'%(_Obj_.tag, len(ChildParamList)))

	tmpDMObj = DMObj.cDMObj(name, NumOfChild, NumOfParas, 0, ChildParamList, ChildObjList)
	return tmpDMObj
	
	
def writeDMObjects(file_object, tmpRootObj):
	if tmpRootObj and file_object:		
		#Write Obj parameters firstly 
		if len(tmpRootObj.childParams) > 0:
			strParas = genTempDMParams(tmpRootObj)
			#print('%s'%strParas)
			writeFileLinesContent(file_object, strParas)
		
		if len(tmpRootObj.childObjs) > 0:
			strChilds = genTempDMChildObjs(tmpRootObj)
			writeFileLinesContent(file_object, strChilds)
		
		strbuf = genTempDMObj(tmpRootObj)

		if strbuf:
			#print("strbuf:%s" % strbuf)
			writeFileLinesContent(file_object, strbuf)
		else:
			print('Obj Gen failed, exit...')
			file_object.close()	
			sys.exit(1)	
			
			
def fetchWriteChildObjects(Child, file_object):
	for subChild in Child:
		if False == isParameter(subChild):	
			print('\nChildObjname=%s,numOfChild:%d' % (subChild.tag,len(subChild)))
			#tmpSubDMObj = getDMObject(subChild)
			#writeDMObjects(file_object, tmpSubDMObj)
			fetchWriteChildObjects(subChild, file_object)
		else:
			print('SubParaName=%s' % subChild.tag)
			
	if False == isParameter(Child) and len(Child):
		tmpChildDMObj = getDMObject(Child)		
		writeDMObjects(file_object, tmpChildDMObj)	

if __name__=='__main__':
	print("Parse xml to generate codes...\n")
	
	root = getRootXmlObject(DATA_MODEL_XML_FILE)
	
	file_object = open(DM_OBJ_HEAD_FILE, 'w+')
	writeFileLinesContent(file_object, AUTO_GEN_PROMPT_STR)
	
	if not root:  # careful!
		print("Error: Invalid xml file, root not found!\n")
	
	
	
	print("\nLoop all sub objects...\n")
	
	for child in root:	
		if False == isParameter(child):
			print('\nChildObjname=%s,numOfChild:%d' % (child.tag,len(child)))
			fetchWriteChildObjects(child, file_object)
		#else:
		#	print('RootChildParaName=%s' % child.tag)

	tmpRootObj = getDMObject(root)
	writeDMObjects(file_object, tmpRootObj)
	
	writeFileLinesContent(file_object, '\n/* +++++ Auto Gen codes end +++++ */\n\n')
	file_object.close()		
			

