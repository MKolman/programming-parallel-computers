CPP=g++ -g -O3 -march=native -std=c++17

.SECONDARY:

.PHONY: test_all test_all_th test clean img/v0 img/v0_th img/v1 img/v1_th img/v2 img/v2_th img/v3 img/v3_th img/v4 img/v4_th img/v5 img/v5_th

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
	@for n in 2 4 8 16 32 64 128 256 512 1024 2048 4096; do echo ""; echo "N=$$n"; ./$< <<< $$n; done

test_all: test_v0 test_v1 test_v2 test_v3 test_v4 test_v5

test_all_th: test_v0_th test_v1_th test_v2_th test_v3_th test_v4_th test_v5_th

test:
	make test_all
	make test_all_th

data/data%.txt:
	make test > $@ 2>&1

data/data%.csv: data/data%.txt
	python process.py < $< > $@

img/v%_progress.png: data/data4.csv plot.py
	python plot.py $< --out "$@" --match "v$*" --type progress

img/v%_per_loop.png: data/data4.csv plot.py
	python plot.py $< --out "$@" --match "v$*" --type per_loop

img/v%_bar.png: data/data4.csv plot.py
	python plot.py $< --out "$@" --match "v$*" --type bar

img/v0: img/v0_progress.png img/v0_per_loop.png
	@echo $@
img/v0_th: img/v0.*_progress.png img/v0.*_per_loop.png img/v0.*_bar.png
	@echo $@
img/v1: img/v[01]_progress.png img/v[01]_per_loop.png img/v[01]_bar.png
	@echo $@
img/v1_th: img/v[01].*_progress.png img/v[01].*_per_loop.png img/v[01].*_bar.png
	@echo $@
img/v2: img/v[012]_progress.png img/v[012]_per_loop.png img/v[012]_bar.png
	@echo $@
img/v2_th: img/v[012].*_progress.png img/v[012].*_per_loop.png img/v[012].*_bar.png
	@echo $@
img/v3: img/v[0123]_progress.png img/v[0123]_per_loop.png img/v[0123]_bar.png
	@echo $@
img/v3_th: img/v[0123].*_progress.png img/v[0123].*_per_loop.png img/v[0123].*_bar.png
	@echo $@
img/v4: img/v[01234]_progress.png img/v[01234]_per_loop.png img/v[01234]_bar.png
	@echo $@
img/v4_th: img/v[01234].*_progress.png img/v[01234].*_per_loop.png img/v[01234].*_bar.png
	@echo $@
img/v5: img/v[012345]_progress.png img/v[012345]_per_loop.png img/v[012345]_bar.png
	@echo $@
img/v5_th: img/v[012345].*_progress.png img/v[012345].*_per_loop.png img/v[012345].*_bar.png
	@echo $@
imgs: img/v0 img/v0_th img/v1 img/v1_th img/v2 img/v2_th img/v3 img/v3_th img/v4 img/v4_th img/v5 img/v5_th
	@echo $@
	@echo "Done"

clean:
	rm bin/* img/*
