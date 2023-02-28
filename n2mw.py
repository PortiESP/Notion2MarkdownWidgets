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
                    
    def exportAsPost(self, path):
        """
            Export the data as a component for the blog to a file
        """

        buffer = ""

        # Imports
        buffer += 'import Tags from "@/components/MarkupWidgets/Tags.js"\n'
        buffer += "\n\n\n"

        # Code
        buffer += "export default function Page(){ return (<>\n\n\t"
        for tagObject in self.outputData:  # Iterate tags list [[tag_fragment], [tag_fragment], ...]
            for tagFragments in tagObject:  # Iterate tag fragment ["<Tags.Title>", "My example title", "</Tags.Title>"]
                buffer += "".join(tagFragments)  # Join fragments in a sigle line for each tag
            buffer += "\n\n\t"  # Join each tag with a two line-break spearation

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