#include <iostream>
#include <fstream>

int menu() {
	int opt;
	
	std::cout << "1: read anything" << std::endl;
	std::cout << "2: write anything" << std::endl;
	std::cout << ">> ";
	
	std::cin >> opt;

	return opt;
}

void *get_pointer() {
	unsigned long long address;

	std::cout << "Address: ";
	std::cin >> address;

	return reinterpret_cast<char *>(address);
}

void readany() {
	char *mem = static_cast<char *>(get_pointer());

	int len = 0;
	std::cout << "length: ";
	std::cin >> len;

	if (len > 1000)
		return;

	for (char *p = mem; p < mem + len; p++)
		std::cout << std::hex << *p << " ";

	std::cout << std::endl;
}

void writeany() {
	unsigned long long *mem = static_cast<unsigned long long *>(get_pointer());
	std::cout << "overwrite: ";
	std::cin >> *mem;
}

int main() {
	std::cout.setf(std::ios::unitbuf);
	std::cin.setf(std::ios::unitbuf);

	std::cout << "Let me give you a hint" << std::endl;
	
	std::ifstream maps("/proc/self/maps");
	std::cout << maps.rdbuf();

	while (1) {
		switch (menu()) {
			case 1: readany(); break;
			case 2: writeany(); break;
			default: return 0;
		}
	}
}
