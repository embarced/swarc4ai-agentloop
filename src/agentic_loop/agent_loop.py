import argparse
import json
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx
from openai import DefaultHttpxClient, OpenAI


@dataclass(slots=True)
class AgentAction:
    thought: str
    action: str
    args: dict[str, str]

    @classmethod
    def from_json(cls, content: str) -> "AgentAction":
        data = json.loads(content)
        return cls(
            thought=data["thought"],
            action=data["action"],
            args=data.get("args", {}),
        )


def run_shell(command: str) -> str:
    print(f"Führe Shell aus: {command}")
    try:
        process = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=False,
        )
        output = process.stdout + process.stderr
        return output if output.strip() else "Befehl ausgeführt (kein Output)"
    except Exception as error:
        return f"Fehler: {error}"


def read_file(path: str) -> str:
    print(f"Lese Datei: {path}")
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError as error:
        return f"Fehler: {error}"


def write_file(path: str, content: str) -> str:
    print(f"Schreibe Datei: {path}")
    try:
        Path(path).write_text(content, encoding="utf-8")
        return "Erfolg: Datei gespeichert."
    except OSError as error:
        return f"Fehler: {error}"


SYSTEM_PROMPT = """
Du bist ein autonomer Python Coding-Agent.
Antworte IMMER im rohen JSON-Format. Kein Markdown!

Struktur:
{
  "thought": "Überlegung...",
  "action": "run_shell" | "read_file" | "write_file" | "finish",
  "args": { "command": "...", "path": "...", "content": "..." }
}

Tools:
1. run_shell(command): Führt Befehle aus.
2. write_file(path, content): Erstellt Dateien.
3. read_file(path): Liest Dateien.
4. finish(): Wenn Aufgabe erledigt.
""".strip()

TASK = (
    "Erstelle einen neuen Unterordner 'HelloWorld'. Lege darin eine Datei "
    "'main.py' an, die 'Hallo Welt aus Python' ausgibt. Führe das Programm "
    "in diesem Ordner aus."
)


SENSITIVE_HEADERS = {
    "authorization",
    "api-key",
    "x-api-key",
    "cookie",
    "set-cookie",
}


def sanitized_headers(headers: httpx.Headers) -> dict[str, str]:
    return {
        name: "<redacted>" if name.lower() in SENSITIVE_HEADERS else value
        for name, value in headers.items()
    }


def format_http_body(body: bytes, encoding: str = "utf-8") -> str:
    if not body:
        return "<empty>"

    text = body.decode(encoding, errors="replace")
    try:
        return json.dumps(
            json.loads(text),
            ensure_ascii=False,
            indent=2,
        )
    except json.JSONDecodeError:
        return text


def log_http_request(request: httpx.Request) -> None:
    request.read()

    print("\n=== OpenAI Request ===")
    print(f"{request.method} {request.url}")
    print("Headers:")
    print(
        json.dumps(
            sanitized_headers(request.headers),
            ensure_ascii=False,
            indent=2,
        )
    )
    print("Body:")
    print(format_http_body(request.content))


def log_http_response(response: httpx.Response) -> None:
    response.read()
    encoding = response.encoding or "utf-8"

    print("=== OpenAI Response ===")
    print(f"Status: {response.status_code}")
    print("Headers:")
    print(
        json.dumps(
            sanitized_headers(response.headers),
            ensure_ascii=False,
            indent=2,
        )
    )
    print("Body:")
    print(format_http_body(response.content, encoding))
    print("=======================\n")


def create_openai_client(http_logging: bool = False) -> OpenAI:
    if not http_logging:
        return OpenAI()

    http_client = DefaultHttpxClient(
        event_hooks={
            "request": [log_http_request],
            "response": [log_http_response],
        }
    )
    return OpenAI(http_client=http_client)


def run_agent(client: Any | None = None, max_steps: int = 15) -> None:
    api_client = client or OpenAI()
    messages: list[dict[str, str]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Aufgabe: {TASK}"},
    ]

    print("Starte Agent...\n")

    for _ in range(max_steps):
        response = api_client.chat.completions.create(
            model="gpt-4o",
            temperature=0.1,
            response_format={"type": "json_object"},
            messages=messages,
        )
        content = response.choices[0].message.content or ""

        # TODO: ÜBUNG 1 - Parse den JSON-String in ein AgentAction-Objekt.
        # TODO: ÜBUNG 1 - Gib den Gedanken des Agenten aus, damit der Loop nachvollziehbar wird.
        # TODO: ÜBUNG 1 - Beende den Loop sofort, wenn die Action "finish" ist.
        # TODO: ÜBUNG 1 - Rufe je nach Action die passende Tool-Funktion auf:
        # run_shell, read_file oder write_file.
        # TODO: ÜBUNG 1 - Behandle unbekannte Actions als Fehlertext.
        # TODO: ÜBUNG 1 - Gib das Tool-Ergebnis gekürzt auf der Konsole aus.
        # TODO: ÜBUNG 1 - Füge die Assistant-Antwort und das Tool-Ergebnis wieder
        # zur Message-History hinzu, damit der Agent im nächsten Schritt auf dem
        # letzten Ergebnis weiterarbeiten kann.
        # SO PRÜFST DU ES: Starte das Programm. Der Agent sollte mehrere Schritte
        # ausführen, eine Datei im Ordner "HelloWorld" erzeugen, sie ausführen und
        # am Ende "Hallo Welt aus Python" ausgeben.
        raise NotImplementedError(
            "ÜBUNG 1: Implementiere JSON-Parsing, Tool-Routing und History-Update."
        )


def parse_args(args: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ein einfacher autonomer Coding-Agent."
    )
    parser.add_argument(
        "--http-logging",
        action="store_true",
        help="OpenAI HTTP-Requests und -Responses protokollieren.",
    )
    return parser.parse_args(args)


def main(args: Sequence[str] | None = None) -> None:
    options = parse_args(args)
    with create_openai_client(options.http_logging) as client:
        run_agent(client)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAbgebrochen.", file=sys.stderr)
