import sys
from collections import defaultdict as dd

V_PREFIX = "=== Running bin/test_"
N_PREFIX = "N="
T_PREFIXES = ["real", "user", "sys"]


def parse(stream):
    v = "v0"
    N = 1
    data = dd(lambda: dd(dict))
    for line in stream:
        if line.startswith(V_PREFIX):
            v = line[len(V_PREFIX) :].strip(" =\n")
        elif line.startswith(N_PREFIX):
            N = int(line[len(N_PREFIX) :].strip(" \n"))
        elif any(line.startswith(t) for t in T_PREFIXES):
            name, time = line.split()
            data[v][N][name] = time
    return data


def dump(data):
    header = True
    for key, d in sorted(data.items()):
        if header:
            header = False
            print("Name", *[n for n in sorted(d)], sep=", ")

        print(key, *[times["real"] for _, times in sorted(d.items())], sep=", ")


def main():
    data = parse(sys.stdin)
    dump(data)


main()
