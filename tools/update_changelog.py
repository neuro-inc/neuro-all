#!/usr/bin/env python3
import click
import datetime
import subprocess
from all_repos.clone import main as clone_main
from difflib import SequenceMatcher
from pathlib import Path
from typing import Optional


def fetch(name: str) -> Optional[str]:
    changelog = Path("cloned") / name / "CHANGELOG.md"
    txt = changelog.read_text()
    TEMPLATE = "[comment]: # (towncrier release notes start)\n"
    idx = txt.index(TEMPLATE)
    right = txt[idx + len(TEMPLATE) :]
    old = Path(name + ".txt")
    left = old.read_text()
    matcher = SequenceMatcher(None, left, right)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            return None
        if tag != "insert":
            raise ValueError(
                f"insert is expected as a first matcher opcode, "
                f"found {tag} '{left[i1:i2]}' ---> '{right[j1:j2]}'"
            )
        old.write_text(right)
        return right[j1:j2]


UPSTREAMS = ("platform-client-python", "neuro-extras", "neuro-flow")


@click.command()
def main() -> None:
    clone_main()
    changes = []
    for name in UPSTREAMS:
        ret = fetch(name)
        if ret is not None:
            changes.append(ret)

    if not changes:
        raise click.UsageError(
            "CHANGELOG.md is not updated:\n" f"Nothing changed in upstreams {UPSTREAMS}"
        )

    changelog = Path("CHANGELOG.md")
    txt = changelog.read_text()
    TEMPLATE = "[comment]: # (release notes start)"
    idx = txt.index(TEMPLATE) + len(TEMPLATE)
    pre = txt[:idx]
    post = txt[idx:]
    proc = subprocess.run(
        ["poetry", "version", "--short"], capture_output=True, check=True, text=True
    )
    version = proc.stdout.strip()
    date = datetime.date.today().isoformat()
    header = f"Neuro {version} ({date})\n"
    header += "=" * (len(header) - 1) + "\n"
    changelog.write_text(pre + "\n\n" + header + "".join(changes) + post)

    click.echo("CHANGELOG.md is updated")


if __name__ == "__main__":
    main()
