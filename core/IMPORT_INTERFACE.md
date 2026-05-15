# Jarvis Tool/Skill Import Interface

## Übersicht

Das System verfügt jetzt über eine dynamische Schnittstelle zum Importieren von Tools und Skills. Diese ermöglicht es, neue Funktionen einfach hinzuzufügen, ohne den Hauptcode ändern zu müssen.

## Struktur

```
/workspace/
├── core/
│   └── tool_loader.py      # Dynamischer Tool-Loader
├── actions/
│   ├── example_skill.py    # Vorlage für neue Tools
│   └── ...                 # Existing actions
└── main.py                 # Hauptprogramm
```

## So erstellen Sie ein neues Tool/Skill

### 1. Erstellen Sie eine neue Datei im `actions`-Verzeichnis

Erstellen Sie eine Datei namens `mein_neues_tool.py` im `/workspace/actions/` Verzeichnis.

### 2. Definieren Sie die TOOL_DECLARATION

Jedes Tool benötigt eine `TOOL_DECLARATION`, die dem KI-Modell erklärt, was das Tool tut:

```python
TOOL_DECLARATION = {
    "name": "mein_neues_tool",
    "description": "Beschreibung, was das Tool macht und wann es verwendet werden soll",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "param1": {"type": "STRING", "description": "Beschreibung des Parameters"},
            "param2": {"type": "INTEGER", "description": "Ein weiterer Parameter"}
        },
        "required": ["param1"]
    }
}
```

### 3. Implementieren Sie die Hauptfunktion

Die Funktion muss denselben Namen wie das Tool haben (oder verwenden Sie einen Alias):

```python
def mein_neues_tool(parameters: dict, player=None, session_memory=None):
    # Extrahiere Parameter
    param1 = parameters.get("param1")
    
    # Deine Logik hier
    ergebnis = f"Erledigt: {param1}"
    
    # Loggen und sprechen
    if player:
        player.write_log(f"JARVIS: {ergebnis}")
    
    return ergebnis
```

### 4. Das Tool wird automatisch geladen

Der `ToolLoader` erkennt alle `.py`-Dateien im `actions`-Verzeichnis automatisch und lädt sie.

## Verwendung in main.py

### Option A: Automatische Tool-Erkennung

```python
from core.tool_loader import get_tool_loader

# Tool-Loader initialisieren
loader = get_tool_loader()
loader.load_all_tools()

# Tool-Deklarationen für die API abrufen
tool_declarations = loader.get_all_declarations()

# Tool-Funktion bei Ausführung aufrufen
def execute_tool(tool_name, args):
    func = loader.get_tool_function(tool_name)
    if func:
        return func(parameters=args, player=ui, session_memory=None)
```

### Option B: Manuelles Importieren eines externen Tools

```python
from pathlib import Path
from core.tool_loader import get_tool_loader

loader = get_tool_loader()

# Externes Tool importieren
externes_tool = Path("/pfad/zu/meinem/tool.py")
loader.import_external_tool(externes_tool)
```

## Beispiel: Einfaches Begrüßungs-Tool

```python
# actions/greet.py

TOOL_DECLARATION = {
    "name": "greet",
    "description": "Begrüßt eine Person mit Namen",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "name": {"type": "STRING", "description": "Name der Person"}
        },
        "required": ["name"]
    }
}

def greet(parameters: dict, player=None, session_memory=None):
    name = parameters.get("name", "Sir")
    msg = f"Hello, {name}!"
    
    if player:
        player.write_log(f"JARVIS: {msg}")
        player.speak(msg)
    
    return msg
```

## API-Referenz

### ToolLoader Klasse

```python
from core.tool_loader import ToolLoader
from pathlib import Path

# Initialisierung
loader = ToolLoader(actions_dir=Path("/workspace/actions"))

# Alle Tools laden
count = loader.load_all_tools()

# Einzelnes Tool neu laden
loader.reload_tool("tool_name")

# Alle Tools neu laden
loader.reload_all_tools()

# Tool-Funktion abrufen
func = loader.get_tool_function("tool_name")

# Alle Deklarationen für die API
declarations = loader.get_all_declarations()

# Externes Tool importieren
loader.import_external_tool(Path("/pfad/zum/tool.py"))
```

### Convenience-Funktionen

```python
from core.tool_loader import load_all_tools, get_tool_loader

# Alle Tools laden und Deklarationen + Funktionen erhalten
declarations, functions = load_all_tools()

# Loader-Instanz erhalten (Singleton)
loader = get_tool_loader()
```

## Hinweise

1. **Fehlerbehandlung**: Tools, die nicht geladen werden können (fehlende Abhängigkeiten), werden übersprungen
2. **Automatische Erkennung**: Der Loader sucht nach `TOOL_DECLARATION` und einer Funktion mit passendem Namen
3. **Alias-Funktionen**: Wenn Ihre Hauptfunktion anders heißt (z.B. `weather_action`), erstellen Sie einen Alias mit dem Tool-Namen
4. **Logging**: Verwenden Sie `player.write_log()` für Logs und `player.speak()` für Sprachausgabe

## Nächste Schritte

1. Kopieren Sie `example_skill.py` als Vorlage
2. Passen Sie die `TOOL_DECLARATION` an Ihr Tool an
3. Implementieren Sie Ihre Logik
4. Starten Sie das System - das Tool wird automatisch erkannt!
