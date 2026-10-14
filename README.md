# Anleitung: Python-Übung "Agentic Loop"

## Ziel der Übung

In dieser Übung baut ihr einen einfachen Agentic Loop in Python:

1. Ein System Prompt definiert das erlaubte JSON-Format.
2. Das LLM entscheidet pro Schritt über die nächste Aktion.
3. Python führt Tools wie `run_shell`, `read_file` und `write_file` aus.
4. Die Tool-Ergebnisse werden wieder in die Nachrichtenhistorie eingespeist.
5. Der Agent arbeitet iterativ, bis die Aufgabe erledigt ist.

Am Ende steht ein einfacher autonomer Coding-Agent mit ReAct-artigem Loop:
Prompt -> LLM-Antwort -> Tool-Ausführung -> Tool-Feedback -> nächster Schritt.

## Voraussetzungen

- Python 3.13
- OpenAI API Key gesetzt

`uv` ist der empfohlene Paketmanager, aber nicht zwingend erforderlich.

## Installation

### Empfohlen: mit uv

Abhängigkeiten aus der mitgelieferten Lock-Datei installieren:

```bash
uv sync --frozen
```

### Alternative: nur mit Python 3.13 und pip

Virtuelle Umgebung erstellen und aktivieren:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

Unter Windows wird die Umgebung so aktiviert:

```powershell
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
```

Danach die Abhängigkeiten installieren:

```bash
python -m pip install -r requirements.txt
```

## API-Key setzen

```bash
export OPENAI_API_KEY="<dein-key>"
```

## Anwendung starten

Mit `uv`:

```bash
uv run python src/agentic_loop/agent_loop.py
```

Ohne `uv` in der aktivierten virtuellen Umgebung:

```bash
python src/agentic_loop/agent_loop.py
```

### Optionales HTTP-Logging

Ein vollständiger HTTP-Log kann mit `--http-logging` aktiviert werden.

Mit `uv`:

```bash
uv run python src/agentic_loop/agent_loop.py --http-logging
```

Ohne `uv`:

```bash
python src/agentic_loop/agent_loop.py --http-logging
```

Der Logger gibt die JSON-Bodies vollständig und eingerückt aus. Besonders
interessant ist im Request das Feld `messages`: Dort sind der System Prompt,
die Aufgabe, frühere Agent-Antworten und die bisherigen Tool-Ergebnisse zu
sehen.

Diese Übung verwendet bewusst nicht das native Tool-Calling der OpenAI API.
Deshalb gibt es im Request kein `tools`-Feld. Stattdessen beschreibt der
System Prompt die erlaubten Aktionen `run_shell`, `read_file`, `write_file`
und `finish`. Das Modell antwortet mit einer JSON-Aktion, die anschließend
vom Python-Code ausgeführt wird.

Ohne den Parameter ist das HTTP-Logging deaktiviert.
Authentifizierungs-Header und Cookies werden maskiert. Request- und
Response-Bodies können jedoch Prompts, Tool-Ergebnisse und Modellantworten
enthalten und sollten deshalb nicht in öffentliche Logs kopiert werden.

## Arbeitsweise

Dieses Repository enthält:

- den Branch `ex1` mit einer unvollständigen Übungsaufgabe
- den Branch `main` mit der vollständigen Referenzlösung

Wichtig:

- `# TODO`-Texte und `# SO PRÜFST DU ES` sind auf Deutsch
- Klassen- und Variablennamen bleiben Englisch

## Branch-Ablauf

### 1) Übungs-Branch: `ex1`

```bash
git checkout ex1
```

Sucht TODOs nach `ÜBUNG 1`.

Inhaltlich:

- JSON-Antwort in `AgentAction` parsen
- den `thought` des Agenten ausgeben
- auf `finish` reagieren
- je nach `action` die passende Tool-Funktion ausführen
- unbekannte Actions sinnvoll behandeln
- Tool-Ergebnis wieder in die History zurückschreiben

Testidee:

- App starten
- Prüfen, ob der Agent mehrere Schritte ausführt
- Beobachten, dass der Agent den Ordner `HelloWorld` anlegt
- Beobachten, dass darin `main.py` erstellt und ausgeführt wird

### 2) Referenzlösung: `main`

```bash
git checkout main
```

`main` enthält die vollständige, lauffähige Lösung.

## Nützliche Kommandos

TODOs finden:

```bash
rg "ÜBUNG" src
```

Status prüfen:

```bash
git status
git diff
```

Branch wechseln:

```bash
git checkout <branch-name>
```

## Wichtige Datei

- `src/agentic_loop/agent_loop.py`
  - System Prompt, Tool-Funktionen, OpenAI-Aufruf, Loop, History-Update und Aufgabenstellung

## Abschluss

Wenn die TODOs in `ex1` gelöst sind, vergleicht mit:

```bash
git checkout main
```
