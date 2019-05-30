import plex

class ParseError(Exception):
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
			self.match('IDENTIFIER')
			self.match('=')
			self.expr()
		elif self.la=='PRINT':
			self.match('PRINT')
			self.expr()
		else:
			raise ParseError("perimenw IDENTIFIER or PRINT")
	def expr(self):
		if self.la=='(' or self.la=='IDENTIFIER' or self.la=='BITSTOKEN':	
			self.term()
			self.term_tail()
		else:
			raise ParseError("perimenw ( or IDENTIFIER or BITSTOKEN or )")
	def term_tail(self):
		if self.la== 'XOR':
			self.match('XOR')
			self.term()
			self.term_tail()
		elif self.la=='IDENTIFIER' or self.la=='PRINT' or self.la== None or self.la==')':
			return
		else:
			raise ParseError("perimenw XOR")
	def term(self):
		if self.la=='(' or self.la=='IDENTIFIER' or self.la=='BITSTOKEN' or self.la==')':	
			self.factor()
			self.factor_tail()
		else:
			raise ParseError("perimenw ( or IDENTIFIER or BITSTOKEN or )")
	def factor_tail(self):
		if self.la=='OR':
			self.match('OR')
			self.factor()
			self.factor_tail()
		elif self.la=='XOR' or self.la=='IDENTIFIER' or self.la=='PRINT' or self.la== None or self.la==')':
			return
		else:
			raise ParseError("perimenw OR")
	def factor(self):
		if self.la=='(' or self.la=='IDENTIFIER' or self.la=='BITSTOKEN' or self.la==')':	
			self.atom()
			self.atom_tail()
		else:
			raise ParseError("perimenw ( or IDENTIFIER or BITSTOKEN or )")
		
	
	def atom_tail(self):
		if self.la =='AND' :
			self.match('AND')
			self.atom()
			self.atom_tail()
		elif self.la=='OR' or self.la=='XOR' or self.la=='IDENTIFIER' or self.la=='PRINT' or self.la== None or self.la==')':
			return
		else:
			raise ParseError("perimenw AND")

	def atom(self):
		if self.la=='(':
			self.match('(')
			self.expr()
			self.match(')')
		elif self.la=='IDENTIFIER':
			self.match('IDENTIFIER')
		elif self.la=='BITSTOKEN':
			self.match('BITSTOKEN')
		else:
			raise ParseError("perimenw id BITS or (")


parser = MyParser()
with open('test1.txt','r') as fp:
	parser.parse(fp)
