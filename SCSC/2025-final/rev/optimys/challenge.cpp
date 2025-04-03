#include <array>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <cstring>

#include <immintrin.h>
#include <smmintrin.h>

#include "parameters.hpp"

const size_t blocksize = 16;
typedef std::array<uint8_t, blocksize> arrayblock;
typedef __m128i block;
typedef std::array<block, blocksize> sbox;

static const sbox SBOX_AVX = {
    *(__m128i *)&SBOX[0],
    *(__m128i *)&SBOX[16],
    *(__m128i *)&SBOX[32],
    *(__m128i *)&SBOX[48],
    *(__m128i *)&SBOX[64],
    *(__m128i *)&SBOX[80],
    *(__m128i *)&SBOX[96],
    *(__m128i *)&SBOX[112],
    *(__m128i *)&SBOX[128],
    *(__m128i *)&SBOX[144],
    *(__m128i *)&SBOX[160],
    *(__m128i *)&SBOX[176],
    *(__m128i *)&SBOX[192],
    *(__m128i *)&SBOX[208],
    *(__m128i *)&SBOX[224],
    *(__m128i *)&SBOX[240],
};

static block KEY_AVX = *(__m128i *)&KEY[0];

static constexpr block array_to_block(const arrayblock &data)
{
    return _mm_loadu_si128((block *)data.data());
}

static constexpr void block_to_array(const block &val, arrayblock &data)
{
    _mm_storeu_si128((block *)data.data(), val);
}

// Apply an sbox to input and return the result
static const block substitute_avx(const block &in, const sbox &sbox)
{
    block cur = in;
    block res = _mm_setzero_si128();
    const block cmp = _mm_set1_epi8(blocksize);

    for (size_t i = 0; i < blocksize; i++)
    {
        // Select elements in scope
        block min = _mm_min_epu8(cur, cmp);
        block is_less_mask = ~_mm_cmpeq_epi8(min, cmp);

        // Substitute all elements
        block substituted = _mm_shuffle_epi8(sbox[i], cur);

        // Apply substitutions in scope
        block substituted_relevant = _mm_and_si128(substituted, is_less_mask);
        res = _mm_or_si128(res, substituted_relevant);

        // Select next slice
        cur = _mm_sub_epi8(cur, cmp);
    }

    return res;
}

#ifdef DEBUG
static const block substitute(const block &in, const uint8_t *const &sbox)
{
    arrayblock tmp;
    block_to_array(in, tmp);
    for (size_t i = 0; i < blocksize; i++)
    {
        tmp[i] = sbox[tmp[i]];
    }

    block res = array_to_block(tmp);
    return res;
}

static const void print_block(const block &in) {
    arrayblock out;
    block_to_array(in, out);
    for (size_t i = 0; i < blocksize; i++)
    {
        int tmp = out[i];
        std::cerr << std::hex << std::setw(2) << std::setfill('0') << tmp;
        if(i+1==blocksize) {
            std::cerr << std::endl;
        } else {
            std::cerr << " ";
        }
    }
}
#endif

static const block permute_avx(const block &in)
{
    uint64_t halves[2];
    _mm_storeu_si128((block *)halves, in);
#ifdef DEBUG
    std::cerr << "halves " << std::hex << halves[0] << " : " << halves[1] << std::endl;
#endif
    uint64_t l1 = _pext_u64(halves[0], mask1);
    uint64_t l2 = _pext_u64(halves[0], ~mask1);
    uint64_t r1 = _pext_u64(halves[1], mask2);
    uint64_t r2 = _pext_u64(halves[1], ~mask2);

#ifdef DEBUG
    std::cerr << "quarters " << std::hex << l1 << " " << l2 << " " << r1 << " " << r2 << std::endl;
#endif
    block res = _mm_setr_epi32(l1, r1, r2, l2);

    return res;
}

static const block round(const block &in, const block &round_key)
{
    block cur = in ^ round_key;
#ifdef DEBUG
    std::cerr << "pre sub ";
    print_block(cur);
#endif
    cur = substitute_avx(cur, SBOX_AVX);
#ifdef DEBUG
    std::cerr << "post sub ";
    print_block(cur);
#endif
    cur = permute_avx(cur);
#ifdef DEBUG
    std::cerr << "post perm ";
    print_block(cur);
#endif
    return cur;
}

static const block encrypt(const block &input_block)
{
    block cur_key = KEY_AVX;
    block round_mul = _mm_set1_epi16(7);
    block current = input_block;
    for (int i = 0; i < 8; i++)
    {
        cur_key = _mm_mullo_epi16(cur_key, round_mul);
#ifdef DEBUG
        std::cerr << "round key ";
        print_block(cur_key);
#endif
        current = round(current, cur_key);
    }
    cur_key = _mm_mullo_epi16(cur_key, round_mul);
#ifdef DEBUG
    print_block(cur_key);
#endif
    current = current ^ cur_key;

    return current;
}

static const arrayblock encrypt_array(const arrayblock &input_block)
{
    block current = array_to_block(input_block);
    current = encrypt(current);
    arrayblock result_block;
    block_to_array(current, result_block);
    return result_block;
}

int main()
{
    std::freopen(nullptr, "rb", stdin);
    std::freopen(nullptr, "wb", stdout);

    if (std::ferror(stdin))
    {
        std::cerr << std::strerror(errno) << std::endl;
        return EXIT_FAILURE;
    }
    std::size_t len;
    arrayblock input_block;
    while ((len = std::fread(input_block.data(), sizeof(input_block[0]), input_block.size(), stdin)) > 0)
    {
        if (std::ferror(stdin) && !std::feof(stdin))
        {
            std::cerr << std::strerror(errno) << std::endl;
            return EXIT_FAILURE;
        }

        for (size_t pad = len; pad < input_block.size(); pad++)
        {
            input_block[pad] = (blocksize - len);
        }

        arrayblock result_block = encrypt_array(input_block);

        if (input_block.size() != std::fwrite(result_block.data(), sizeof(input_block[0]), input_block.size(), stdout))
        {
            return EXIT_FAILURE;
        }
    }

    return 0;
}