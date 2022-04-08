#include<algorithm>
#include<limits>
#include <x86intrin.h>

#if defined(__clang__)
typedef float float8_t __attribute__ ((ext_vector_type (8)));
#else
typedef float float8_t __attribute__ ((vector_size (8 * sizeof(float))));
#endif

static inline float8_t swap4(float8_t x) { return _mm256_permute2f128_ps(x, x, 0b00000001); }
static inline float8_t swap2(float8_t x) { return _mm256_permute_ps(x, 0b01001110); }
static inline float8_t swap1(float8_t x) { return _mm256_permute_ps(x, 0b10110001); }

static float8_t* float8_alloc(std::size_t n) {
    void* tmp = 0;
    if (posix_memalign(&tmp, sizeof(float8_t), sizeof(float8_t) * n)) {
        throw std::bad_alloc();
    }
    return (float8_t*)tmp;
}

constexpr float infty = std::numeric_limits<float>::infinity();

constexpr float8_t f8infty {
    infty, infty, infty, infty,
    infty, infty, infty, infty
};

static inline float hmin8(float8_t vv) {
    float v = infty;
    for (int i = 0; i < 8; ++i) {
        v = std::min(vv[i], v);
    }
    return v;
}

static inline float8_t min8(float8_t x, float8_t y) {
    return x < y ? x : y;
}

void step(float* r, const float* d_, int n) {
    // vectors per input column
    int na = (n + 8 - 1) / 8;

    // input data, padded, converted to vectors
    float8_t* vd = float8_alloc(na*n);
    // input data, transposed, padded, converted to vectors
    float8_t* vt = float8_alloc(na*n);

    #pragma omp parallel for
    for (int ja = 0; ja < na; ++ja) {
        for (int i = 0; i < n; ++i) {
            for (int jb = 0; jb < 8; ++jb) {
                int j = ja * 8 + jb;
                vd[n*ja + i][jb] = j < n ? d_[n*j + i] : infty;
                vt[n*ja + i][jb] = j < n ? d_[n*i + j] : infty;
            }
        }
    }

    #pragma omp parallel for
    for (int ia = 0; ia < na; ++ia) {
        for (int ja = 0; ja < na; ++ja) {
            float8_t vv000 = f8infty;
            float8_t vv001 = f8infty;
            float8_t vv010 = f8infty;
            float8_t vv011 = f8infty;
            float8_t vv100 = f8infty;
            float8_t vv101 = f8infty;
            float8_t vv110 = f8infty;
            float8_t vv111 = f8infty;
            for (int k = 0; k < n; ++k) {
                constexpr int PF = 20;
                __builtin_prefetch(&vd[n*ia + k + PF]);
                __builtin_prefetch(&vt[n*ja + k + PF]);
                float8_t a000 = vd[n*ia + k];
                float8_t b000 = vt[n*ja + k];
                float8_t a100 = swap4(a000);
                float8_t a010 = swap2(a000);
                float8_t a110 = swap2(a100);
                float8_t b001 = swap1(b000);
                vv000 = min8(vv000, a000 + b000);
                vv001 = min8(vv001, a000 + b001);
                vv010 = min8(vv010, a010 + b000);
                vv011 = min8(vv011, a010 + b001);
                vv100 = min8(vv100, a100 + b000);
                vv101 = min8(vv101, a100 + b001);
                vv110 = min8(vv110, a110 + b000);
                vv111 = min8(vv111, a110 + b001);
            }
            float8_t vv[8] = { vv000, vv001, vv010, vv011, vv100, vv101, vv110, vv111 };
            for (int kb = 1; kb < 8; kb += 2) {
                vv[kb] = swap1(vv[kb]);
            }
            for (int jb = 0; jb < 8; ++jb) {
                for (int ib = 0; ib < 8; ++ib) {
                    int i = ib + ia*8;
                    int j = jb + ja*8;
                    if (j < n && i < n) {
                        r[n*i + j] = vv[ib^jb][jb];
                    }
                }
            }
        }
    }

    std::free(vt);
    std::free(vd);
}