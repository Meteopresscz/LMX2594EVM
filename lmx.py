#!/usr/bin/env python3

import hid
import time
import sys
import binascii
import re
import logging

logger = logging.getLogger("lmx")


MAGIC_INIT = ["3f0c547004010001006a",
"3f0c54ba04010002000a",
"3f0c54c904010003006a",
"3f0a54c802010004006802",
"3f0c547004010001006a",
"3f0c54ba04010002000a",
"3f0c54c904010003006a",
"3f0a54c802010004006802",
"3f1054ce08010005000800010100010100c0",
"3f1554f30d01000600050101000100000001",
"3f1554d90d01000700060101000100000001"]



def sendmsg(h, msg):
	assert(len(msg) <= 64)
	data = bytearray(msg + b"\x00"*(64-len(msg)))
	d = binascii.hexlify(data, " ")
	#print("SEND: %s"%d)
	logger.debug(d.decode("ascii"))

	assert(len(data) == 64)
	h.write(data)

	while True:
		d = h.read(64)
		if d:
			d = bytearray(d)
			#print("RECV: %s"%binascii.hexlify(d, " "))
		else:
			break

def open_device():
	global serial
	logger.info("Opening the device")

	h = hid.device()
	h.open(0x2047, 0x0301)

	logger.info("Manufacturer: %s" % h.get_manufacturer_string())
	logger.info("Product: %s" % h.get_product_string())
	logger.info("Serial No: %s" % h.get_serial_number_string())

	# enable non-blocking mode
	h.set_nonblocking(1)

	# reset serial
	serial = 8

	logger.info("Sending initializing commands")
	for m in MAGIC_INIT:
		sendmsg(h,binascii.unhexlify(m))
	
	return h

serial = 8
def setreg(h,reg, contents):
	global serial

	assert(reg >= 0 and reg <= 112)
	assert(serial < 255)
	prolog = b"\x3f\x0c\x54"
	checksum = b"\x00" # don't care
	epilog = b"\x04\x01\x00"
	epilog2 = b"\x00\x09\x03"
	data = contents

	msg = prolog + checksum + epilog + bytes([serial]) + epilog2 + data
	sendmsg(h,msg)
	serial += 1

def set_registers(h, regs):
	logger.info("Setting registers")
	for reg,val in regs.items():
		contents = binascii.unhexlify(val)
		setreg(h,reg, contents)
		time.sleep(0.001)

def close_device(h):
	# wait
	time.sleep(0.05)
	logger.info("Closing the device")
	h.close()

def start_pll(regs):
	h = open_device()
	set_registers(h,regs)
	close_device(h)

def parse_regfile(filename):
	regs = {}
	with open(sys.argv[1],"r") as f:
		for line in f:
			m = re.fullmatch("R([0-9]{1,3})\t0x([0-9A-Z]{6})", line.strip())
			if not m:
				print("Bad file format, cannot match %s"%l)
				sys.exit(1)

			reg = int(m.group(1))
			regs[reg] = m.group(2)
	return regs

if __name__ == "__main__":
	logging.basicConfig(level = logging.DEBUG)
	logger = logging.getLogger(__name__)
	if len(sys.argv) < 2:
		print("Usage: %s <file HexRegisterValues.txt>"%sys.argv[0])
		sys.exit(2)
	print("Parsing register file")
	regs = parse_regfile(sys.argv[1])

	start_pll(regs)
	
