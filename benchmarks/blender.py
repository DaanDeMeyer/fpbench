from typing import Tuple

import click
import contextlib
from datetime import datetime

from benchmarks.tee import tee
from benchmarks.common import BenchmarkResult, download, unzip

BLENDER_VERSION = 1


class Blender:
    def __init__(self) -> None:
        pass

    @staticmethod
    def name() -> str:
        return "blender"

    def id(self) -> str:
        return f"{self.name()}-v{BLENDER_VERSION}"

    def setup(self, stack: contextlib.ExitStack):
        zipfile = download(
            "http://download.blender.org/demo/test/cycles_benchmark_20160228.zip",
            "026e7499a7bd9e0d41fe4d43e611a145a62d8d5df4fe347a6a08c6f0e98cf0c6",
        )

        self.dir = unzip(zipfile)

    def run(self) -> Tuple[BenchmarkResult, ...]:
        p = tee(
            [
                "blender",
                "-b",
                str(self.dir / "benchmark/bmw27/bmw27_cpu.blend"),
                "-f",
                "1",
                "-F",
                "JPEG",
                "-o",
                "blender.jpeg",
                "--",
                "--cycles-device",
                "CPU",
            ]
        )

        for line in reversed(p.stdout.split("\n")):
            line = line.strip()
            if line.startswith("Time: "):
                columns = line.split()
                break
        else:
            assert False

        duration = datetime.strptime(columns[1], "%M:%S.%f")

        return (
            BenchmarkResult(
                benchmark=self.id(),
                result="Duration (s)",
                value=(duration.minute * 60 + duration.second),
            ),
        )


@click.command()
def run_blender():
    return Blender()
