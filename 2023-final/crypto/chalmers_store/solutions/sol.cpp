// Find a collision for the first hash. Can be done in sqrt(1e6) time using birtday attack, but we simply brute it
// Then, if our solutions are a and b, realize that a+b, a+a, b+a, a+a+a+b etc will all also collide. Now find collision of these concatenations for 2nd hash. repeat

#include <bits/stdc++.h>
using namespace std;

unsigned long long magic[] = { 4404 ^ 3214, 25954 ^ 3214, 17763 ^ 3124 };


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

unsigned long long powerhash(const std::string& s, int m)
{
    return hashonce(s, magic[m]);
}

string a;
string b;

auto Start = chrono::high_resolution_clock::now();
void resettimer() { Start = chrono::high_resolution_clock::now(); }
int elapsedmillis() { return chrono::duration_cast<chrono::milliseconds>(chrono::high_resolution_clock::now() - Start).count(); }

void collide(int ind)
{
    mt19937 rng(1); // Period of rand can be too short

    uniform_int_distribution<int> dist(0, 1);
  

    int hi = 8;
    resettimer();
    while (true)
    {
        string o;
        string p;

        for (int i = 0; i < hi; i++)
        {
            if (dist(rng)) o += a;
            else o += b;

            if (dist(rng)) p += a;
            else p += b;

        }

        if (o != p && powerhash(o, ind) == powerhash(p, ind))
        {
            a = o;
            b = p;
            break;
        }

        if (elapsedmillis()>1000)
        {
            hi++;
            resettimer();
        }
    }
}

int32_t main()
{
    if (0)
    {
        std::string k, p;
        std::cin >> k >> p;
        std::cout << k.size() << " " << p.size() << "\n";
        for (int i = 0; i < 4; i++)
        {
            std::cout << powerhash(k, i) << " ";
        }
        std::cout << "\n";
        for (int i = 0; i < 4; i++)
        {
            std::cout << powerhash(p, i) << " ";
        }
        return 0;
    }
    

    //string a, b;
    //cin >> a >> b;
    //cout << powerhash(a) << " " << powerhash(b) << "\n";


    unordered_map<int, string> seen;

    cout << "Starting stage 1\n";
    srand(124);
    while (true)
    {
        string s = string(4, 'A');
        for (int i = 0; i < 4; i++) s[i] = rand() % 26 + 'a';
        unsigned long long h = powerhash(s, 0);

        if (seen.find(h) != seen.end())
        {
            if (seen[h] == s) continue;
            a = s;
            b = seen[h];

            break;
        }
        seen[h] = s;
    }

    for (int i = 1; i < 3; i++)
    {
        cout << "Starting stage " << i+1 << "\n";
        collide(i);
        cout << powerhash(a, i) << " " << powerhash(b, i) << "\n";
    }
    
    for (int i = 0; i < 3; i++)
    {
        cout << powerhash(a, i) << " ";
    }
    cout << "\n";
    for (int i = 0; i < 3; i++)
    {
        cout << powerhash(b, i) << " ";
    }
    cout << "\n" << powerhash(a) << " " << powerhash(b) << "\n";


    cout << "\n" << a << "\n\n" << b;

}
