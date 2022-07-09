#!/usr/bin/env python3

from typing import Optional, Any
from pathlib import Path
import json

import click

from benchmarks.common import Benchmark, IBenchmark
from benchmarks.zstd import Zstd, run_zstd
from benchmarks.openssl import OpenSSL, run_openssl
from benchmarks.blender import Blender, run_blender
from benchmarks.pyperformance import Pyperformance, run_pyperformance
from benchmarks.pgbench import Pgbench, run_pgbench
from benchmarks.redis import Redis, run_redis
from benchmarks.botan import Botan, run_botan
from benchmarks.gcc import Gcc, run_gcc


@click.group(invoke_without_command=True)
@click.option("-t", "--times-to-run", default=1)
@click.option("--omit-fp/--no-omit-fp", required=True, default=None)
@click.option("--save", type=click.Path())
def bench(*args: Any, **kwargs: Any):
    return


@bench.result_callback()
def benchcb(
    impl: Optional[IBenchmark],
    times_to_run: int,
    omit_fp: bool,
    save: Optional[str],
):
    metadata = {"fp": "omit" if omit_fp else "keep"}

    if impl:
        benchmarks = (
            Benchmark(times_to_run=times_to_run, metadata=metadata, impl=impl),
        )
    else:
        benchmarks = (
            Benchmark(
                times_to_run=1,
                metadata=metadata,
                impl=Blender(),
            ),
            Benchmark(
                times_to_run=1,
                metadata=metadata,
                impl=OpenSSL(algorithms=(), seconds=10),
            ),
            Benchmark(
                times_to_run=3,
                metadata=metadata,
                impl=Pgbench(scale=100, clients=20, time=20),
            ),
            Benchmark(
                times_to_run=1,
                metadata=metadata,
                impl=Pyperformance(rigorous=True),
            ),
            Benchmark(
                times_to_run=3,
                metadata=metadata,
                impl=Redis(operations=("GET", "SET", "SADD", "LPUSH", "LPOP")),
            ),
            Benchmark(
                times_to_run=10,
                metadata=metadata,
                impl=Zstd(min_eval_sec=10),
            ),
            Benchmark(
                times_to_run=1,
                metadata=metadata,
                impl=Botan(),
            ),
            Benchmark(
                times_to_run=1,
                metadata=metadata,
                impl=Gcc(),
            ),
        )

    for bench in benchmarks:
        data = bench.run()

        if save:
            file = Path(save)
            d = json.loads(file.read_text()) if file.exists() else tuple()
            j = json.dumps((*d, *data), indent=4)
            Path(save).write_text(f"{j}\n")


bench.add_command(name=Zstd.name(), cmd=run_zstd)
bench.add_command(name=OpenSSL.name(), cmd=run_openssl)
bench.add_command(name=Blender.name(), cmd=run_blender)
bench.add_command(name=Pyperformance.name(), cmd=run_pyperformance)
bench.add_command(name=Pgbench.name(), cmd=run_pgbench)
bench.add_command(name=Redis.name(), cmd=run_redis)
bench.add_command(name=Botan.name(), cmd=run_botan)
bench.add_command(name=Gcc.name(), cmd=run_gcc)


if __name__ == "__main__":
    bench()
