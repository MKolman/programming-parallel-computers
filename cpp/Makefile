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
	time ./$<;

clean:
	rm bin/*