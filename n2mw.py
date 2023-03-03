from re import search

from n2mw_parser import N2MW_Parser
from sys import argv


class N2MW_CLI(N2MW_Parser):

    def __init__(self, inputMethod="MD"):
        super().__init__()

        # Parameters
        self.inputmethod = inputMethod
        self.inputPath = ""

        # Buffers
        self.inputData = ""
        self.outputData = []


    def loadFile(self, path):
        """
            Main method to run the app
        """ 
        self.inputPath = path
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

        with open(self.inputPath, 'r', encoding="utf-8") as fd:
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
                    if len(tag) == 3 and tag[0] != "<Tags.Code>": tag[1] = self.parseFontStyle(tag[1])
                    self.outputData.append(tag)  # Parse and append to output tags array
                    

    def exportAsPost(self, path):
        """
            Export the data as a component for the blog to a file
        """

        buffer = ""

        # Imports
        buffer += 'import Tags from "@/components/MarkupWidgets/Tags.js"\n'
        buffer += 'import metadataList from "@/api/blog/postData"\n'
        buffer += "\n\n\n"

        # Metadata (<head></head>)
        buffer += 'export const metadata = metadataList.' + "".join((search("(\w+)\.[jt]sx?", path).groups()) or "POST_ID_HERE")
        buffer += "\n\n\n"

        # Code
        buffer += "export default function Page(){ return (<>\n\n"
        for tagObject in self.outputData:  # Iterate tags list [[tag_fragment], [tag_fragment], ...]
            # Iterate tag fragment ["<Tags.Title>", "My example title", "</Tags.Title>"]
            if len(tagObject) == 3:  # Parse wrapper tags
                buffer += '\t' + tagObject[0] + '\n\t\t' + tagObject[1] + '\n\t' + tagObject[2] + '\n\n'# Join fragments in a sigle line for each tag
            else:  # Parse one-line tags
                buffer += '\t' + tagObject[0] + '\n\n'

        # EOF
        buffer += "\n\n</>)}"

        # Preview
        print(f"==============[ Output file to: {path} ]==============")
        print(buffer)
        print("=====================[ End Of file ]===================")

        # Dump
        try:
            with open(path, "w", encoding="utf-8") as fd:
                fd.write(buffer)
        except UnicodeEncodeError:
            print("\n[!] EXCEPTION Captured: Error dumping unicode characters (emogi, tildes, greek letters, ...)")

    

if __name__ == "__main__":
    converter = N2MW_CLI()

    if len(argv) == 1:
        print("\n\t[i] Usage: python3 n2mw.py <inputPath> <outputPath>\n")
        print("\t[i] Exaple: python3 n2mw.py ./in.md ./out.jsx \n")
        
        print("\t[i] Entering interacive mode...")

        inputPath = input("\t[>] Input path: ").strip(' "\'&')
        outputPath = input("\t[>] Output path (./out.jsx): ").strip(' "')

        converter.loadFile(inputPath)
        converter.exportAsPost(outputPath)
    else:
        converter.loadFile(argv[1])
        converter.exportAsPost(argv[2])

