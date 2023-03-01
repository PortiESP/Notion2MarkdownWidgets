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
        self.debuglevel = True   # Print debug messages
        self.buffer = ["", None, ""]  # This attr will be filled when we need some elements to support multiline children --> ["<closingPattern>", <callback>, "<buffer>"]

    
    def identifyTag(self, input):
        """
            Matches the input data with the corresponding function that parses it as a tag

            `input`:(String) --> Data that will be matched as a MD object
            RETURN:(function) --> Function that will parse the input MD object

        """
        tags = {  # All managed tags that can be parsed
            "####\s": self.parseTitle4,
            "###\s": self.parseTitle3,
            "##\s": self.parseTitle2,
            "#\s": self.parseTitle,
            '(---|===)+': self.parseHr,
            '>\s': self.parseQuote,
            '```': self.parseCode,
            '!\[': self.parseImg,
            '\[': self.parseUrl,
            '</?aside>': self.parseCallout,
            '\*\*\w+': self.parseBold,
            '\*\w+': self.parseItalic,
            '\-\s': self.parseUList,
        }

        if self.debuglevel: print('[*] DEBUG: identifyTag("', input,'") @ Buffer: ', self.buffer)
        
        if len(input.strip()) and (self.buffer[0] == 0): 
            return None


        if self.buffer[0] == "":  # If there is no active buffer
            for key,val in tags.items(): 
                if self.debuglevel: print('  [i] DEBUG: identifyTag("', input,'") -->', re.match("\s*" + key, input))
                if (re.match("\s*" + key, input) != None): return val
            else:
                return self.parseParagraph
        else:
            if re.search(self.buffer[0] + "$", input):  # Closing pattern matched
                return self.buffer[1]
            else:  # Keep writting to the buffer
                self.buffer[2] += '\n\n' + input
                return None
                
    

    def toggleBuffer(self, pattern, data, callback):
        """
            Return the buffer if the closing pattern is matched
        """

        if self.buffer[0] == '':  # Buffer empty, start new one
            self.buffer[0] = pattern
            self.buffer[1] = callback
            self.buffer[2] = data.strip(" " + pattern)
            if self.debuglevel: print('  [i] DEBUG: Start wrap', self.buffer)
            return None
        else:
            self.buffer[0] = ""
            self.buffer[1] = None
            if self.debuglevel: print('  [i] DEBUG: Stop wrap', self.buffer)
            return self.buffer[2] + '\n\n'
        

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
        if self.debuglevel: print('[*] DEBUG: parseCode("', data, '")')

        buffState = self.toggleBuffer("```", data, self.parseCode)

        if buffState:
            return ["<Tags.Code>", buffState + data, "</Tags.Code>"]
        else:    
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


    def parseCallout(self, data):
        if self.debuglevel: print('[*] DEBUG: parseCallout()')

        return ["<Tags.Callout>", re.search("<aside>([\w\s\(\)]+)</aside>", data).groups()[0], "</Tags.Callout>"]
    

    def parseBold(self, data):
        if self.debuglevel: print('[*] DEBUG: parseBold()')

        return ["<b>", re.search("\*\*([\w\s\(\)]+)\*\*", data).groups()[0], "</b>"]
    

    def parseItalic(self, data):
        if self.debuglevel: print('[*] DEBUG: parseItalic()')

        return ["<i>", re.search("\*([\w\s\(\)]+)\*", data).groups()[0], "</i>"]


    def parseUList(self, data):
        if self.debuglevel: print('[*] DEBUG: parseUList()')

        print(data)
