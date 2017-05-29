import sys
import struct
import re

def read_array(f, type = "I"):
	ret = []
	length = struct.unpack(type, f.read(4))[0]
	for n in range(length):
		ret.append(struct.unpack(type, f.read(4))[0])
	return ret

def check_magic(f):
	magic = struct.unpack("I", f.read(4))[0]
	if magic != 0x3fcccccd:
		print "Error: invalid magic"
		sys.exit(0)

def dump_thumb(f, offset, length, name):
	f.seek(offset, 0)
	dump = open(name, "wb")
	dump.write(f.read(length))
	dump.close()

def load_index(name):	
	db_file = open(name, "rb")
	check_magic(db_file)
	db_file.seek(4, 1)
	db_ar1 = read_array(db_file)
	db_ar2 = read_array(db_file)
	db_ar3 = read_array(db_file)
	offset_size = zip(db_ar2, db_ar3)
	db_file.close()
	return offset_size

def dump_thumbs(name, thumb_index):
	thumb_file = open(name, "rb")
	check_magic(thumb_file)
	count = 0
	for offset, size in offset_size:
		if offset > 0 and size > 0:
			print offset, size
			dump_thumb(thumb_file, offset, size, sys.argv[2] + "_" + str(count) + ".jpg")
		count += 1
	thumb_file.close()

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Usage: %s <thumb index> <thumbs file>" % (sys.argv[0])
		sys.exit(0)
	thumb_index = load_index(sys.argv[1])
	dump_thumbs(sys.argv[2], thumb_index)
