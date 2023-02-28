import re 


data = "![This is a template alt text](https://cdn.sstatic.net/Img/home/illo-public.svg?v=14bd5a506009)"

# patternAlt = "[\w\s]+"
# patternUrl = "https?:\/\/[\w\.\\\/-\?=]+"
charsetSymbols = "!\.\-\_@#%\?=\/:"
charsetAlt = f"\w\s{charsetSymbols}"
charsetUrl = f"\w\s{charsetSymbols}"
src, alt = re.search(f'!\[([{charsetAlt}]+)\]\(([{charsetUrl}]+)\)', data).groups()

print(src, alt)