from typing import Tuple, Mapping, Any

import click

from benchmarks.tee import tee
from benchmarks.common import BenchmarkResult

OPENSSL_VERSION = 1


class OpenSSL:
    def __init__(self, algorithm: str, num_bytes: int, seconds: int) -> None:
        self.algorithm = algorithm
        self.num_bytes = num_bytes
        self.seconds = seconds

    @staticmethod
    def name() -> str:
        return "openssl"

    def id(self) -> str:
        return f"openssl-v{OPENSSL_VERSION}-{self.algorithm}-b{self.num_bytes}-s{self.seconds}"

    def __enter__(self):
        pass

    def __exit__(self, *args):
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
                self.algorithm,
            ]
        )

        for line in reversed(p.stdout.split("\n")):
            line = line.removesuffix("\r 3#")
            if line.startswith(self.algorithm):
                columns = line.split()
                break
        else:
            assert False

        speed = round(float(columns[-1].rstrip("k")), 2)

        return (
            BenchmarkResult(
                benchmark=self.id(),
                result="Speed (kB/s)",
                value=speed,
            ),
        )


@click.command()
@click.option(
    "--algorithm",
    "-a",
    help="Algorithm to benchmark",
    default="sha256",
)
@click.option(
    "--bytes",
    "-b",
    "num_bytes",
    help="Set buffer size",
    default=16384,
)
@click.option(
    "--seconds",
    "-s",
    help="Minimum Evaluation Time (in seconds)",
    default=1,
)
def run_openssl(algorithm: str, num_bytes: int, seconds: int):
    return OpenSSL(algorithm, num_bytes, seconds)
