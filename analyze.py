#!/usr/bin/env python3
from typing import Iterable
import json
from pathlib import Path

import pandas as pd
import numpy as np
import click

from benchmarks.common import flatten, BenchmarkResult


@click.command()
@click.argument("sources", nargs=-1, type=click.Path(exists=True))
def analyze(sources: Iterable[str]):
    decoded: Iterable[BenchmarkResult] = flatten(
        json.loads(Path(src).read_text()) for src in sources
    )

    df = pd.DataFrame(decoded)

    df = df.groupby(["benchmark", "result", "fp"]).agg(
        avg=("value", np.average),
        stddev=("value", lambda x: np.std(x, ddof=0) * 100 / np.average(x)),
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

    def diff(x):
        keep = x.xs("keep", level="fp").iat[0]
        omit = x.xs("omit", level="fp").iat[0]
        return round((1 - omit / keep) * 100, 1)

    def compare(x):
        keep = x.xs("keep", level="fp").iat[0]
        omit = x.xs("omit", level="fp").iat[0]
        return (round(omit, 4), round(keep, 4))

    def count(x):
        keep = x.xs("keep", level="fp").iat[0]
        omit = x.xs("omit", level="fp").iat[0]
        return (omit, keep)

    df = (
        df.groupby(["benchmark", "result"])
        .agg(
            compare=("avg", compare),
            diff=("avg", diff),
            stddev=("stddev", compare),
            count=("count", count),
        )
        .reset_index()
    )

    print(
        df.to_string(
            index=False,
            header=[
                "Benchmark",
                "Result",
                "Mean (omit / no-omit)",
                "Mean Difference",
                "Std Dev (omit / no-omit)",
                "Num Tests (omit / no-omit)",
            ],
            formatters={
                "diff": lambda x: f"{abs(x)}%",
                "stddev": lambda x: f"{x[0]}% / {x[1]}%",
                "compare": lambda x: f"{x[0]} / {x[1]}",
                "count": lambda x: f"{x[0]} / {x[1]}",
            },
        )
    )


if __name__ == "__main__":
    analyze()
