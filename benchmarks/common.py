from typing import Iterable, TypeVar, TypedDict, Mapping, ContextManager

T = TypeVar("T")


def flatten(xss: Iterable[Iterable[T]]) -> Iterable[T]:
    return (x for xs in xss for x in xs)


class BenchmarkResult(TypedDict):
    benchmark: str
    result: str
    value: float


class IBenchmark(ContextManager[None]):
    def run(self) -> Iterable[BenchmarkResult]:
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
        with self.impl:
            results = tuple(flatten(self.impl.run() for _ in range(self.times_to_run)))

        for result in results:
            for key, value in self.metadata.items():
                result[key] = value

        return results
