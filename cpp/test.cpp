#include<iostream>
#include<vector>

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
    step(&r[0], &d[0], n);
}
