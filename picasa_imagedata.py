#!/usr/bin/python
#
#   This script will extract metadata from a Google Picasa PMP file
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
