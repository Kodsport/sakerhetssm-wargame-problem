
recursive: zig-out/bin/recursive
	strip -o recursive zig-out/bin/recursive

zig-out/bin/recursive: src/main.zig
	zig build -Drelease-small=true
