const fs = require("fs");

const CRC_LOOKUP = [
	0x00000000, 0x77073096, 0xEE0E612C, 0x990951BA, 0x076DC419, 0x706AF48F,
	0xE963A535, 0x9E6495A3, 0x0EDB8832, 0x79DCB8A4, 0xE0D5E91E, 0x97D2D988,
	0x09B64C2B, 0x7EB17CBD, 0xE7B82D07, 0x90BF1D91, 0x1DB71064, 0x6AB020F2,
	0xF3B97148, 0x84BE41DE, 0x1ADAD47D, 0x6DDDE4EB, 0xF4D4B551, 0x83D385C7,
	0x136C9856, 0x646BA8C0, 0xFD62F97A, 0x8A65C9EC, 0x14015C4F, 0x63066CD9,
	0xFA0F3D63, 0x8D080DF5, 0x3B6E20C8, 0x4C69105E, 0xD56041E4, 0xA2677172,
	0x3C03E4D1, 0x4B04D447, 0xD20D85FD, 0xA50AB56B, 0x35B5A8FA, 0x42B2986C,
	0xDBBBC9D6, 0xACBCF940, 0x32D86CE3, 0x45DF5C75, 0xDCD60DCF, 0xABD13D59,
	0x26D930AC, 0x51DE003A, 0xC8D75180, 0xBFD06116, 0x21B4F4B5, 0x56B3C423,
	0xCFBA9599, 0xB8BDA50F, 0x2802B89E, 0x5F058808, 0xC60CD9B2, 0xB10BE924,
	0x2F6F7C87, 0x58684C11, 0xC1611DAB, 0xB6662D3D, 0x76DC4190, 0x01DB7106,
	0x98D220BC, 0xEFD5102A, 0x71B18589, 0x06B6B51F, 0x9FBFE4A5, 0xE8B8D433,
	0x7807C9A2, 0x0F00F934, 0x9609A88E, 0xE10E9818, 0x7F6A0DBB, 0x086D3D2D,
	0x91646C97, 0xE6635C01, 0x6B6B51F4, 0x1C6C6162, 0x856530D8, 0xF262004E,
	0x6C0695ED, 0x1B01A57B, 0x8208F4C1, 0xF50FC457, 0x65B0D9C6, 0x12B7E950,
	0x8BBEB8EA, 0xFCB9887C, 0x62DD1DDF, 0x15DA2D49, 0x8CD37CF3, 0xFBD44C65,
	0x4DB26158, 0x3AB551CE, 0xA3BC0074, 0xD4BB30E2, 0x4ADFA541, 0x3DD895D7,
	0xA4D1C46D, 0xD3D6F4FB, 0x4369E96A, 0x346ED9FC, 0xAD678846, 0xDA60B8D0,
	0x44042D73, 0x33031DE5, 0xAA0A4C5F, 0xDD0D7CC9, 0x5005713C, 0x270241AA,
	0xBE0B1010, 0xC90C2086, 0x5768B525, 0x206F85B3, 0xB966D409, 0xCE61E49F,
	0x5EDEF90E, 0x29D9C998, 0xB0D09822, 0xC7D7A8B4, 0x59B33D17, 0x2EB40D81,
	0xB7BD5C3B, 0xC0BA6CAD, 0xEDB88320, 0x9ABFB3B6, 0x03B6E20C, 0x74B1D29A,
	0xEAD54739, 0x9DD277AF, 0x04DB2615, 0x73DC1683, 0xE3630B12, 0x94643B84,
	0x0D6D6A3E, 0x7A6A5AA8, 0xE40ECF0B, 0x9309FF9D, 0x0A00AE27, 0x7D079EB1,
	0xF00F9344, 0x8708A3D2, 0x1E01F268, 0x6906C2FE, 0xF762575D, 0x806567CB,
	0x196C3671, 0x6E6B06E7, 0xFED41B76, 0x89D32BE0, 0x10DA7A5A, 0x67DD4ACC,
	0xF9B9DF6F, 0x8EBEEFF9, 0x17B7BE43, 0x60B08ED5, 0xD6D6A3E8, 0xA1D1937E,
	0x38D8C2C4, 0x4FDFF252, 0xD1BB67F1, 0xA6BC5767, 0x3FB506DD, 0x48B2364B,
	0xD80D2BDA, 0xAF0A1B4C, 0x36034AF6, 0x41047A60, 0xDF60EFC3, 0xA867DF55,
	0x316E8EEF, 0x4669BE79, 0xCB61B38C, 0xBC66831A, 0x256FD2A0, 0x5268E236,
	0xCC0C7795, 0xBB0B4703, 0x220216B9, 0x5505262F, 0xC5BA3BBE, 0xB2BD0B28,
	0x2BB45A92, 0x5CB36A04, 0xC2D7FFA7, 0xB5D0CF31, 0x2CD99E8B, 0x5BDEAE1D,
	0x9B64C2B0, 0xEC63F226, 0x756AA39C, 0x026D930A, 0x9C0906A9, 0xEB0E363F,
	0x72076785, 0x05005713, 0x95BF4A82, 0xE2B87A14, 0x7BB12BAE, 0x0CB61B38,
	0x92D28E9B, 0xE5D5BE0D, 0x7CDCEFB7, 0x0BDBDF21, 0x86D3D2D4, 0xF1D4E242,
	0x68DDB3F8, 0x1FDA836E, 0x81BE16CD, 0xF6B9265B, 0x6FB077E1, 0x18B74777,
	0x88085AE6, 0xFF0F6A70, 0x66063BCA, 0x11010B5C, 0x8F659EFF, 0xF862AE69,
	0x616BFFD3, 0x166CCF45, 0xA00AE278, 0xD70DD2EE, 0x4E048354, 0x3903B3C2,
	0xA7672661, 0xD06016F7, 0x4969474D, 0x3E6E77DB, 0xAED16A4A, 0xD9D65ADC,
	0x40DF0B66, 0x37D83BF0, 0xA9BCAE53, 0xDEBB9EC5, 0x47B2CF7F, 0x30B5FFE9,
	0xBDBDF21C, 0xCABAC28A, 0x53B39330, 0x24B4A3A6, 0xBAD03605, 0xCDD70693,
	0x54DE5729, 0x23D967BF, 0xB3667A2E, 0xC4614AB8, 0x5D681B02, 0x2A6F2B94,
	0xB40BBE37, 0xC30C8EA1, 0x5A05DF1B, 0x2D02EF8D
];

function crc32(buffer, crc = 0) {
	return (
		~ buffer.reduce(
			(crc, v) => CRC_LOOKUP[(crc ^ v) & 0xff] ^ (crc >>> 8),
			~ crc
		)
	) >>> 0;
}

function adler32(buffer) {
	let a = 1;
	let b = 0;
	for (let i = 0; i < buffer.length; i++) {
		a = (a + buffer[i]) % 65521;
		b = (b + a) % 65521;
	}
	return (b << 16) | a;

}

let outBuf = new ArrayBuffer(0, { maxByteLength: 1024 * 1024 * 1024 });
let out = new Uint8Array(outBuf);
let outi = 0;

let header = [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A];
outBuf.resize(header.length);
out.set(header, 0); outi += header.length;

function hexEncode(n) {
	return n.toString(16).padStart(8, "0").match(/.{2}/g).map(a => parseInt(a, 16))
}

function appendBlock(type, data) {
	outBuf.resize(outi + 4 + 4 + data.length + 4);
	out.set(hexEncode(data.length), outi); outi += 4;
	let block = new Uint8Array(4 + data.length);
	block.set(type.split("").map(a => a.charCodeAt()), 0);
	block.set(data, 4);
	out.set(block, outi); outi += block.length;
	out.set(hexEncode(crc32(block)), outi); outi += 4;
}

let width, height;
width = height = 2**20;

let ihdr = [];
ihdr.push(...hexEncode(width)); // width
ihdr.push(...hexEncode(height)); // height
ihdr.push(1); // bit depth
ihdr.push(0); // grayscale
ihdr.push(0); // compression
ihdr.push(0); // filter
ihdr.push(0); // no interlace

appendBlock("IHDR", ihdr);

/*appendBlock("IDAT", zlib.deflateSync(Buffer.from([
	...Array(1024).fill([0x00, ...Array(1024 / 8).fill(0x00)]).flat()
])));*/


// SSM{p3t4by7e_n3tw0rk_6r4ph1c5}
let qr = `\
111111111111111111111111111111111
111111111111111111111111111111111
111111111111111111111111111111111
111111111111111111111111111111111
111100000001110011011100000001111
111101111101000111100101111101111
111101000101100111110101000101111
111101000101001110000101000101111
111101000101111001010101000101111
111101111101010110101101111101111
111100000001010101010100000001111
111111111111111001100111111111111
111100000100000100000010101011111
111101011111101010110010110101111
111110101100001110100111011001111
111101010110000101011001111011111
111110001101001111000101010101111
111101000011000000011010100001111
111101100100101100001001110001111
111101010010000101010010111011111
111101110001011000110000010101111
111111111111010011000111001001111
111100000001001100010101001001111
111101111101110101110111001111111
111101000101001110000000010011111
111101000101001011010000001001111
111101000101001100110111110101111
111101111101001111111001111101111
111100000001001110111000110001111
111111111111111111111111111111111
111111111111111111111111111111111
111111111111111111111111111111111
111111111111111111111111111111111`.split("\n");

let x = Math.floor((width - qr[0].length) / 2 / 8) * 8;
let y = Math.floor((height - qr.length) / 2);

console.log(x, y);

let buf = new ArrayBuffer(0, { maxByteLength: 1024 * 1024 * 1024 });
let deflate = new Uint8Array(buf);
let bi = 0;
function append_bit(bit) {
	if ((bi >> 3) >= deflate.length) {
		buf.resize((bi >> 3) + 1);
	}
	deflate[bi >> 3] |= bit << (bi & 7);
	bi++;
}
function append_bits(bits) {
	for (let bit of bits) {
		append_bit(parseInt(bit, 2));
	}
}

function append_literal(bytes) {
	append_bits("0" + "00");
	append_bits("0".repeat((8 - (bi % 8)) % 8));
	let len = bytes.length.toString(2).padStart(16, "0");
	append_bits(len.slice(8).split("").reverse().join("") + len.slice(0, 8).split("").reverse().join(""));
	let clen = (~bytes.length & 0xffff).toString(2).padStart(16, "0");
	append_bits(clen.slice(8).split("").reverse().join("") + clen.slice(0, 8).split("").reverse().join(""));
	append_bits(bytes.map(a => a.toString(2).padStart(8, "0").split("").reverse().join("")).join(""));
}

function append_zeros(n) {
	if (n >= 259) {
		n -= 1;
		append_bits("0" + "01");
		append_bits("10111" + "00000" + "0111");
		append_bits("000" + "000" + "100" + "000" + "000" + "000" + "000" + "000" + "000" + "000" + "000" + "000" + "000" + "000" + "000" + "010" + "000" + "010");
		append_bits("11" + "0" + "1111111" + "0" + "0101011" + "11" + "0" + "1000100" + "10" + "10");
		append_bits("10");
		for (let i = 0; i < Math.floor(n / 258); i++) {
			append_bit(0);
			append_bit(0);
		}
		append_bits("11");
	}
	if (n % 258 != 0) {
		append_literal(Array(n % 258).fill(0));
	}
}

//let deflate = "0 01 10111 00000 0111  000 000 100 000 000 000 000 000 000 000 000 000 000 000 000 010 000 010  11 0 1111111 0 0101011 11 0 1000100 10 10";
//deflate += "10" + "0 0".repeat(Math.floor((y * (1 + width / 8) + 1 + x) / 259)) + "11";

//append_zeros(y * (1 + width / 8) + 1);
let bytes = 0;
append_zeros(y * (1 + width / 8) + 1 + x / 8);
bytes += y * (1 + width / 8) + 1 + x / 8;
for (let yy = 0; yy < qr.length; yy++) {
	append_literal(qr[yy].match(/.{1,8}/g).map(a => parseInt(a.padEnd(8, 0), 2)));
	bytes += qr[yy].match(/.{1,8}/g).length;
	if (yy != qr.length - 1) {
		append_zeros(1 + width / 8 - Math.ceil(qr[yy].length / 8));
		bytes += 1 + width / 8 - Math.ceil(qr[yy].length / 8);
	}
}

append_zeros(height * (1 + width / 8) - bytes);


//append_literal(Array(64).fill([0x00, ...Array(64 / 8).fill(0xff)]).flat());

// end
append_bits("1" + "10");
append_bits("000000000");


//deflate = deflate.replaceAll(" ", "").match(/.{1,8}/g).map(a => parseInt(a.padEnd(8, 0).split("").reverse().join(""), 2));

let csum = adler32(deflate);

let idat = new Uint8Array(2 + deflate.length + 4);
idat.set([
	0x78, // deflate, 32k window size
	0xda  // maximum compression
], 0);
idat.set(deflate, 2);
idat.set(hexEncode(csum), 2 + deflate.length);

appendBlock("IDAT", idat);

appendBlock("IEND", []);

fs.writeFileSync("out.png", out);