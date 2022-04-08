import argparse
import re
import sys
from typing import Iterable

from matplotlib import pyplot as plt


parser = argparse.ArgumentParser(description="Plot graphs")
parser.add_argument(
    "infile",
    type=argparse.FileType("r"),
    default="cpp/data/data4.csv",
)
parser.add_argument("--out", required=True)
parser.add_argument("--match", default=".*")
parser.add_argument(
    "--type",
    choices=["bar", "progress", "per_loop"],
    default="progress",
)


def read(stream: Iterable[str]) -> list[tuple[str | float]]:
    return [tuple(map(try_convert_time, line.strip().split(", "))) for line in stream]


def try_convert_time(maybe_time: str) -> str | float:
    try:
        return float(maybe_time)
    except ValueError:
        return maybe_time


def convert_time(time: str) -> float:
    """Converts time format `5m35,892s` into seconds."""
    m, s = time.replace(",", ".").strip("s").split("m")
    return int(m) * 60 + float(s)


def plot_progression(
    data: list[tuple[str | float]],
    per_inner_loop=True,
):
    xs = list(map(int, data[0][1:]))
    for line in data[1:]:
        if per_inner_loop:
            ts = [y / 1000 / x**3 for x, y in zip(xs, line[1:])]
            plt.plot(xs, ts, "o-", label=line[0])
        else:
            ts = [t / 1000 for t in line[1:]]
            plt.plot(xs, [t / 1000 for t in line[1:]], "o-", label=line[0])
        if len(data) <= 3:
            for x, t in zip(xs[::2], ts[::2]):
                v = t
                if t > 10:
                    v = f"{t:.0f}"
                elif t > 0.1:
                    v = f"{t:.2g}"
                else:
                    v = f"{t:.0e}"
                    v = v.replace("e-02", "0m").replace("e-03", "m")
                    v = (
                        v.replace("e-04", "00u")
                        .replace("e-05", "0u")
                        .replace("e-06", "u")
                    )
                    v = (
                        v.replace("e-07", "00n")
                        .replace("e-08", "0n")
                        .replace("e-09", "n")
                    )
                    v = (
                        v.replace("e-10", "00p")
                        .replace("e-11", "0p")
                        .replace("e-12", "p")
                    )
                plt.annotate(v + "s", (x, t), size=10)
    plt.legend()
    ax = plt.gca()
    ax.set_yscale("log")
    ax.set_xscale("log", base=2)
    plt.grid(linestyle=":")
    # plt.xlabel("Graph input memory size [4B$\cdot n^2$]")
    plt.xlabel("Graph size [n]")
    if per_inner_loop:
        plt.ylabel("Time for inner loop")
        plt.yticks(
            [1e-10, 1e-9, 1e-8],
            ["100ps", "1ns", "10ns"],
        )
    else:
        plt.ylabel("Time to complete")
        plt.yticks(
            [1e-5, 0.0001, 0.001, 0.01, 0.1, 1, 10, 60, 600],
            ["10us", "100us", "1ms", "10ms", "100ms", "1s", "10s", "1m", "10min"],
        )
    # plt.xticks(xs, [format_bytes(x) for x in xs], size="small")
    plt.xticks(xs, xs)


def format_bytes(n):
    b = 4 * n**2
    prefix = ["", "k", "M", "G"]
    for p in prefix:
        if b < 1024:
            return f"{b}{p}B"
        b = round(b / 1024)


def trim_row(row, n=5):
    return [row[0]] + list(row[n:])


def select(data, row_match, col_skip):
    match = re.compile(row_match)
    result = [trim_row(data[0], col_skip)]
    for row in data[1:]:
        if match.fullmatch(row[0]):
            result.append(trim_row(row, col_skip))
    return result


def plot_bar(data):
    xs = []
    ys = []
    xs_th = []
    ys_th = []
    should_split = len(data) > 3
    for row in data[1:]:
        t = row[-1] / 1000
        if should_split and row[0].endswith("_th"):
            xs_th.append(row[0][:-3])
            ys_th.append(t)
        else:
            xs.append(row[0])
            ys.append(t)
    if xs:
        bar = plt.bar(xs, ys, label="Single-threaded")
    if xs_th:
        bar_th = plt.bar(xs_th, ys_th, label="Multi-threaded")
        plt.bar_label(bar_th, fmt="%.1fs", color="white" if xs else "black")
    if xs:
        plt.bar_label(bar, fmt="%.1fs")
    if xs and xs_th:
        plt.legend()
    if should_split:
        plt.yscale("log")
        plt.yticks(
            [1, 10, 60, 600],
            ["1s", "10s", "1m", "10min"],
        )
    plt.ylabel(f"Time to complete N={int(data[0][-1])} case.")


def main():
    args = parser.parse_args()
    data = read(args.infile)
    data = select(data, args.match, 4)
    if args.type == "bar":
        plot_bar(data)
    else:
        plot_progression(
            data,
            per_inner_loop=args.type == "per_loop",
        )
    plt.gcf().set_size_inches((4.5, 2.5))
    plt.tight_layout()
    plt.savefig(args.out, dpi=200)


if __name__ == "__main__":
    main()
