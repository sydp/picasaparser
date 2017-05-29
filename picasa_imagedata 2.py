import struct
import sys

def check_magic(f):
	magic = struct.unpack("I", f.read(4))[0]
	if magic != 0x3fcccccd:
		print "Error: invalid magic"
		sys.exit(0)

# only handles ASCII strings
def unpackCString(f):
	ret = ""
	c = struct.unpack("b", f.read(1))[0]
	while c != 0:	# TODO: add check for non ascii
		ret += chr(c)	
		c = struct.unpack("b", f.read(1))[0]
	return ret

def load_imagedata(name):	
	f = open(name, "rb")
	check_magic(f)
	data_type = struct.unpack("b", f.read(1))[0]
	f.seek(11,1)
	num_entries = struct.unpack("I", f.read(4))[0]
	index_data = []
	for n in range(num_entries):
		if data_type == 0: 		# string
			index_data.append(unpackCString(f))
		elif data_type == 1:	# 32-bit int
			index_data.append(struct.unpack("I", f.read(4))[0])
	return index_data

if __name__ == "__main__":
	print "\n".join(load_imagedata(sys.argv[1]))
