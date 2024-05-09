from PIL import Image, ImageDraw, ImageFont
from sys import stderr
import os
import struct
import zipfile


FLAG_NAME = "privat_flagga_läs_ej.jpg"
ZIP_NAME = "zaknas.zip"

print(f"Generating flag {FLAG_NAME}", file=stderr)

FLAG = "SSM{zn34ky_zn34ky_b1nw4lk_l34ky}"
FONT_SIZE = 30
PADDING = 10

font = ImageFont.truetype("SAX2.ttf", FONT_SIZE)
_, _, twidth, theight = font.getbbox(FLAG)


out_img = Image.new("RGB", (2 * PADDING + twidth, 2 * PADDING + theight), (255, 255, 255))
draw = ImageDraw.Draw(out_img)
draw.text((PADDING, PADDING), FLAG, font=font, fill=(0, 0, 0))

out_img.save(os.path.join("files", FLAG_NAME))

print(f"Generating zipfile [", file=stderr, flush=True, end="")

with zipfile.ZipFile(ZIP_NAME, mode="w", compression=zipfile.ZIP_BZIP2) as z:
    for f in os.listdir("files"):
        if f.startswith("."):
            continue

        print(f, file=stderr, end=", ", flush=True)
        z.write(os.path.join("files", f), f)

print("]", file=stderr)

print(f"Patching zip file", file=stderr)
with open(ZIP_NAME, "r+b") as zf:
    zf.seek(-22, 2) # 2 = END OF STREAM, -22 = size of header

    eocd_offset = zf.tell()
    eocd = zf.read(22)
    magic, _diskn, _cdrdisk, _ndiskcdr, ncdr, sizecdr, cdr_offset, comment_length = struct.unpack("IHHHHIIH", eocd)
    assert magic == 0x06054b50, "Incorrect EOCD header"

    print(f"  CDR @ {hex(cdr_offset)}, #CDR = {ncdr}", file=stderr)

    new_cdr = bytes()
    new_ncdr = 0

    zf.seek(cdr_offset)
    for i in range(ncdr):
        at = zf.tell()
        cdr_hdr = zf.read(46)

        magic, _ver, _verext, _gp, _compmeth, _filemodt, _filemodd, _crc32, _cmpsz, _uncmpsz, nfilename, next, ncmt, _diskn, _intattr, _extattr, file_offset = \
            struct.unpack("=IHHHHHHIIIHHHHHII", cdr_hdr)

        assert magic == 0x02014b50

        vld = zf.read(nfilename + next + ncmt)
        fn = vld[:nfilename]

        print(f"    File {fn.decode()} @ {hex(at)}", file=stderr)
        if fn.lower().decode() == FLAG_NAME.lower():
            print("      Ignoring!", file=stderr)
            continue

        new_cdr = new_cdr + cdr_hdr + vld
        new_ncdr += 1

    zf.seek(cdr_offset)
    zf.write(new_cdr)
    print(f"  Patched CDR", file=stderr)

    eocd_patched = eocd[:8] + struct.pack("H", new_ncdr) + struct.pack("H", new_ncdr) + struct.pack("I", len(new_cdr)) + eocd[16:]
    zf.write(eocd_patched)
    zf.truncate()

    print(f"  Patched CDR", file=stderr)


print(f"Done", file=stderr)
