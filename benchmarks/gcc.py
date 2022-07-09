from typing import Tuple

import click
import contextlib
import multiprocessing
from datetime import datetime
import time

from benchmarks.tee import tee
from benchmarks.common import BenchmarkResult, download, untar

GCC_VERSION = 1


class Gcc:
    def __init__(self) -> None:
        pass

    @staticmethod
    def name() -> str:
        return "gcc"

    def id(self) -> str:
        return f"{self.name()}-v{GCC_VERSION}"

    def setup(self, stack: contextlib.ExitStack):
        tarfile = download(
            "https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.0.5.tar.xz",
            "61332ef22b53c50c10faabfb965896a7d1ad4f3381f0f89643c820f28a60418e",
        )

        self.dir = untar(tarfile, strip_components=1)

    def run(self) -> Tuple[BenchmarkResult, ...]:
        tee(["make", "mrproper"], cwd=self.dir)

        start = time.time()
        tee(["make", "defconfig"], cwd=self.dir)
        tee(["scripts/config", "--set-val", "CONFIG_WERROR", "n"], cwd=self.dir)
        tee(["make", "-j", str(multiprocessing.cpu_count())], cwd=self.dir)
        end = time.time()

        return (
            BenchmarkResult(
                benchmark=self.id(),
                result="Duration (s)",
                value=end - start,
            ),
        )


@click.command()
def run_gcc():
    return Gcc()
