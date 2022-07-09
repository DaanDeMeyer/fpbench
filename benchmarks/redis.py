import subprocess
from typing import Tuple, Sequence
import contextlib
import io
import csv

import click

from benchmarks.tee import tee
from benchmarks.common import BenchmarkResult

REDIS_VERSION = 1
DEFAULT_NUM_REQUESTS = 10000000
DEFAULT_NUM_PIPELINE = 32
DEFAULT_NUM_CLIENTS = 50
DEFAULT_OPERATIONS = ("GET",)


class Redis:
    def __init__(
        self,
        num_requests: int = DEFAULT_NUM_REQUESTS,
        num_pipeline: int = DEFAULT_NUM_PIPELINE,
        num_clients: int = DEFAULT_NUM_CLIENTS,
        operations: Sequence[str] = DEFAULT_OPERATIONS,
    ) -> None:
        self.num_requests = num_requests
        self.num_pipeline = num_pipeline
        self.num_clients = num_clients
        self.operations = operations

    @staticmethod
    def name() -> str:
        return "redis"

    def id(self) -> str:
        return f"{self.name()}-v{REDIS_VERSION}-n{self.num_requests}-P{self.num_pipeline}-c{self.num_clients}"

    def setup(self, stack: contextlib.ExitStack):
        stack.callback(self.teardown)
        subprocess.run(["systemctl", "start", "redis"], check=True)

    def teardown(self):
        subprocess.run(["systemctl", "stop", "redis"])

    def run(self) -> Tuple[BenchmarkResult, ...]:
        p = tee(
            [
                "redis-benchmark",
                "-n",
                str(self.num_requests),
                "-P",
                str(self.num_pipeline),
                "-c",
                str(self.num_clients),
                "-t",
                ",".join(self.operations),
                "--csv",
            ],
            check=True,
        )

        reader = csv.reader(io.StringIO(p.stdout), delimiter=",")
        next(reader)

        return tuple(
            BenchmarkResult(
                benchmark=self.id(),
                result=f"{row[0]} (requests per second)",
                value=int(row[1]),
            )
            for row in reader
        )


@click.command()
@click.option("--num-requests", "-n", default=DEFAULT_NUM_REQUESTS)
@click.option("--num-pipeline", "-P", default=DEFAULT_NUM_PIPELINE)
@click.option("--num-clients", "-c", default=DEFAULT_NUM_CLIENTS)
@click.option("--operation", "-t", "operations", default=DEFAULT_OPERATIONS, multiple=True)
def run_redis(
    num_requests: int,
    num_pipeline: int,
    num_clients: int,
    operations: Sequence[str],
):
    return Redis(num_requests, num_pipeline, num_clients, operations)
