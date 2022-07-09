#!/usr/bin/env python3

from typing import Iterable
from pathlib import Path
import json

import click

from benchmarks.common import BenchmarkResult

@click.command()
@click.option("--key", required=True)
@click.argument("sources", nargs=-1, type=click.Path(exists=True))
def remove(key: str, sources: Iterable[str]):
    for src in sources:
        data: Iterable[BenchmarkResult] = json.loads(Path(src).read_text())
        data = tuple(d for d in data if d["benchmark"] != key)
        Path(src).write_text(json.dumps(data, indent=4))


if __name__ == "__main__":
    remove()
