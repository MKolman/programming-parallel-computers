#include <chrono>
#include <iostream>
#include <vector>

void step(float*, const float*, int);

int main() {
    int n;
    std::cin >> n;
    std::vector<float> d(n*n);
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            d[i*n+j] = std::abs(i-j);
            d[i*n+j] *= d[i*n+j];
        }
    }
    std::vector<float> r(n*n);
    auto start = std::chrono::high_resolution_clock::now();
    step(&r[0], &d[0], n);
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> dur = end - start;
    std::cout << "real " << dur.count() << "\n";


}
