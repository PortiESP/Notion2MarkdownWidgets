from n2mw_parser import N2MW_Parser


class N2MW_CLI(N2MW_Parser):

    def __init__(self):
        super().__init__()
        self.inputmethod = "MD"
        self.inputData = ""
        
        self.outputData = []


    def convert(self):
        """
            Main method to run the app
        """ 
        self.readInput()

        if self.inputmethod == "MD":
            self.parseInputMD()


    def debug(self):
        """
            Debug method
        """

        print("=========== INPUT DATA ===========")
        print(self.inputData)
        print("=========== OUTPUT ARR ===========")
        print(self.outputData)
        

    def readInput(self):  # Read & store the data onf the input file
        """
            Read the content of the input file
        """

        if self.debuglevel: print('[*] DEBUG: readInput()')

        with open("./TestTemplates/test.md", 'r') as fd:
            self.inputData = fd.read()


    def parseInputMD(self):  # Parse the data from the input
        """
            Split the input file content in line to parse it independently and append to the `outputData` list
        """

        if self.debuglevel: print('[*] DEBUG: parseInputMD()'), 
        data = self.inputData.split('\n')

        for line in data:
            parserFunc = self.identifyTag(line)  # Indetify the tag
            if parserFunc:  # Valid tag returned 
                tag = parserFunc(line)  # Check that is a valid tag value
                if tag: self.outputData.append(tag)  # Parse and append to output tags array
                    
                
            

                

            
              

    

if __name__ == "__main__":
    converter = N2MW_CLI()

    converter.debug()
    converter.convert()
    converter.debug()