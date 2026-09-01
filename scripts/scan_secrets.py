from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(".")
ALLOW_MARKER = "secret-scan: allow-test-fixture"
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache"}
BINARY_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip",
    ".gz", ".tar", ".pyc", ".p12", ".pfx",
}

PATTERNS = [
    ("AWS access key id", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    (
        "Private key header",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    ),
    (
        "AWS credential assignment",
        re.compile(
            r"\b(?:AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY|AWS_SESSION_TOKEN)\b\s*[:=]\s*[\"']?[^\s\"']{8,}"
        ),
    ),
]


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    kind: str


def find_secret_findings(text: str, path: str) -> list[Finding]:
    findings: list[Finding] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if ALLOW_MARKER in line:
            continue
        for kind, pattern in PATTERNS:
            if pattern.search(line):
                findings.append(Finding(path=path, line=line_number, kind=kind))
    return findings


def iter_text_files(root: Path = ROOT):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in BINARY_SUFFIXES:
            continue
        yield path


def main() -> None:
    findings: list[Finding] = []
    for path in iter_text_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        findings.extend(find_secret_findings(text, path.as_posix()))

    if findings:
        print("[ERRO] Possíveis segredos encontrados:")
        for finding in findings:
            print(f"- {finding.path}:{finding.line} — {finding.kind}")
        raise SystemExit(1)

    print("[OK] Nenhum padrão de segredo de alto risco foi detectado nos arquivos de texto.")


if __name__ == "__main__":
    main()
