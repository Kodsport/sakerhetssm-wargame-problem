dd if=/dev/zero of=empty_filesystem bs=512 count=32768
mkfs.fat -F 16 -s 1 -f 1 empty_filesystem