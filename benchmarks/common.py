import contextlib
from typing import Iterable, Tuple, TypeVar, TypedDict, Mapping, Protocol
from pathlib import Path
import urllib.request
import urllib.parse
import os
import subprocess

T = TypeVar("T")


def flatten(xss: Iterable[Iterable[T]]) -> Tuple[T]:
    return tuple(x for xs in xss for x in xs)


class BenchmarkResult(TypedDict):
    benchmark: str
    result: str
    value: float


class IBenchmark(Protocol):
    def setup(self, stack: contextlib.ExitStack):
        ...

    def run(self) -> Tuple[BenchmarkResult]:
        ...


class Benchmark:
    def __init__(
        self,
        times_to_run: int,
        metadata: Mapping[str, str],
        impl: IBenchmark,
    ) -> None:
        self.times_to_run = times_to_run
        self.metadata = metadata
        self.impl = impl

    def run(self) -> Iterable[BenchmarkResult]:
        results = []

        with contextlib.ExitStack() as stack:
            self.impl.setup(stack)
            results = tuple(flatten(self.impl.run() for _ in range(self.times_to_run)))

        for result in results:
            for key, value in self.metadata.items():
                result[key] = value

        return results


def calculate_sha256sum(path: Path) -> str:
    return subprocess.run(
        ["sha256sum", str(path)],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    ).stdout.split()[0]


def download(url: str, sha256sum: str) -> Path:
    cache = Path(
        "/var/cache" if os.getuid() == 0 else os.getenv("XDG_CACHE_HOME", "~/.cache")
    ).joinpath("fpbench").expanduser()
    cache.mkdir(exist_ok=True)
    base = Path(urllib.parse.urlparse(url).path).name
    path = cache / base

    if path.exists():
        actual = calculate_sha256sum(path)
        if calculate_sha256sum(path) == sha256sum:
            print(f"Found existing file at {path}, skipping download")
            return path

        print(f"SHA256SUM mismatch for {base} ({actual} != {sha256sum})")

    subprocess.run(["curl", "-L", "-o", path, url], check=True)

    return path


def unzip(path: Path):
    cache = path.with_suffix('')

    if cache.exists():
        return cache

    subprocess.run(["unzip", "-d", cache, str(path)], check=True)

    return cache

def untar(path: Path, strip_components: int=0):
    cache = path.with_suffix('').with_suffix('')

    if cache.exists():
        return cache

    cache.mkdir(exist_ok=True)
    subprocess.run(["tar", "xf", str(path), "-C", str(cache), "--strip-components", str(strip_components)], check=True)

    return cache
