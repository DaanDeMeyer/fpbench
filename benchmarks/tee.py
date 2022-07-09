import asyncio
import subprocess
import sys
import io

from typing import Iterable, TextIO, Any


def tee(
    cmd: Iterable[str],
    check: bool = True,
    **kwargs: Any,
) -> subprocess.CompletedProcess[str]:
    out = io.StringIO()
    err = io.StringIO()

    async def read(
        stream: asyncio.StreamReader,
        sinks: Iterable[TextIO],
    ) -> None:
        while True:
            line = await stream.readline()
            if line:
                decoded = line.decode()
                for sink in sinks:
                    sink.write(decoded)
                    sink.flush()
            else:
                break

    async def loading(proc: asyncio.subprocess.Process) -> None:
        if not sys.stderr.isatty():
            return

        ticks = 0
        while True:
            try:
                await asyncio.wait_for(asyncio.shield(proc.wait()), 1)
            except asyncio.TimeoutError:
                print("." * ticks, end="\r", file=sys.stderr)
                ticks += 1
                if ticks == 20:
                    print(" " * ticks, end="\r", file=sys.stderr)
                    ticks = 0
            else:
                break

    async def run() -> subprocess.CompletedProcess[str]:
        p = await asyncio.create_subprocess_exec(
            "stdbuf",
            "-oL",
            "-eL",
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            **kwargs,
        )

        assert p.stdout
        assert p.stderr

        await asyncio.wait(
            (
                asyncio.create_task(read(p.stdout, (out, sys.stdout))),
                asyncio.create_task(read(p.stderr, (err, sys.stderr))),
                asyncio.create_task(loading(p)),
            )
        )

        assert p.returncode is not None

        if check and p.returncode > 0:
            raise subprocess.CalledProcessError(
                p.returncode,
                tuple(cmd),
                out.getvalue(),
                err.getvalue(),
            )

        return subprocess.CompletedProcess(
            tuple(cmd),
            p.returncode,
            out.getvalue(),
            err.getvalue(),
        )

    return asyncio.run(run())
