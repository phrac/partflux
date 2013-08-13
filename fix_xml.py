# coding: ascii
# Find numeric character references that refer to Unicode code points
# that are not valid in XML.
# Get byte offsets for seeking etc in undecoded file bytestreams.
# Get unicode offsets for checking against ElementTree error message,
# **IF** your input file is small enough. 

BYTE_OFFSETS = False
import sys, re, codecs
fname = sys.argv[1]
print fname
if BYTE_OFFSETS:
    text = open(fname, "rb").read()
else:
    # Assumes file is encoded in UTF-8.
    text = codecs.open(fname, "rb", "utf8").read()
rx = re.compile("&#([0-9]+);|&#x([0-9a-fA-F]+);")
endpos = len(text)
pos = 0
while pos < endpos:
    m = rx.search(text, pos)
    if not m: break
    mstart, mend = m.span()
    target = m.group(1)
    if target:
        num = int(target)
    else:
        num = int(m.group(2), 16)
    # #x9 | #xA | #xD | [#x20-#xD7FF] | [#xE000-#xFFFD] | [#x10000-#x10FFFF]
    if not(num in (0x9, 0xA, 0xD) or 0x20 <= num <= 0xD7FF
    or 0xE000 <= num <= 0xFFFD or 0x10000 <= num <= 0x10FFFF):
        print mstart, m.group()
    pos = mend