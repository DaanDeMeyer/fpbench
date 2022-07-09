#!/usr/bin/env python3

import subprocess
import argparse
import json

from typing import Sequence, List, Any, TYPE_CHECKING

if TYPE_CHECKING:
    CompletedProcess = subprocess.CompletedProcess[Any]
else:
    CompletedProcess = subprocess.CompletedProcess


COPR = "daandemeyer/fno-omit-frame-pointer"


def run(
    cmd: Sequence[str],
    check: bool = True,
    **kwargs: Any,
) -> CompletedProcess:
    return subprocess.run(cmd, check=check, text=True, **kwargs)


def resolve(package: str, resolve_deps: bool) -> List[str]:
    source = run(
        [
            "dnf",
            "repoquery",
            "--disablerepo=*",
            "--enablerepo=rawhide",
            "--quiet",
            "--arch=x86_64",
            "--qf",
            "%{source_name}",
            package,
        ],
        stdout=subprocess.PIPE,
    ).stdout.splitlines()[-1]

    deps: Sequence[str] = (
        []
        if not resolve_deps
        else run(
            [
                "dnf",
                "repoquery",
                "--disablerepo=*",
                "--enablerepo=rawhide",
                "--quiet",
                "--arch=x86_64",
                "--qf",
                "%{source_name}",
                "--requires",
                "--resolve",
                "--recursive",
                package,
            ],
            stdout=subprocess.PIPE,
        ).stdout.splitlines()
    )

    return [source, *deps]


def exists_in_copr(package: str) -> bool:
    return not (
        f"No package with name {package}"
        in run(
            ["copr", "get-package", COPR, "--name", package],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            check=False,
        ).stderr
    )


def build_in_copr(package: str, force: bool) -> None:
    exists = exists_in_copr(package)

    if exists and not force:
        return

    verb = "edit" if exists else "add"

    print(f"Submitting {verb} for {package}")

    run(
        [
            "copr",
            f"{verb}-package-distgit",
            COPR,
            "--name",
            package,
            "--commit=f37",
            "--webhook-rebuild=on",
            "--max-builds=0",
        ],
        stdout=subprocess.DEVNULL,
    )

    print(f"Submitting build for {package}")

    run(
        [
            "copr",
            "build-package",
            COPR,
            "--name",
            package,
            "--nowait",
            "--timeout",
            "172800",
        ],
        stdout=subprocess.DEVNULL,
    )


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("--submit", dest="dryrun", action="store_false")
    parser.add_argument("--deps", action="store_true")
    parser.add_argument("--force", action="store_true")

    args, packages = parser.parse_known_args()
    packages = {
        srpm
        for package in packages
        for srpm in resolve(package, resolve_deps=args.deps)
    }
    packages = sorted(packages)

    if args.dryrun:
        for package in packages:
            print(package)
    else:
        for package in packages:
            build_in_copr(package, force=args.force)


if __name__ == "__main__":
    main()
