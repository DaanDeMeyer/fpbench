from typing import Tuple

import click
import subprocess
import contextlib
from pathlib import Path

from benchmarks.tee import tee
from benchmarks.common import BenchmarkResult

POSTGRESQL_VERSION = 1
DEFAULT_SCALE = 1
DEFAULT_CLIENTS = 1
DEFAULT_TIME = 10


class Pgbench:
    def __init__(self, scale: int = DEFAULT_SCALE, clients: int = DEFAULT_CLIENTS, time: int = DEFAULT_TIME) -> None:
        self.scale = scale
        self.clients = clients
        self.time = time

    @staticmethod
    def name() -> str:
        return "pgbench"

    def id(self) -> str:
        return f"{self.name()}-v{POSTGRESQL_VERSION}-s{self.scale}-c{self.clients}-T{self.time}"

    def setup(self, stack: contextlib.ExitStack):
        stack.callback(self.teardown)

        datadir = Path("/var/lib/pgsql/data")
        if not datadir.exists() or not any(datadir.iterdir()):
            subprocess.run(["postgresql-setup", "--initdb"], check=True)

        subprocess.run(["systemctl", "start", "postgresql"], check=True)
        subprocess.run(["createdb", "pgbench"], user="postgres", check=True)

        subprocess.run(
            ["pgbench", "-i", "-s", str(self.scale), "-n", "pgbench"],
            user="postgres",
            check=True,
        )

    def teardown(self):
        subprocess.run(["dropdb", "--if-exists", "pgbench"], user="postgres")
        subprocess.run(["systemctl", "stop", "postgresql"])

    def run(self) -> Tuple[BenchmarkResult, ...]:
        subprocess.run(["systemctl", "restart", "postgresql"], check=True)

        p = tee(
            [
                "pgbench",
                "-c",
                str(self.clients),
                "-T",
                str(self.time),
                "-r",
                "pgbench",
            ],
            user="postgres"
        )

        for line in reversed(p.stdout.splitlines()):
            line = line.strip()
            if line.startswith("tps"):
                columns = line.split()
                break
        else:
            assert False

        tps = round(float(columns[2]), 2)

        for line in reversed(p.stdout.splitlines()):
            line = line.strip()
            if line.startswith("latency average"):
                columns = line.split()
                break
        else:
            assert False

        la = round(float(columns[3]), 2)

        return (
            BenchmarkResult(
                benchmark=self.id(),
                result="Transactions per second",
                value=tps,
            ),
            BenchmarkResult(
                benchmark=self.id(),
                result="Average Latency (in ms)",
                value=la,
            ),
        )


@click.command()
@click.option("--scale", "-s", default=DEFAULT_SCALE)
@click.option("--clients", "-c", default=DEFAULT_CLIENTS)
@click.option("--time", "-T", default=DEFAULT_TIME)
def run_pgbench(scale: int, clients: int, time: int):
    return Pgbench(scale, clients, time)
