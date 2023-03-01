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

        self.CHARSET_SYMBOLS = "!\.\-\_@#%\?=\/:<>,"

    
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
            '`\w+': self.parseItalic,
            '\-\s': self.parseUList,
            '-->': self.parseTest,
        }

        if self.debuglevel: print('[*] DEBUG: identifyTag("', input,'") @ Buffer: ', self.buffer)
        
        if len(input.strip()) and (self.buffer[0] == 0): 
            return None

        if self.buffer[0] == "":  # If there is no active buffer
            for key,val in tags.items(): 
                if self.debuglevel: print('  [i] DEBUG: identifyTag("', input,'") -->', re.match("\s*" + key, input))
                if (re.match("\s*" + key, input) != None): 
                    ret = val
                    break
            else:
                ret = self.parseParagraph
        else:
            if re.search(self.buffer[0] + "$", input):  # Closing pattern matched
                ret = self.buffer[1]
            else:  # Keep writting to the buffer
                self.buffer[2] += '\n\n' + input
                ret = None

        return ret
                
    

    def toggleBuffer(self, pattern, data, callback):
        """
            Return the buffer if the closing pattern is matched
        """

        if self.buffer[0] == '':  # Buffer empty, start new one
            self.buffer[0] = pattern
            self.buffer[1] = callback
            self.buffer[2] = data
            if self.debuglevel: print('  [i] DEBUG: Start wrap', self.buffer)
            return None
        else:
            self.buffer[0] = ""
            self.buffer[1] = None
            if self.debuglevel: print('  [i] DEBUG: Stop wrap', self.buffer)
            return self.buffer[2] + '\n\n'
        

    def wrapTag(self, tag, child, params=None):
        """
            Takes a tag and its child and create as list of the open tag (<Tags.tag>) and the close tag (</Tags.tag>)
        """

        params = params if params else ""

        return [f"<Tags.{tag} {params}>", child.strip(), f"</Tags.{tag}>"]
    

    def extractTitle(self, data):
        """
            Takes a string, and if it is longer than a single line, extrac the first line as a title parameter and returns a tuple

            RETURN ('title="My first line"', 'The rest of my lines\nThis is a second line')

        """

        data = data.strip().split('\n')
        params = None

        if len(data) > 1:
            params = 'title="' + data[0] + '"'
            data = "\n".join(data[1:])

        return (params, data)
    

    def parseFontStyle(self, string):
        """
            Parse the inline font styles for Bold, Italic & Code
        """

        if self.debuglevel: print('[*] DEBUG: parseFontStyle("', string,'")')

        if string == None: return None

        # Parse bold
        matches = re.findall("\*\*([\w\s`]+)\*\*", string)
        for entry in matches:
            string = re.sub("\*\*"+entry+"\*\*", "<b>" + entry + "</b>", string)
        string = re.sub("(\*\*)", "", string)


        # Parse italic
        matches = re.findall("\*([\w\s<>/`]+)\*", string)
        for entry in matches:
            string = re.sub("\*"+entry+"\*", "<i>" + entry + "</i>", string)
        string = re.sub("(\*)", "", string)


        # Parse inline code
        matches = re.findall("`([\w\s<>/\*]+)`", string)
        for entry in matches:
            string = re.sub("`"+entry+"`", "<Tags.Code inline>" + entry + "</Tags.Code>", string)
        string = re.sub("(`)", "", string)


        return string
        

    """

        Mardown object parsing functions bellow...
        ---------------------------------------------------------------------------------------------------

    """

    def parseTitle4(self, data):
        if self.debuglevel: print('[*] DEBUG: parseTitle3("', data,'")')

        return self.wrapTag("Title3", data.strip(' #'))
    

    def parseTitle3(self, data):
        if self.debuglevel: print('[*] DEBUG: parseTitle3("', data,'")')

        return self.wrapTag("Title3", data.strip(' #'))
    

    def parseTitle2(self, data):
        if self.debuglevel: print('[*] DEBUG: parseTitle2("', data,'")')

        return self.wrapTag("Title2", data.strip(' #'))
    

    def parseTitle(self, data):
        if self.debuglevel: print('[*] DEBUG: parseTitle("', data,'")')

        return self.wrapTag("Title", data.strip(' #'))
    

    def parseHr(self, _):
        if self.debuglevel: print('[*] DEBUG: parseHr()')

        return "<Hr />"

    def parseParagraph(self, data):
        if self.debuglevel: print('[*] DEBUG: parseParagraph()')

        return self.wrapTag("Paragraph", data)
    

    def parseQuote(self, data):
        if self.debuglevel: print('[*] DEBUG: parseQuote()')

        data = "".join(re.findall("> ?([\w\s]+)\s?", data))
        (params, data) = self.extractTitle(data)

        return self.wrapTag("Quote", data, params)
    

    def parseCode(self, data):
        if self.debuglevel: print('[*] DEBUG: parseCode("', data, '")')

        buffState = self.toggleBuffer("```", data.strip(" `"), self.parseCode)

        if buffState:
            return self.wrapTag("Code", buffState + data.strip(" `"))
        else:    
            return None


    def parseImg(self, data):
        if self.debuglevel: print('[*] DEBUG: parseImg()')

        charsetAlt = f"\w\s{self.CHARSET_SYMBOLS}"
        charsetUrl = f"\w\s{self.CHARSET_SYMBOLS}"
        alt, src = re.search(f'!\[([{charsetAlt}]+)\]\(([{charsetUrl}]+)\)', data).groups()

        return ['<Tags.Image alt={"' + alt + '"} img={"' + src + '"} />',]
    

    def parseUrl(self, data):
        if self.debuglevel: print('[*] DEBUG: parseUrl()')

        
        charsetAlt = f"\w\s{self.CHARSET_SYMBOLS}"
        charsetUrl = f"\w\s{self.CHARSET_SYMBOLS}"
        title, src = re.search(f'\[([{charsetAlt}]+)\]\(([{charsetUrl}]+)\)', data).groups()

        return ['<Tags.Url title={"' + title + '"} src={"' + src + '"} />',]


    def parseCallout(self, data):
        if self.debuglevel: print('[*] DEBUG: parseCallout()', data)

        data = re.sub("</?aside>", "", data)
        buffState = self.toggleBuffer("</aside>", data, self.parseCallout)

        if buffState:  # If buffer is closed
            (params, data) = self.extractTitle(buffState+data)
            return self.wrapTag("Callout", data, params)
        else:   # If buffer is still opened
            return None
    

    def parseBold(self, data):
        if self.debuglevel: print('[*] DEBUG: parseBold()')

        return ["<b>", re.search("\*\*([\w\s\(\)]+)\*\*", data).groups()[0], "</b>"]
    

    def parseItalic(self, data):
        if self.debuglevel: print('[*] DEBUG: parseItalic()')

        return ["<i>", re.search("\*([\w\s\(\)]+)\*", data).groups()[0], "</i>"]
    

    def parseInlineCode(self, data):
        if self.debuglevel: print('[*] DEBUG: parseInlineCode()')

        data = re.search(f"`([\w\s{self.CHARSET_SYMBOLS}]+)`", data).groups()[0]

        return self.wrapTag("Code", data, "inline")


    def parseUList(self, data):
        if self.debuglevel: print('[*] DEBUG: parseUList()')

        itemList = data.strip().split("\n")
        stripFunc = lambda s: '"' + s.strip(' -') + '"'

        parsedList = map(stripFunc, itemList)

        itemsStr = ", ".join(parsedList)
        
        itemsListStr = "{" + f"[{itemsStr}]" + "}"
        
        return [f"<Tags.UList items={itemsListStr} />"]
    
    def parseTest(self, data):
        if self.debuglevel: print('[*] DEBUG: parseTest()')
        
        self.identifyTag(data.replace("-->", ""))
