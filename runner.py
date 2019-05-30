import plex

class ParseError(Exception):
	pass

class ParseRun(Exception):
	pass

class MyParser:
	def __init__(self):
		space = plex.Any(" \n\t")
		parenthesi = plex.Str('(',')')
		letter = plex.Range('azAZ')
		digit = plex.Range('09')
		inp = plex.Range('01')
		bits = plex.Rep1(inp)
		name = letter+plex.Rep(letter|digit)
		keyword = plex.Str('print','PRINT')
		operator=plex.Str('AND','OR','XOR','=')
		self.st = {}
		self.lexicon = plex.Lexicon([
			(operator,plex.TEXT),
			(keyword,'PRINT'),
			(parenthesi,plex.TEXT),
			(name,'IDENTIFIER'),
			(bits, 'BITSTOKEN'),
			(space,plex.IGNORE)
			])

	def create_scanner(self,fp):
		self.scanner = plex.Scanner(self.lexicon,fp)
		self.la,self.text=self.next_token()

	def next_token(self):
		return self.scanner.read()

	def match(self,token):
		if self.la==token:
			self.la,self.text=self.next_token()
		else:
			raise ParseError("perimenw (")

	def parse(self,fp):
		self.create_scanner(fp)
		self.stmt_list()
		
	def stmt_list(self):
		if self.la=='IDENTIFIER' or self.la=='PRINT':
			self.stmt()
			self.stmt_list()
		elif self.la==None:
			return
		else:
			raise ParseError("perimenw IDENTIFIER or Print")
	def stmt(self):
		if self.la=='IDENTIFIER':
			varname= self.text
			self.match('IDENTIFIER')
			self.match('=')
			e=self.expr()
			self.st[varname]= e
		elif self.la=='PRINT':
			self.match('PRINT')
			e=self.expr()
			print('{:b}'.format(e))
		else:
			raise ParseError("perimenw IDENTIFIER or PRINT")
	def expr(self):
		if self.la=='(' or self.la=='IDENTIFIER' or self.la=='BITSTOKEN':	
			func=self.term()
			while self.la == 'XOR':
				self.match ('XOR')
				func2 = self.term()
				func ^= func2
			if self.la == 'IDENTIFIER' or self.la == 'PRINT' or self.la == None or self.la == ')':
				return func 
			else:
				raise ParseError ('perimenw XOR')
			
		else:
			raise ParseError("perimenw ( or IDENTIFIER or BITSTOKEN or )")
	
	def term(self):
		if self.la=='(' or self.la=='IDENTIFIER' or self.la=='BITSTOKEN':	
			func=self.factor()
			while self.la == 'OR':
				self.match ('OR')
				func2 = self.factor()
				func |= func2
			if self.la == 'XOR' or self.la == 'IDENTIFIER' or self.la == 'PRINT' or self.la == None or self.la == ')':
				return func 
			else:
				raise ParseError ('perimenw OR')
			
		else:
			raise ParseError("perimenw ( or IDENTIFIER or BITSTOKEN or )")
	def factor(self):
		if self.la=='(' or self.la=='IDENTIFIER' or self.la=='BITSTOKEN':	
			func=self.atom()
			while self.la == 'AND':
				self.match ('AND')
				func2 = self.atom()
				func &= func2
			if self.la == 'XOR' or self.la == 'OR' or self.la == 'IDENTIFIER' or self.la == 'PRINT' or self.la == None or self.la == ')':
				return func 
			else:
				raise ParseError ('perimenw AND')
			
		else:
			raise ParseError("perimenw ( or IDENTIFIER or BITSTOKEN or )")
	
	def atom(self):
		if self.la=='(':
			self.match('(')
			e=self.expr()
			self.match(')')
			return e
		elif self.la=='IDENTIFIER':
			varname = self.text
			self.match('IDENTIFIER')
			if varname in self.st:
				return self.st[varname]
			raise ParseRun("perimenw id arxikopoiimeno")
		elif self.la=='BITSTOKEN':
			value=int(self.text,2)
			self.match('BITSTOKEN')
			return value
		else:
			raise ParseError("perimenw id BITSTOKEN or (")
	
parser = MyParser()
with open('test1.txt','r') as fp:
	parser.parse(fp)
