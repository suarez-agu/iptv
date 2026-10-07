#!/usr/bin/env python3

import argparse
import re
import urllib.request
from pathlib import Path

SOURCE_URL = "https://iptv-org.github.io/iptv/index.country.m3u"
EL_TRECE_URL = "https://livetrx01.vodgc.net/eltrecetv/index.m3u8"
EL_TRECE_REFERRER = "https://vodgc.net"
TARGET_TVG_ID = "ElTrece.ar"


def is_el_trece(extinf_line: str) -> bool:
    """Match ElTrece.ar and variants such as ElTrece.ar@SD."""
    match = re.search(r'tvg-id="([^"]+)"', extinf_line)
    if not match:
        return False
    tvg_id = match.group(1)
    return tvg_id == TARGET_TVG_ID or tvg_id.startswith(TARGET_TVG_ID + "@")


def patch_playlist(text: str) -> str:
    """Keep IPTV-org intact except for the El Trece stream."""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")

    output = []
    matches = 0
    i = 0

    while i < len(lines):
        line = lines[i]

        if not line.startswith("#EXTINF:"):
            output.append(line)
            i += 1
            continue

        block = [line]
        i += 1
        while i < len(lines) and not lines[i].startswith("#EXTINF:"):
            block.append(lines[i])
            i += 1

        if is_el_trece(block[0]):
            matches += 1
            output.append(block[0])
            output.append(f"#EXTVLCOPT:http-referrer={EL_TRECE_REFERRER}")
            output.append(EL_TRECE_URL)

            trailing_blanks = 0
            for item in reversed(block[1:]):
                if item == "":
                    trailing_blanks += 1
                else:
                    break
            output.extend([""] * trailing_blanks)
        else:
            output.extend(block)

    if matches == 0:
        raise RuntimeError(
            f"Could not find {TARGET_TVG_ID!r} in the source playlist. "
            "IPTV-org may have changed its metadata format; refusing to publish "
            "an unpatched playlist."
        )

    if matches > 1:
        raise RuntimeError(
            f"Found {matches} El Trece entries. Expected exactly 1; refusing to "
            "publish until the script is reviewed."
        )

    while output and output[-1] == "":
        output.pop()

    return "\r\n".join(output) + "\r\n"


def fetch_playlist(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "iptv-org-el-trece-mirror/1.0 (+GitHub Actions)"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read()

    text = data.decode("utf-8-sig")
    if not text.lstrip().startswith("#EXTM3U"):
        raise RuntimeError("Downloaded content does not look like an M3U playlist.")
    return text


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Mirror IPTV-org and override the El Trece stream."
    )
    parser.add_argument("--source", default=SOURCE_URL)
    parser.add_argument(
        "--output",
        default="docs/index.country.m3u",
        help="Output M3U path (default: docs/index.country.m3u)",
    )
    args = parser.parse_args()

    source = fetch_playlist(args.source)
    patched = patch_playlist(source)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        f.write(patched)

    print(f"Wrote patched playlist to {output_path}")
    print(f"El Trece override: {EL_TRECE_URL}")


if __name__ == "__main__":
    main()
