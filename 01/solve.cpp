#include <iostream>
#include <map>
#include <fstream>
#include <string>

int main()
{  
    std::ifstream infile("input.txt");
    std::map<int, int> m;
    int a, b;
    while (infile >> a) {
        b = 2020-a;
        if (m.find(b) != m.end()) {
            std::cout << "Found: a[" << a << "] * b[" << b << "] = " << a * b << std::endl;
        } else {
            m[a] = 1;
        }
    }
}
