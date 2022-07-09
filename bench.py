#!/usr/bin/env python3

from typing import Optional, Any, Iterable
from pathlib import Path
import json

import click
import pandas as pd


from benchmarks.common import Benchmark, BenchmarkResult, IBenchmark, flatten
from benchmarks.zstd import Zstd, run_zstd
from benchmarks.openssl import OpenSSL, run_openssl


@click.group()
def bench():
    return


@bench.group()
@click.option("-t", "--times-to-run", default=1)
@click.option("--omit-fp/--no-omit-fp")
@click.option("--save", type=click.Path())
def run(*args: Any, **kwargs: Any):
    pass


@run.result_callback()
def runcb(
    result: IBenchmark,
    times_to_run: int,
    omit_fp: bool,
    save: Optional[str],
):
    metadata = {"fp": "omit" if omit_fp else "keep"}

    data = Benchmark(times_to_run=times_to_run, metadata=metadata, impl=result).run()

    if save:
        file = Path(save)
        d = json.loads(file.read_text()) if file.exists() else tuple()
        j = json.dumps((*d, *data), indent=4)
        Path(save).write_text(f"{j}\n")


run.add_command(name=Zstd.name(), cmd=run_zstd)
run.add_command(name=OpenSSL.name(), cmd=run_openssl)


def allexcept(all: Iterable[str], exc: Iterable[str]) -> Iterable[str]:
    exc = set(exc)
    return (item for item in all if item not in exc)


@bench.command()
@click.argument("sources", nargs=-1, type=click.Path(exists=True))
def analyze(sources: Iterable[str]):
    decoded: Iterable[BenchmarkResult] = flatten(
        json.loads(Path(src).read_text()) for src in sources
    )

    df = pd.DataFrame(decoded)

    df = df.groupby(["benchmark", "result", "fp"]).agg(
        avg=("value", "mean"),
        count=("value", "size"),
    )

    def filter(x):
        benchmark = df.index.get_level_values("benchmark").unique()[0]
        result = df.index.get_level_values("result").unique()[0]
        unique = df.index.get_level_values("fp").unique()
        if "omit" not in unique:
            print(
                f'Missing -fomit-frame-pointer results for benchmark "{benchmark}" result "{result}", ignoring'
            )
        if "keep" not in unique:
            print(
                f'Missing -fno-omit-frame-pointer results for benchmark "{benchmark}" result "{result}", ignoring'
            )
        return len(x) == 2

    df = df.groupby(["benchmark", "result"]).filter(filter)

    def compare(x):
        keep = x.xs("keep", level="fp").iat[0]
        omit = x.xs("omit", level="fp").iat[0]
        return (round(omit, 2), round(keep, 2))

    def diff(x):
        keep = x.xs("keep", level="fp").iat[0]
        omit = x.xs("omit", level="fp").iat[0]
        return round((1 - omit / keep) * 100, 1)

    def count(x):
        keep = x.xs("keep", level="fp").iat[0]
        omit = x.xs("omit", level="fp").iat[0]
        return (omit, keep)

    df = df.groupby(["benchmark", "result"]).agg(
        diff=("avg", diff), compare=("avg", compare), count=("count", count)
    ).reset_index()

    print(
        df.to_string(
            index=False,
            header=[
                "Benchmark",
                "Result",
                "-fno-omit-frame-pointer",
                "Comparison (omit / no-omit)",
                "Num Tests (omit / no-omit)",
            ],
            formatters={
                "diff": lambda x: f"{x}% {'faster' if x >= 0 else 'slower'}",
                "compare": lambda x: f"{x[0]} / {x[1]}",
                "count": lambda x: f"{x[0]} / {x[1]}",
            },
        )
    )


if __name__ == "__main__":
    bench()
