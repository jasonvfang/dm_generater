#coding=utf-8
import os, sys
import xml.etree.ElementTree as ET
from string import Template
from datetime import datetime

#global definition for data model object elements
PARAMETER_ATTRS = ['type', 'access', 'notification', 'needReboot', 'accessList', 'style', 'defaultValue']
XML_OBJ_TYPES = ['Object', 'MultiObject', 'Parameter', 'Instance']
VALUE_TYPES = ('Unsigned', 'dateTime', 'String', 'Int', 'Bool')

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
		
def getRootXmlObject(dmFile):
	tree = ET.parse(dmFile)
	return tree.getroot()


def getALLRootChildObject(_root_):
	for child in _root_:
		print('ChildName=%s' % child.tag, 'Type=%s' % child.get('type'), 'isObject=%s'%isObject(child))

def getChildObjects(Child):
	print('subChildName=%s' % Child.tag, 'Type=%s' % Child.get('type'))
	for subChild in Child:
		#print('objName=%s' % subChild.tag, 'Type=%s' % subChild.get('type'), 'isParameter=%s'%isParameter(subChild))
		#print('items=%s\n' % subChild.items())
		#print('keys=%s\n' % subChild.keys())
		
		if False == isParameter(subChild):
			print('Sub child parameters')
			getChildObjects(subChild)
		else:
			print('SubChildName=%s\n' % subChild.tag)
	
if __name__=='__main__':
	print("Parse xml to generate codes...\n")
	root = getRootXmlObject('data_model_tmp.xml')

	if not root:  # careful!
		print("Error: Invalid xml file, root not found!\n")
		
	getALLRootChildObject(root)	
	
	print("\nLoop all sub objects...\n")
	
	for child in root:	
		if False == isParameter(child):
			print('name=%s\n' % child.tag)
			#print('items=%s\n' % child.items())
			#print('keys=%s\n' % child.keys())
			getChildObjects(child)
		else:
			print('Sub parameters:')
			print('ChildName=%s' % child.tag, 'Type=%s' % child.get('type'))
			

