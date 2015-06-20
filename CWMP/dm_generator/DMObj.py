#coding=utf-8
	
class cDMParas:
	name           = ''
	access         = 0
	type           = ''
	notification   = 0
	
	def __init__(self, name, access, notification, type):
		self.name           = name
		self.access         = access
		self.notification   = notification
		self.type           = type
	
	
class cDMObj:
	name           = ''
	numOfChildObj  = 0
	numOfChildPara = 0
	type           = 0
	
	def __init__(self, name, numOfChildObj, numOfChildPara, type):
		self.name           = name
		self.numOfChildObj  = numOfChildObj
		self.numOfChildPara = numOfChildPara
		self.type           = type	
		
		
		