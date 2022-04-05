CPP=g++ -g -O3 -march=native -std=c++17

bin/v%: v%.cpp
	$(CPP) main.cpp $< -o $@

bin/v%_th: v%.cpp
	$(CPP) -fopenmp main.cpp $< -o $@

bin/test_v%: v%.cpp
	$(CPP) test.cpp $< -o $@

bin/test_v%_th: v%.cpp
	$(CPP) -fopenmp test.cpp $< -o $@

test_v%: bin/test_v%
	@echo "=== Running $< ==="
	@for n in 2 4 8 16 32 64 128 256 512 1024 2048 4096; do echo "\nN=$$n"; time ./$< <<< $$n; done

test_all: test_v0 test_v1 test_v2 test_v3 test_v4 test_v5

test_all_th: test_v0_th test_v1_th test_v2_th test_v3_th test_v4_th test_v5_th

test: test_all test_all_th

clean:
	rm bin/*
