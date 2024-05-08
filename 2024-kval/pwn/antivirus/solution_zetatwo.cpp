// clang++ -O0 -static -o solution_zetatwo solution_zetatwo.cpp

#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <iostream>
#include <fstream>

constexpr uint64_t F = 172933ul;
constexpr size_t M = 700;
constexpr size_t N = 300;

template<uint64_t sum, uint64_t count>
class adder {
    public:
    __attribute__((always_inline))
    static inline uint64_t add() {
        
        return sum+adder<sum-F, count-1>::add();
    }
};

template<uint64_t sum>
class adder<sum, 0> {
    public:
    __attribute__((always_inline))
    static inline uint64_t add() {
        return 0;
    }
};

template<uint64_t delta>
void addadd() {
    printf("Res: %lx\n", adder<0x100000000 + delta*1000*F, M>::add());
    addadd<delta-1>();
}

template<>
void addadd<0>() {
    return;
}

int main() {
    addadd<N>();
    std::ifstream f("/flag");
    if (f.is_open())
        std::cout << f.rdbuf();
    return 0;
}
