#!/usr/bin/python
#
#   This script will extract the thumbnail images from a Google Picasa 
#	thumbnail file i.e. previews.db, thumbs_0.db, etc..
#       
#   Copyright 2014 Syd Pleno <syd dot pleno at gmail dot com>
#   
#   Licensed under GNU General Public License 3.0 or later.
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import struct

def read_array(f, type = "I"):
	ret = []
	length = struct.unpack("I", f.read(4))[0]
	for n in range(length):
		ret.append(struct.unpack(type, f.read(struct.calcsize(type)))[0])
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
	db_ar1 = read_array(db_file)	# unknown
	db_ar2 = read_array(db_file)	# offset
	db_ar3 = read_array(db_file)	# preview file index (8 bit) / size (24 bit) 
	offset_size = zip(db_ar2, db_ar3)
	db_file.close()
	return offset_size

def getOffset(val):
	return val >> 24

def getSize(val):
	return val & 0x00FFFFFF

def dump_thumbs(name, thumb_index):
	count = 0
	for offset, val in thumb_index:
		#print hex(val), getSize(val), getPreviewFileIndex(val)
		if offset > 0 and getSize(val) > 0:
			if getOffset(val) > 0:
				name = name.replace(0, getOffset(val))
			thumb_file = open(name, "rb")
			check_magic(thumb_file)
			dump_thumb(thumb_file, offset, getSize(val), name + "_" + str(count) + ".jpg")
		count += 1
	thumb_file.close()

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Usage: %s <thumb index> <thumbs file>" % (sys.argv[0])
		sys.exit(0)
	thumb_index = load_index(sys.argv[1])
	dump_thumbs(sys.argv[2], thumb_index)
