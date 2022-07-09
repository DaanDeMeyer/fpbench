from typing import Tuple, Sequence

import click

from benchmarks.tee import tee
from benchmarks.common import BenchmarkResult

OPENSSL_VERSION = 1
DEFAULT_ALGORITHMS = ("sha256",)
DEFAULT_NUM_BYTES = 16384
DEFAULT_SECONDS = 1


class OpenSSL:
    def __init__(
        self,
        num_bytes: int = DEFAULT_NUM_BYTES,
        seconds: int = DEFAULT_SECONDS,
        algorithms: Sequence[str] = DEFAULT_ALGORITHMS,
    ) -> None:
        self.num_bytes = num_bytes
        self.seconds = seconds
        self.algorithms = algorithms

    @staticmethod
    def name() -> str:
        return "openssl"

    def id(self) -> str:
        return f"openssl-v{OPENSSL_VERSION}-b{self.num_bytes}-s{self.seconds}"

    def setup(self, stack):
        pass

    def run(self) -> Tuple[BenchmarkResult, ...]:
        p = tee(
            [
                "openssl",
                "speed",
                "-bytes",
                str(self.num_bytes),
                "-seconds",
                str(self.seconds),
                "-mr",
                *self.algorithms,
            ]
        )

        results = []

        for line in reversed(p.stdout.split("\n")):
            line = line.removesuffix("\r 3#")
            columns = line.split(":")
            if len(columns) > 0 and columns[0] == "+F":
                algorithm = columns[2]
                speed = round(float(columns[3]))
                results.append(
                    BenchmarkResult(
                        benchmark=self.id(),
                        result=f"{algorithm} (MB/second)",
                        value=speed / 1000000,
                    )
                )

        assert len(results) > 0

        return tuple(results)


@click.command()
@click.option(
    "--bytes",
    "-b",
    "num_bytes",
    help="Set buffer size",
    default=DEFAULT_NUM_BYTES,
)
@click.option(
    "--seconds",
    "-s",
    help="Minimum Evaluation Time (in seconds)",
    default=DEFAULT_SECONDS,
)
@click.option(
    "--algorithm",
    "-a",
    "algorithms",
    help="Algorithm to benchmark",
    default=DEFAULT_ALGORITHMS,
    multiple=True,
)
def run_openssl(num_bytes: int, seconds: int, algorithms: Sequence[str]):
    return OpenSSL(num_bytes, seconds, algorithms)
