#coding=utf-8
	
class cDMParas:
	name           = ''
	access         = ''
	type           = ''
	notification   = ''
	
	def __init__(self, name, access, notification, type):
		self.name           = name
		self.access         = access
		self.notification   = notification
		self.type           = type
	
	
class cDMObj:
	name           = ''
	numOfChildObj  = 0
	numOfChildPara = 0
	type           = ''
	childParams    = []
	
	def __init__(self, name, numOfChildObj, numOfChildPara, type, childParams):
		self.name           = name
		self.numOfChildObj  = numOfChildObj
		self.numOfChildPara = numOfChildPara
		self.type           = type	
		self.childParams	= childParams
		
		
		