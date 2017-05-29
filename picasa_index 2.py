# todo
# option to split HTML
# option to dump just CSV of index data
# option to ignore "face detection" rows
# option to dump extra imagedata metadata

import struct
import sys
import os.path
from picasa_thumbs import load_index, dump_thumbs
from picasa_imagedata import load_imagedata

def unpack (format, buffer) :
    while True :
        pos = format.find ('z')
        if pos < 0 :
            break
        asciiz_start = struct.calcsize (format[:pos])
        asciiz_len = buffer[asciiz_start:].find('\0')
        format = '%s%dsx%s' % (format[:pos], asciiz_len, format[pos+1:])
    return (struct.unpack_from (format, buffer), struct.calcsize(format))

def load_filenames (name) :
    file = open(name, "rb")
    magic = struct.unpack("I", file.read(4))[0]
    if magic != 0x40466666:
        print "Error: invalid magic"
        sys.exit(0)
    
    count = struct.unpack("I", file.read(4))[0]
    buffer = file.read()
    file.close()
    buffer_offset = 0
    filenames = []
    for n in range(count):
        record = unpack("<z26xi", buffer[buffer_offset:])
        buffer_offset += record[1]
        filenames.append(record[0])
        
    return filenames
    
def dump_csv() :
    print "Index\tName\tParent\tbigthumbs offset\tbigthumbs size\tthumbs_0 offset\tthumbs_0 size\tthumbs2_0 offset\tthumbs2_0\tpreviews offset\tpreviews size"
    for n in range(len(filenames)):
        if filenames[n][0] == "":
            print n,"\t",filenames[n][0],"\t",filenames[n][1],"\t",thumb_indexes[0][n][0],"\t",thumb_indexes[0][n][1],"\t",thumb_indexes[1][n][0],"\t",thumb_indexes[1][n][1],"\t",thumb_indexes[2][n][0],"\t",thumb_indexes[2][n][1]
        else:
            print n,"\t",filenames[n][0],"\t",filenames[n][1],"\t",thumb_indexes[0][n][0],"\t",thumb_indexes[0][n][1],"\t",thumb_indexes[1][n][0],"\t",thumb_indexes[1][n][1],"\t",thumb_indexes[2][n][0],"\t",thumb_indexes[2][n][1],"\t",thumb_indexes[3][n][0],"\t",thumb_indexes[3][n][1]

def dump_html(filenames, thumb_indexes, imagedatum):
    print "<html><body><table border=\"1\">"
    print "<tr><td>Index</td><td>Name</td><td>Parent</td><td>bigthumbs_0.db Preview</td><td>thumbs_0.db Preview</td><td>thumbs2_0.db Preview</td><td>previews_0.db Preview</td><td>Original Height</td><td>Original Width</td></tr>"
    for n in range(len(filenames)):
        if filenames[n][1] == -1:
            print "<tr><td>%s</td><td>%s</td><td>Directory</td><td>N/A</td><td>N/A</td><td>N/A</td><td>N/A</td><td>N/A</td><td>N/A</td></tr>" % (n, filenames[n][0])
        else:
            bigthumbs = "Not present"
            parent_folder = filenames[filenames[n][1]][0]
            if os.path.exists("bigthumbs_0.db_%s.jpg" % n):
                bigthumbs = "<img src=\"bigthumbs_0.db_%s.jpg\">" % n
            preview = "Not present"
            if filenames[n][0] != "" and os.path.exists("previews_0.db_%s.jpg" % n):
                preview = "<a href=\"previews_0.db_%s.jpg\">View</a>" % (n) 
            # face detected
            elif filenames[n][0] == "" and os.path.exists("previews_0.db_%s.jpg" % filenames[n][1]):
                    preview = "<a href=\"previews_0.db_%s.jpg\">Face detected in %s</a>" % (filenames[n][1], filenames[n][1])
                    parent_folder = "%s%s" % (filenames[filenames[filenames[n][1]][1]][0], filenames[filenames[n][1]][0])
            print "<tr><td>%s</td><td>%s</td><td>(%s) - %s</td><td>%s</td><td><img src=\"thumbs_0.db_%s.jpg\"></td><td><img src=\"thumbs2_0.db_%s.jpg\"></td><td>%s</td><td>%s</td><td>%s</td></tr>" % (n, filenames[n][0], filenames[n][1], parent_folder, bigthumbs, n, n, preview, imagedatum["Original Height"][n], imagedatum["Original Width"][n])
    print "</table></body></html>"


filenames = load_filenames("thumbindex.db" if len(sys.argv) == 1 else sys.argv[1])

thumbfiles = [("bigthumbs_0.db", "bigthumbs_index.db"), ("thumbs_0.db", "thumbs_index.db"), ("thumbs2_0.db", "thumbs2_index.db"), ("previews_0.db", "previews_index.db")]
thumb_indexes = {}
for thumbfile in thumbfiles:
    thumb_index = load_index(thumbfile[1])
    dump_thumbs(thumbfile[0], thumb_index)
    thumb_indexes[thumbfile[1]] = thumb_index

imagedatafiles = [("imagedata_height.pmp", "Original Height"), ("imagedata_width.pmp", "Original Width")]
imagedatum = {}
for imagedatafile in imagedatafiles:
    imagedata = load_imagedata(imagedatafile[0])
    imagedatum[imagedatafile[1]] = imagedata

dump_html(filenames, thumb_indexes, imagedatum)

    
    
