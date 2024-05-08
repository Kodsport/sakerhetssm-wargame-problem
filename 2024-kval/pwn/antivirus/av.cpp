#include <fstream>
#include <iostream>
#include <unordered_map>

using namespace std;

typedef __uint64_t	Elf64_Addr;
typedef __uint16_t	Elf64_Half;
typedef __int16_t	Elf64_SHalf;
typedef __uint64_t	Elf64_Off;
typedef __int32_t	Elf64_Sword;
typedef __uint32_t	Elf64_Word;
typedef __uint64_t	Elf64_Xword;
typedef __int64_t	Elf64_Sxword;

#define EI_NIDENT	16

struct Elf64_Ehdr {
        unsigned char   e_ident[EI_NIDENT];
        Elf64_Half      e_type;
        Elf64_Half      e_machine;
        Elf64_Word      e_version;
        Elf64_Addr      e_entry;
        Elf64_Off       e_phoff;
        Elf64_Off       e_shoff;
        Elf64_Word      e_flags;
        Elf64_Half      e_ehsize;
        Elf64_Half      e_phentsize;
        Elf64_Half      e_phnum;
        Elf64_Half      e_shentsize;
        Elf64_Half      e_shnum;
        Elf64_Half      e_shstrndx;
};

#define	EI_MAG0		0		/* e_ident[] indexes */
#define	EI_MAG1		1
#define	EI_MAG2		2
#define	EI_MAG3		3
#define	EI_CLASS	4
#define	EI_DATA		5
#define	EI_VERSION	6
#define	EI_OSABI	7
#define	EI_PAD		8

#define	ELFMAG0		0x7f		/* EI_MAG */
#define	ELFMAG1		'E'
#define	ELFMAG2		'L'
#define	ELFMAG3		'F'

#define	ELFCLASS64	2

void check(bool value, const char* msg) {
    if (!value) {
        cerr << msg << endl;
        exit(1);
    }
}

Elf64_Ehdr* parse_header(char* buf, size_t size) {
    check(size >= sizeof(Elf64_Ehdr), "Header EOF");
    Elf64_Ehdr *hdr = reinterpret_cast<Elf64_Ehdr*>(buf);

    check(hdr->e_ident[EI_MAG0] == ELFMAG0, "MAG0");
    check(hdr->e_ident[EI_MAG1] == ELFMAG1, "MAG1");
    check(hdr->e_ident[EI_MAG2] == ELFMAG2, "MAG2");
    check(hdr->e_ident[EI_MAG3] == ELFMAG3, "MAG3");

    check(hdr->e_ident[EI_CLASS] == ELFCLASS64, "CLASS");
    check(hdr->e_ident[EI_DATA] == 1, "DATA");
    check(hdr->e_ident[EI_VERSION] == 1, "VERSION");
    check(hdr->e_ident[EI_OSABI] == 3, "ABI");

    check(hdr->e_type == 2, "TYPE");
    check(hdr->e_machine == 62, "ARCH");
    check(hdr->e_version == 1, "VERSION");

    check(hdr->e_ehsize == sizeof(Elf64_Ehdr), "EHSIZE");
    return hdr;
}

unordered_map<long long, int> sigs;

void check_signatures(char* buf, size_t size) {
    for (int i = 0; i < size - 7; i++, buf++) {
        long long sig = *reinterpret_cast<long long*>(buf);
        sigs[sig]++;
    }
}

void check_forbidden_bytes(char* buf, size_t size) {
    for (int i = 0; i < size; i++, buf++) {
        check(*buf != 0xe8, "CALL1");
        check(*buf != 0xff, "CALL2");
        check(*buf != 0x9a, "CALL3");
        check(*buf != 0x0f, "SYSCALL");
    }
}

typedef struct {
	Elf64_Word	sh_name;
	Elf64_Word	sh_type;
	Elf64_Xword	sh_flags;
	Elf64_Addr	sh_addr;
	Elf64_Off	sh_offset;
	Elf64_Xword	sh_size;
	Elf64_Word	sh_link;
	Elf64_Word	sh_info;
	Elf64_Xword	sh_addralign;
	Elf64_Xword	sh_entsize;
} Elf64_Shdr;

void parse_sections(char* buf, Elf64_Ehdr* hdr, size_t size) {
    size_t sht_off = hdr->e_shoff;
    check(hdr->e_shentsize == sizeof(Elf64_Shdr), "SHENTSIZE");
    size_t sht_size = sizeof(Elf64_Shdr) * hdr->e_shnum;
    check(sht_off <= size, "SHT OFFSET");
    check(size - sht_off >= sht_size, "SHT SIZE");

    for (size_t i = 0; i < hdr->e_shnum; i++) {
        Elf64_Shdr* shdr = reinterpret_cast<Elf64_Shdr*>(buf + sht_off + i * sizeof(Elf64_Shdr)); 
        if (shdr->sh_flags & 0x4) {
            check(shdr->sh_offset <= size, "S OFFSET");
            check(size - shdr->sh_offset >= shdr->sh_size, "S OFFSET");
            check_signatures(buf + shdr->sh_offset, shdr->sh_size);
        }
    }
    check(sigs[0xfa1e0ff3] == 0, "endbr64");
    for (size_t i = 0; i < hdr->e_shnum; i++) {
        Elf64_Shdr* shdr = reinterpret_cast<Elf64_Shdr*>(buf + sht_off + i * sizeof(Elf64_Shdr)); 
        if (shdr->sh_flags & 0x4) {
            check_forbidden_bytes(buf + shdr->sh_offset, shdr->sh_size);
        }
    }
}

int main(int argc, char** argv) {
    ifstream binary(string(argv[1]), ios::binary | ios::ate);
    size_t binary_size = binary.tellg();
    binary.seekg(0);

    char* buf = new char[binary_size];
    binary.read(buf, binary_size);

    Elf64_Ehdr* hdr = parse_header(buf, binary_size);
    parse_sections(buf, hdr, binary_size);

    delete[] buf;
}
