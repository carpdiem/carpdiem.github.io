## TODO:
## - investigate whether I need to implement a "re-process" functionality

import sys
import requests
from tempfile import mkstemp
from shutil import move, copymode
from urllib.parse import quote
from os import fdopen, remove

def extract_outer_split(s, sep):
    return s.split(sep, maxsplit=1)[1][::-1].split(sep, maxsplit=1)[1][::-1]

def url_encode_string(s, prefix):
    return quote(prefix + s)

def replace(file_path, image_dest, prefix="\LARGE "):
    if image_dest[-1] != '/':
        image_dest += "/"
    #Create temp file
    fh, abs_path = mkstemp()
    count = 0
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                if line.strip()[0:2] == "++" and line.strip()[-2:] == "++":
                    # re-insert existing latex as a comment to maintain editability later
                    new_file.write("{::comment}\n")
                    new_file.write(line)
                    new_file.write("{:/comment}\n")
                    # extract latex
                    latex = "{" + extract_outer_split(line, '++') + "}"
                    # url encode latex + prefix
                    url = "https://latex.codecogs.com/svg.latex?" + quote(latex, prefix)
                    # download and store corresponding image file
                    img = requests.get(url)
                    img_fn = "math" + str(count) + ".svg"
                    with open(image_dest + img_fn, 'wb') as f:
                        f.write(img.content)
                    # write out image link
                    new_file.write("![]({{ site.url }}/" + image_dest + img_fn + ")\n")
                    count += 1
                else:
                    new_file.write(line)
    #Copy the file permissions from the old file to the new file
    copymode(file_path, abs_path)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

## when invoking from command line:
## `python3 processLaTeX.py <path-to-file> <path-to-image-dir>`
if __name__=="__main__":
    replace(sys.argv[1], sys.argv[2])
