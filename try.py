#!/usr/bin/env python3

# References: https://github.com/trezor/cython-hidapi/blob/master/try.py

import hid
import time
import sys
#from icecream import ic
import binascii

if len(sys.argv) < 2:
  print("Usage: %s <tcpdump file.txt>"%sys.argv[0])
  sys.exit(2)

# enumerate USB devices

for d in hid.enumerate():
  keys = list(d.keys())
  keys.sort()
  for key in keys:
      print("%s : %s" % (key, d[key]))
  print()

print("Opening the device")

h = hid.device()
h.open(0x2047, 0x0301)

print("Manufacturer: %s" % h.get_manufacturer_string())
print("Product: %s" % h.get_product_string())
print("Serial No: %s" % h.get_serial_number_string())

# enable non-blocking mode
h.set_nonblocking(1)

f = open(sys.argv[1], "r")
log = open("log.txt", "wb")
data = b""
for l in f.readlines():
  if l.startswith("\t"):
    pcs = l.split(" ")
    x = "".join(pcs[1:]).strip()
    data += binascii.unhexlify(x)
  else:
    if data.endswith(b"\x00\x00"):
      data = bytearray(data)
      #ic(data)
      data[3] = 0
      assert(len(data) == 64)
      h.write(data)
      log.write(binascii.hexlify(data, " ") + b"\n")

    while True:
      d = h.read(64)
      if d:
        print(d)
      else:
        break
    data = b""

# wait
time.sleep(0.05)


print("Closing the device")
h.close()

