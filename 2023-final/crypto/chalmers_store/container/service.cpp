#include <iostream>
#include <unordered_map>
#include <set>
#include <vector>
#include <fstream>
#include <string>
#include <chrono>
#include <thread>
#include <cmath>

unsigned long long magic[] = { 4404 ^ 3214, 25954 ^ 3214, 17763 ^ 3124 };
std::unordered_map<unsigned long long, int> values;
std::set<std::string> inventory = {"Video of a cute cat", "Flag", "Picture of a fish"};
std::unordered_map<std::string, std::string> extra = { {"Flag","flag.txt"},{"Video of a cute cat","cat.txt"}, {"Picture of a fish","fish.txt"}};
long long balance = 0;

unsigned long long hashonce(const std::string& s, unsigned long long b)
{
	unsigned long long h = 0;
	unsigned long long m = 1;
	for (auto c : s)
	{
		h = (h + m * c) % 0x1FFFF7;
		m = m * b % 0x1FFFF7;
	}
	return h;
}

unsigned long long powerhash(const std::string& s)
{
	return hashonce(s, magic[0]) + (hashonce(s, magic[1]) << 21) + (hashonce(s, magic[2]) << 42);
}


int getprice(const std::string& s)
{
	unsigned long long snowflake = powerhash(s);
	if (values.find(snowflake)!=values.end())
	{
		return values[snowflake];
	}
	return values[snowflake] = int(1000 * pow(0.67, (double)values.size()));
}

void main_menu()
{
	std::cout << "You currently have " << balance << " chalmers coins" << std::endl;
	std::cout << "Our stock:" << std::endl;
	for (auto item : inventory)
	{
		std::cout << item << ": " << getprice(item) << std::endl;
	}
	std::cout << "What do you want to do? " << std::endl;
	std::cout << "1. Sell" << std::endl;
	std::cout << "2. Buy" << std::endl;
	std::cout << "3. Leave" << std::endl;
}

int main()
{
	unsigned long long coins = 0;
	while (true)
	{
		main_menu();
		std::string command;
		std::getline(std::cin, command);

		if (command=="1")
		{
			std::cout << "What do you want to sell?" << std::endl;
			std::string ware;
			std::getline(std::cin, ware);
			for (auto c : ware)
			{
				if (c<'a'||c>'z')
				{
					std::cout << "Non-ascii wares not allowed!" << std::endl;
					goto end;
				}
			}
			if (inventory.find(ware)!=inventory.end())
			{
				std::cout << "We already have " << ware << " in stock." << std::endl;
				goto end;
			}
			std::cout << "Thanks for selling " << ware << "! I think it's worth around " << getprice(ware) << " chalmers coins" << std::endl;
			inventory.insert(ware);
			balance += getprice(ware);
		}
		else if (command=="2")
		{
			std::cout << "What do you want to buy?" << std::endl;
			std::string ware;
			std::getline(std::cin, ware);

			if (inventory.find(ware)==inventory.end())
			{
				std::cout << "We do not have " << ware << " in stock." << std::endl;
				goto end;
			}
			if (balance<getprice(ware))
			{
				std::cout << "You have too little chalmers coins to buy " << ware << std::endl;
				goto end;
			}
			balance -= getprice(ware);
			inventory.erase(ware);
			std::cout << "Thanks for buying " << ware << "! " << std::endl;


			if (extra.find(ware)!=extra.end())
			{
				std::ifstream f(extra[ware]);
				std::string content;
				f >> content;
				std::cout << "As an extra, we'll throw in " << content << std::endl;
			}
		}
		else if (command=="3")
		{
			std::cout << "Bye bye" << std::endl;
			exit(0);
		}

	end:;
		std::this_thread::sleep_for(std::chrono::milliseconds(2000));
		std::cout << std::endl << std::endl;
	}
}
