from pathlib import Path
from typing import Tuple
import pyperf

import click

from benchmarks.tee import tee
from benchmarks.common import BenchmarkResult

PYPERFORMANCE_VERSION = 1


class Pyperformance:
    def __init__(self, rigorous: bool = False) -> None:
        self.rigorous = rigorous

    @staticmethod
    def name() -> str:
        return "pyperformance"

    def id(self) -> str:
        return f"{self.name()}-v{PYPERFORMANCE_VERSION}-r{int(self.rigorous)}"

    def setup(self, stack):
        pass

    def run(self) -> Tuple[BenchmarkResult, ...]:
        output = Path("/tmp/pyperformance.json")
        output.unlink(missing_ok=True)
        tee(["pyperformance", "run", "-o", str(output), "-r" if self.rigorous else "-f"])

        suite = pyperf.BenchmarkSuite.load(str(output))
        return tuple(
            BenchmarkResult(
                benchmark=self.id(),
                result=bench.get_name(),
                value=bench.mean(),
            )
            for bench in suite
        )


@click.command()
@click.option("--rigorous", "-r", is_flag=True)
def run_pyperformance(rigorous: bool):
    return Pyperformance()
