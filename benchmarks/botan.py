from typing import Tuple, Sequence
import json

import click

from benchmarks.tee import tee
from benchmarks.common import BenchmarkResult

BOTAN_VERSION = 1
DEFAULT_ALGORITHMS = ("AES-256", "Blowfish", "CAST-256", "KASUMI", "Twofish", "ChaCha20Poly1305")
DEFAULT_SECONDS = 1


class Botan:
    def __init__(
        self,
        seconds: int = DEFAULT_SECONDS,
        algorithms: Sequence[str] = DEFAULT_ALGORITHMS,
    ) -> None:
        self.seconds = seconds
        self.algorithms = algorithms

    @staticmethod
    def name() -> str:
        return "botan"

    def id(self) -> str:
        return f"botan-v{BOTAN_VERSION}-s{self.seconds}"

    def setup(self, stack):
        pass

    def run(self) -> Tuple[BenchmarkResult, ...]:
        p = tee(
            [
                "botan",
                "speed",
                f"--msec={self.seconds * 1000}",
                "--format=json",
                *self.algorithms,
            ]
        )

        results = []

        for result in json.loads(p.stdout):
            if "bps" not in result:
                continue

            results.append(
                BenchmarkResult(
                    benchmark=self.id(),
                    result=f"{result['algo']} (MB/second)",
                    value=result["bps"] / 1000000,
                )
            )

        assert len(results) > 0

        return tuple(results)


@click.command()
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
def run_botan(seconds: int, algorithms: Sequence[str]):
    return Botan(seconds, algorithms)
