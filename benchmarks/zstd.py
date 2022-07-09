from typing import Tuple

import click

from benchmarks.tee import tee
from benchmarks.common import BenchmarkResult

ZSTD_VERSION = 1
DEFAULT_COMPRESSION = 3
DEFAULT_MIN_EVAL_SEC = 1


class Zstd:
    def __init__(
        self,
        level: int = DEFAULT_COMPRESSION,
        min_eval_sec: int = DEFAULT_MIN_EVAL_SEC,
    ) -> None:
        self.level = level
        self.min_eval_sec = min_eval_sec

    @staticmethod
    def name() -> str:
        return "zstd"

    def id(self) -> str:
        return f"{self.name()}-v{ZSTD_VERSION}-b{self.level}-i{self.min_eval_sec}"

    def setup(self, stack):
        pass

    def run(self) -> Tuple[BenchmarkResult, ...]:
        p = tee(["zstd", f"-b{self.level}", f"-i{self.min_eval_sec}"])

        for line in reversed(p.stdout.split("\n")):
            line = line.removesuffix("\r 3#")
            line = line.replace(",", " ")
            columns = line.split()
            if len(columns) >= 4:
                break
        else:
            assert False

        compression = round(float(columns[-4]), 2)
        decompression = round(float(columns[-2]), 2)

        return (
            BenchmarkResult(
                benchmark=self.id(),
                result="Compression Speed (MB/s)",
                value=compression,
            ),
            BenchmarkResult(
                benchmark=self.id(),
                result="Decompression Speed (MB/s)",
                value=decompression,
            ),
        )


@click.command()
@click.option(
    "--compression",
    "-b",
    "level",
    help="Compression Level",
    default=DEFAULT_COMPRESSION,
)
@click.option(
    "--min-eval-sec",
    "-i",
    help="Minimum Evaluation Time (in seconds)",
    default=DEFAULT_MIN_EVAL_SEC,
)
def run_zstd(level: int, min_eval_sec: int):
    return Zstd(level, min_eval_sec)
