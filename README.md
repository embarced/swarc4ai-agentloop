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
- `uv` als Paketmanager
- OpenAI API Key gesetzt

Abhängigkeiten installieren:

```bash
uv sync
```

API-Key setzen:

```bash
export OPENAI_API_KEY="<dein-key>"
```

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

## Anwendung starten

```bash
uv run python src/agentic_loop/agent_loop.py
```

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
