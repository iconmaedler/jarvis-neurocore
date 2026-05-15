# 🧠 JARVIS NEUROCORE - Das ultimative KI-Agenten-System

Ein hochentwickeltes, modulares KI-System mit **3D-Gehirn-Visualisierung**, **Multi-Agenten-Schwarm**, **lokalem Systemzugriff** und **Echtzeit-Internet**.

---

## 🚀 One-Click Installation

### Automatische Installation (Empfohlen)

```bash
# Repository klonen
git clone https://github.com/iconmaedler/jarvis-neurocore.git
cd jarvis-neurocore

# One-Click Installer ausführen
chmod +x install.sh
./install.sh
```

**Der Installer erledigt automatisch:**
- ✅ Prüft Python-Version (3.10+)
- ✅ Erstellt virtuelle Umgebung
- ✅ Installiert alle Abhängigkeiten
- ✅ Erstellt .env Konfigurationsdatei
- ✅ Richtet Start-Skripte ein

### Manuelle Installation

```bash
# Virtuelle Umgebung erstellen
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# oder: venv\Scripts\activate  # Windows

# Abhängigkeiten installieren
pip install -r requirements.txt

# Konfiguration erstellen
cp .env.example .env
# Trage deine API-Keys in .env ein
```

---

## 🎯 Schnellstart

### Option 1: Mit Start-Skript (nach Installation)
```bash
./start_jarvis.sh
```

### Option 2: Manuell
```bash
# 3D-Gehirn im Hintergrund starten
python3 visuals/brain_dashboard.py &

# Hauptsystem starten
python3 main.py
```

### Option 3: Nur Gehirn-Visualisierung
```bash
python3 visuals/brain_dashboard.py
```

**Öffne dann im Browser:**
- **Lokal:** http://localhost:5000
- **Netzwerk:** http://21.0.12.42:5000

Du siehst sofort dein **lebendiges 3D-Gehirn** mit feuernenden Neuronen!

---

## 🌟 Kernfunktionen

### 🧠 NeuroCore 3D Gehirn
- **50+ Neuronen** in 4 spezialisierten Regionen (Logik, Memory, Kreativität, Lernen)
- **200+ Synapsen** für neuronale Verbindungen
- **Hebb'sche Lernregel**: "Neurons that fire together, wire together"
- **Echtzeit-Visualisierung** mit Three.js/WebGL
- **Wachstum**: Das Gehirn lernt mit jeder Aufgabe dazu

### 🤖 Multi-Agenten-Schwarm
Erstelle simultane Agenten für komplexe Aufgaben:
```python
from agents.multi_agent_system import create_swarm

swarm = create_swarm(
    task="Recherchiere KI-Trends 2024",
    num_agents=5,
    roles=["researcher", "analyst", "fact_checker", "summarizer", "critic"]
)
results = swarm.execute()
consensus = swarm.find_consensus(results)
```

**Verfügbare Rollen:**
- `researcher` - Websuche & Datensammlung
- `analyst` - Mustererkennung & Analyse
- `fact_checker` - Faktenverifikation
- `coder` - Code-Generierung & Review
- `creative` - Ideengenerierung
- `critic` - Qualitätskontrolle

### 🖥️ Lokaler Systemzugriff
Vollständige Kontrolle über deinen Computer:
```python
from actions.local_system import (
    read_file, write_file, list_directory,
    execute_command, get_system_info, search_files
)

# Datei lesen
content = read_file("/pfad/zur/datei.txt")

# Terminal-Befehl (gesichert)
result = execute_command("ls -la")

# System-Infos
info = get_system_info()
```

### 🌐 Echtzeit-Internet
Live-Daten aus dem Web:
```python
from services.realtime_internet import (
    web_search, get_news, get_weather,
    get_stock_price, download_url
)

# Websuche
results = web_search("KI Entwicklung 2024")

# Nachrichten
news = get_news(category="technology")

# Wetter
weather = get_weather(city="Berlin")

# Aktienkurse
price = get_stock_price("AAPL")
```

### 🎙️ Stimm-Engine
Passe die Stimme dynamisch an:
```python
from audio.voice_engine import set_voice, speak

# Stimme per Beschreibung anpassen
set_voice("tief, warm, professionell, langsam")
speak("Willkommen zurück, Sir.")

# Vordefinierte Profile
set_voice("jervis_classic")  # Klassischer Butler
set_voice("friendly_female")  # Freundlich, weiblich
set_voice("robotic")  # Roboterhaft
```

### 📊 Task-Visualisierung
Echtzeit-Einblick in alle laufenden Aufgaben:
- Aktive Agenten
- Fortschrittsbalken
- Ergebnis-Vergleich
- Konsens-Findung

---

## 🛠️ Eigene Tools/Skills hinzufügen

### Schritt-für-Schritt

1. **Neue Datei erstellen** in `/workspace/actions/`:
   ```python
   # /workspace/actions/mein_neues_tool.py
   
   TOOL_DECLARATION = {
       "name": "mein_tool",
       "description": "Beschreibt was das Tool macht",
       "parameters": {
           "type": "object",
           "properties": {
               "param1": {"type": "string", "description": "Beschreibung"}
           },
           "required": ["param1"]
       }
   }

   def mein_tool(parameters, player, session_memory):
       # Deine Logik hier
       return {"success": True, "result": "Ergebnis"}
   ```

2. **Automatisches Laden**: Das Tool wird beim nächsten Start automatisch erkannt!

3. **Nutzen**:
   ```python
   from core.tool_loader import load_all_tools
   tools = load_all_tools()
   tools["mein_tool"]({...})
   ```

---

## 📁 Projektstruktur

```
/workspace
├── brain/                  # NeuroCore Gehirn-Engine
│   ├── neuro_core.py       # Hauptlogik mit Lernregeln
│   └── neurons.py          # Neuronen-Definitionen
├── visuals/                # 3D-Visualisierungen
│   ├── brain_dashboard.py  # Web-Server für 3D-Gehirn
│   └── templates/          # HTML/JS Templates
├── agents/                 # Multi-Agenten-System
│   └── multi_agent_system.py
├── actions/                # Tools & Skills
│   ├── local_system.py     # PC-Zugriff
│   ├── example_skill.py    # Vorlage für neue Tools
│   └── [deine_tools].py
├── services/               # Externe Dienste
│   └── realtime_internet.py
├── audio/                  # Sprachausgabe
│   └── voice_engine.py
├── core/                   # Kernsystem
│   ├── tool_loader.py      # Dynamisches Tool-Laden
│   └── IMPORT_INTERFACE.md
├── FEATURES_OVERVIEW.md    # Feature-Dokumentation
├── BRAIN_VISUALIZATION.md  # Gehirn-Doku
└── README.md               # Diese Datei
```

---

## 🔧 Konfiguration

### API-Keys (optional für volle Internet-Funktionen)

Erstelle `.env` im Root-Verzeichnis:
```bash
GOOGLE_API_KEY=dein_google_key
NEWS_API_KEY=dein_news_key
OPENWEATHER_API_KEY=dein_weather_key
ALPHA_VANTAGE_KEY=dein_stock_key
```

### Sicherheitseinstellungen

In `actions/local_system.py` kannst du gefährliche Befehle blockieren:
```python
BLOCKED_COMMANDS = ["rm -rf /", "sudo", "mkfs", ...]
```

---

## 🎮 Interaktive Nutzung

### Python REPL
```python
>>> from brain.neuro_core import get_brain
>>> brain = get_brain()
>>> brain.process_task("Analysiere diese Daten...")
```

### Kommandozeile
```bash
python3 -c "from agents.multi_agent_system import create_swarm; print(create_swarm('Test', 3))"
```

---

## 📈 Live-Statistiken

Das Dashboard zeigt in Echtzeit:
- **Neuronen-Aktivität**: Welche Regionen gerade feuern
- **Synapsen-Stärke**: Gelernte Verbindungen
- **Wissensstand**: Kumuliertes Wissen
- **Aufgaben-Historie**: Alle bearbeiteten Tasks
- **Agenten-Status**: Parallele Prozesse

---

## 🐛 Troubleshooting

### Website nicht erreichbar?
1. Prüfe ob Server läuft: `curl http://localhost:5000`
2. Port freigeben: `sudo ufw allow 5000`
3. Firewall prüfen

### Tools werden nicht geladen?
- Stelle sicher dass `TOOL_DECLARATION` definiert ist
- Funktion muss exakt so heißen wie im Declaration-Name
- Keine Syntaxfehler in der Datei

### Stimmen klingen falsch?
- Audio-Treiber prüfen
- Bibliotheken installieren: `pip install pyttsx3 speechrecognition`

---

## 🚀 Nächste Schritte

1. **Browser öffnen**: http://localhost:5000
2. **Erste Aufgabe stellen**: Beobachte wie Neuronen feuern
3. **Agenten-Schwarm starten**: Parallele Recherche testen
4. **Eigenes Tool bauen**: Nach Vorlage in `example_skill.py`
5. **Stimme anpassen**: Finde deine perfekte Voice

---

## 📚 Dokumentation

- [Gehirn-Visualisierung](BRAIN_VISUALIZATION.md)
- [Features Übersicht](FEATURES_OVERVIEW.md)
- [Tool Import Guide](core/IMPORT_INTERFACE.md)

---

**Entwickelt für maximale Flexibilität und Echtzeit-Interaktion.**  
🧠 *Dein Gehirn wächst mit jeder Aufgabe!*
