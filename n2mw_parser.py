"""

    This modules defines the class `N2MW_Parser` 

    > The class can be inherited on instanced to use its metods

    > I has a main method: `identifyTag(input)` this one will match the input with one tag and return the function 
    > that will be able to parse that input, so the return function must be called passing the same argument as the identify function

    > The rest of the functions are the parser functions

"""


import re


class N2MW_Parser():


    def __init__(self):
        self.debuglevel = True
        self.forceWrapping = ''
        self.wrappingStack = []

    
    def identifyTag(self, input):
        """
            Matches the input data with the corresponding function that parses it as a tag

            `input`:(String) --> Data that will be matched as a MD object
            RETURN:(function) --> Function that will parse the input MD object

        """
        tags = {  # All managed tags that can be parsed
            "####": self.parseTitle4,
            "###": self.parseTitle3,
            "##": self.parseTitle2,
            "#": self.parseTitle,
            '---': self.parseHr,
            '===': self.parseHr,
            '>': self.parseQuote,
            '```': self.parseCode,
            '!\[': self.parseImg,
            '\[': self.parseUrl,
        }
        if self.debuglevel: print('[*] DEBUG: identifyTag("', input,'")')
        
        if len(input.strip()) == 0: return None

        if not re.match('^' + self.forceWrapping, input):  # Run this code while force wrapping pattern doesnt get matched
            self.concatTagChildren(input)
            return None


        input = input.strip()
        for key,val in tags.items(): 
            if self.debuglevel: print('  [i] DEBUG: identifyTag("', input,'") -->', re.search(key, input))
            if (re.search('^' + key, input) != None): return val

        return self.parseParagraph
    

    def openTag(self, tag, params=''):
        """
            Add the tag and the children to the stack
        """

        self.wrappingStack.append([tag, [f"<Tags.{tag} {params}>", ""]])

    
    def concatTagChildren(self, children):
        """
            Add the children data to the top of the stack
        """

        if self.wrappingStack:
            self.wrappingStack[-1][1][1] += children
    

    def closeTag(self):
        """
            Pops the top of the wrapping stack and return the full tag
        """

        tag, childrenObject = self.wrappingStack.pop()    

        return [*childrenObject, f"</Tags.{tag}>"]


    """

        Mardown object parsing functions bellow...
        ---------------------------------------------------------------------------------------------------

    """

    def parseTitle4(self, data):
        if self.debuglevel: print('[*] DEBUG: parseTitle3("', data,'")')

        return ["<Tags.Title3>", data.strip(' #'), "</Tags.Title3>"]
    

    def parseTitle3(self, data):
        if self.debuglevel: print('[*] DEBUG: parseTitle3("', data,'")')

        return ["<Tags.Title3>", data.strip(' #'), "</Tags.Title3>"]
    

    def parseTitle2(self, data):
        if self.debuglevel: print('[*] DEBUG: parseTitle2("', data,'")')

        return ["<Tags.Title2>", data.strip(' #'), "</Tags.Title2>"]
    

    def parseTitle(self, data):
        if self.debuglevel: print('[*] DEBUG: parseTitle("', data,'")')

        return ["<Tags.Title>", data.strip(' #'), "</Tags.Title>"]
    

    def parseHr(self, _):
        if self.debuglevel: print('[*] DEBUG: parseHr()')

        return ["<Tags.Hr />",]
    

    def parseParagraph(self, data):
        if self.debuglevel: print('[*] DEBUG: parseParagraph()')

        return ["<Tags.Paragraph>", data, "</Tags.Paragraph>"]
    

    def parseQuote(self, data):
        if self.debuglevel: print('[*] DEBUG: parseQuote()')

        return ["<Tags.Quote>", data.strip(' >'), "</Tags.Quote>"]
    

    def parseCode(self, data):
        if self.debuglevel: print('[*] DEBUG: parseCode()')

        if self.forceWrapping:
            if self.debuglevel: print('  [i] DEBUG: Stop wrap')
            self.forceWrapping = ''
            return self.closeTag()
        else: 
            if self.debuglevel: print('  [i] DEBUG: Start wrap')
            self.forceWrapping = "```" 
            self.openTag("Code")
            return None


    def parseImg(self, data):
        if self.debuglevel: print('[*] DEBUG: parseImg()')

        charsetSymbols = "!\.\-\_@#%\?=\/:"
        charsetAlt = f"\w\s{charsetSymbols}"
        charsetUrl = f"\w\s{charsetSymbols}"
        alt, src = re.search(f'!\[([{charsetAlt}]+)\]\(([{charsetUrl}]+)\)', data).groups()

        return ['<Tags.Image alt={"' + alt + '"} img={"' + src + '"} />',]
    

    def parseUrl(self, data):
        if self.debuglevel: print('[*] DEBUG: parseUrl()')

        charsetSymbols = "!\.\-\_@#%\?=\/:"
        charsetAlt = f"\w\s{charsetSymbols}"
        charsetUrl = f"\w\s{charsetSymbols}"
        title, src = re.search(f'\[([{charsetAlt}]+)\]\(([{charsetUrl}]+)\)', data).groups()

        return ['<Tags.Url title={"' + title + '"} src={"' + src + '"} />',]
