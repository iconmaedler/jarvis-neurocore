# Erweiterte Jarvis-Fähigkeiten

## Übersicht

Das System wurde um **fünf** mächtige Module erweitert:

### 1. 🖥️ Lokaler System-Zugriff (`/workspace/actions/local_system.py`)

**Funktionen:**
- **read_file**: Dateien vom lokalen Computer lesen
- **write_file**: Dateien schreiben (mit Verzeichnis-Erstellung)
- **list_directory**: Verzeichnisse auflisten (optional rekursiv)
- **execute_command**: Terminal-Befehle ausführen (mit Sicherheitsfilter)
- **get_system_info**: System-Informationen (CPU, RAM, OS, Festplatte)
- **search_files**: Dateisystem durchsuchen nach Mustern

**Sicherheitsfeatures:**
- Zugriff nur auf Home-Verzeichnis, /workspace und aktuelles Arbeitsverzeichnis
- Gefährliche Befehle werden blockiert (rm -rf /, mkfs, etc.)
- Timeout für Befehlsausführung

**Beispiel:**
```python
# Datei lesen
read_file({"file_path": "~/dokumente/notizen.txt"})

# Terminal-Befehl
execute_command({"command": "ls -la", "working_directory": "/workspace"})

# System-Infos
get_system_info({"info_type": "all"})
```

---

### 2. 🤖 Multi-Agenten-System (`/workspace/agents/multi_agent_system.py`)

**Funktionen:**
- **create_search_agents**: Erstellt mehrere Agenten für parallele Suche
  - Simultane Recherche über verschiedene Quellen
  - Automatischer Konsens-Abgleich
  - Konfigurierbare Anzahl an Agenten (2-10)
  
- **deploy_research_team**: Setzt spezialisiertes Forschungsteam ein
  - Verschiedene Rollen: researcher, analyst, fact_checker, etc.
  - Parallele Aufgabenbearbeitung
  - Zeitgesteuerte Ausführung
  
- **compare_agent_results**: Vergleicht und bewertet Agenten-Ergebnisse
  - Konsistenzprüfung
  - Qualitätsbewertung
  - Identifiziert Übereinstimmungen und Widersprüche

**Agenten-Rollen:**
- `researcher`: Datensammlung und Quellenanalyse
- `analyst`: Mustererkennung und Trendanalyse
- `fact_checker`: Verifikation und Faktenprüfung
- `summarizer`: Zusammenfassung und Synthese
- `critic`: Qualitätsbewertung und Gegenargumente

**Beispiel:**
```python
# 3 Agenten suchen parallel mit Konsens-Abgleich
create_search_agents({
    "query": "Klimawandel Auswirkungen 2025",
    "num_agents": 3,
    "search_engines": ["google", "bing", "duckduckgo"],
    "consensus_threshold": 0.6
})

# Forschungsteam einsetzen
deploy_research_team({
    "topic": "Künstliche Intelligenz in der Medizin",
    "agent_roles": ["researcher", "analyst", "fact_checker"],
    "time_limit_seconds": 60
})
```

---

### 3. 🌐 Echtzeit-Internet-Zugriff (`/workspace/services/realtime_internet.py`)

**Funktionen:**
- **web_search**: Echtzeit-Web-Suche
  - Sprachsteuerung (de, en, etc.)
  - Zeitfilter (Tag, Woche, Monat, Jahr)
  - Relevanz-Bewertung
  
- **get_news**: Aktuelle Nachrichten
  - Themen-spezifisch
  - Länder-spezifisch
  - Optional mit Volltext
  
- **get_weather**: Wetterdaten und Vorhersage
  - Aktuelle Bedingungen
  - Bis zu 7 Tage Vorhersage
  - Metrische oder imperiale Einheiten
  
- **get_stock_price**: Aktienkurse und Finanzdaten
  - Echtzeit-Kurse
  - Historische Daten (30 Tage)
  - Umfangreiche Kennzahlen (P/E, Market Cap, etc.)
  
- **fetch_url**: Webseiten herunterladen
  - HTML oder extrahierter Text
  - Timeout-Steuerung
  - Sicherheitsfilter
  
- **check_website_status**: Website-Verfügbarkeit prüfen
  - Response-Time Messung
  - SSL-Zertifikat-Prüfung
  - Server-Informationen

**Beispiel:**
```python
# Web-Suche
web_search({
    "query": "Neueste KI-Entwicklungen",
    "num_results": 10,
    "language": "de",
    "time_range": "week"
})

# Nachrichten
get_news({
    "topic": "Technologie",
    "country": "de",
    "num_articles": 5,
    "include_full_content": True
})

# Wetter
get_weather({
    "location": "Berlin",
    "days": 5,
    "units": "metric"
})

# Aktienkurs
get_stock_price({
    "symbol": "AAPL",
    "include_history": True
})
```

---

### 4. 🧠 NeuroCore - 3D Gehirn Visualisierung

**Neu!** Ein lernendes neuronales Netzwerk mit Echtzeit-3D-Visualisierung.

**Dateien:**
- `/workspace/brain/neuro_core.py` - Die Gehirn-Engine
- `/workspace/visuals/brain_dashboard.py` - Das 3D Dashboard
- `/workspace/BRAIN_VISUALIZATION.md` - Detaillierte Dokumentation

**Funktionen:**
- **50 Neuronen** in 3D-Raum kugelförmig angeordnet
- **200+ Synapsen** verbinden die Neuronen
- **Hebb'sche Lernregel**: "Neurons that fire together, wire together"
- **4 Gehirnregionen**: Logic, Memory, Creativity, Learning
- **Three.js Visualisierung** im Browser
- **Echtzeit-Statistiken** und Aktivitäts-Logs

**Starten:**
```bash
cd /workspace
python3 visuals/brain_dashboard.py
```

Öffne dann **http://localhost:5000** in deinem Browser!

**Integration:**
```python
from brain.neuro_core import get_brain

brain = get_brain()
result = brain.process_task("Beschreibe die Aufgabe hier")
print(f"Aktive Neuronen: {result['active_neurons']}")
```

---

### 5. 🎨 Task Visualisierung & Stimm-Modul

**In Entwicklung** - Wird als nächstes implementiert:
- Interaktives Task-Dashboard
- Dynamische Stimmerzeugung
- Sprachausgabe mit anpassbaren Stimmen

---

## Integration ins System

Alle Tools werden automatisch geladen durch das Tool-Loader-System:

1. **Automatische Erkennung**: Alle Python-Dateien mit `TOOL_DECLARATION` werden erkannt
2. **Dynamisches Laden**: Keine Code-Änderungen nötig
3. **Sofort einsatzbereit**: Nach dem Start verfügbar

## API-Schnittstelle aktivieren (Produktion)

Für echte Internet-Daten müssen API-Keys konfiguriert werden:

```python
# config.py
API_KEYS = {
    "google_search": "your-api-key",
    "newsapi": "your-api-key",
    "openweathermap": "your-api-key",
    "alphavantage": "your-api-key"
}
```

## Sicherheitshinweise

1. **Lokaler Zugriff**: Nur erlaubte Verzeichnisse zugänglich
2. **Befehlsfilter**: Gefährliche Commands werden blockiert
3. **URL-Filter**: Bekannte schädliche Domains gesperrt
4. **Timeouts**: Alle externen Requests haben Timeouts

## Nächste Schritte

1. **API-Keys hinzufügen**: Für echte Internet-Daten
2. **Erweiterte Agenten-Rollen**: Eigene Rollen definieren
3. **Custom Tools**: Eigene Tools im `/workspace/actions/` Ordner erstellen
4. **Logging**: Ausführungs-Logs für Debugging aktivieren
5. **Brain Dashboard starten**: `python3 visuals/brain_dashboard.py`

---

**Viel Erfolg beim Erweitern Ihres Jarvis-Systems!**
