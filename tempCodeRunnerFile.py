
        print("\n\t[i] Usage: python3 n2mw.py <inputPath> <outputPath>\n")
        print("\t[i] Exaple: python3 n2mw.py ./in.md ./out.jsx \n")
    else:
        converter.loadFile(argv[1])
        converter.exportAsPost(argv[2])