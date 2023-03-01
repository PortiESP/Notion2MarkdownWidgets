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
            self.inputData = fd.read().strip()


    def parseInputMD(self):  # Parse the data from the input
        """
            Split the input file content in line to parse it independently and append to the `outputData` list
        """

        if self.debuglevel: print('[*] DEBUG: parseInputMD()'), 
        filedata = self.inputData.split('\n\n')

        for block in filedata:
            parserFunc = self.identifyTag(block)  # Indetify the tag
            if parserFunc:  # Valid tag parser function returned 
                tag = parserFunc(block)  # Check that is a valid tag value
                if tag: 
                    tag[1] = self.parseFontStyle(tag[1])
                    self.outputData.append(tag)  # Parse and append to output tags array
                    
    def exportAsPost(self, path):
        """
            Export the data as a component for the blog to a file
        """

        buffer = ""

        # Imports
        buffer += 'import Tags from "@/components/MarkupWidgets/Tags.js"\n'
        buffer += "\n\n\n"

        # Code
        buffer += "export default function Page(){ return (<>\n\n"
        for tagObject in self.outputData:  # Iterate tags list [[tag_fragment], [tag_fragment], ...]
            # Iterate tag fragment ["<Tags.Title>", "My example title", "</Tags.Title>"]
            buffer += '\t' + tagObject[0] + '\n\t\t' + tagObject[1] + '\n\t' + tagObject[2] + '\n\n'# Join fragments in a sigle line for each tag

        # EOF
        buffer += "\n\n</>)}"

        # Preview
        print(f"==============[ Output file to: {path} ]==============")
        print(buffer)
        print("=====================[ End Of file ]===================")

        # Dump
        with open(path, "w") as fd:
            fd.write(buffer)

    

if __name__ == "__main__":
    converter = N2MW_CLI()

    converter.convert()
    converter.debug()
    converter.exportAsPost("./out.jsx")