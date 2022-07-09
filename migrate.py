#!/usr/bin/env python3

import json
from pathlib import Path

p = Path("bench.json")
j = json.loads(p.read_text())

for b in j:
    if "blender" in b["benchmark"]:
        b["result"] = "Duration (s)"
        b["value"] = int(b["value"] / 1000000)

    if "botan" in b["benchmark"]:
        b["result"] = b["result"].replace("bytes", "MB")
        b["value"] /= 1000000

    if "openssl" in b["benchmark"]:
        b["result"] = b["result"].replace("bytes", "MB")
        b["value"] /= 1000000

Path("benchv2.json").write_text(json.dumps(j, indent=4))
