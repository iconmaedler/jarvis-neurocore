# 🧠 Jarvis NeuroCore - 3D Gehirn Visualisierung

## Übersicht
Das NeuroCore-Modul simuliert ein lernendes neuronales Netzwerk und visualisiert es in Echtzeit als 3D-Modell im Browser.

## Features

### Neuronales Netzwerk
- **50 Neuronen** in 3D-Raum kugelförmig angeordnet
- **200+ Synapsen** verbinden die Neuronen
- **Hebb'sche Lernregel**: "Neurons that fire together, wire together"
- **4 Gehirnregionen**: Logic, Memory, Creativity, Learning

### 3D Visualisierung
- **Three.js** für WebGL Rendering
- **Interaktive Darstellung** mit rotierenden Neuronen
- **Farbcodierung** basierend auf Aktivitätslevel
- **Synapsen-Linien** zeigen Verbindungen und Signalübertragung
- **Sanfte Kamerabewegung** für bessere Übersicht

### Echtzeit-Statistiken
- Anzahl aktiver Neuronen
- Gesamtanzahl der Synapsen
- Verarbeitete Gedanken
- Wissensstand (lernt kontinuierlich)
- Aktivität der Gehirnregionen als Balkendiagramme

## Starten

```bash
cd /workspace
python3 visuals/brain_dashboard.py
```

Das Dashboard startet auf **http://localhost:5000**

## API Endpoints

### GET /api/brain-state
Gibt den aktuellen Zustand des Gehirns zurück:
```json
{
  "neurons": [...],
  "synapses": [...],
  "regions": {
    "logic": 0.45,
    "memory": 0.32,
    "creativity": 0.67,
    "learning": 0.89
  },
  "stats": {
    "total_neurons": 50,
    "total_synapses": 259,
    "thoughts": 142,
    "knowledge_level": 12.45
  }
}
```

### POST /api/think
Löst einen neuen Denkprozess aus.

## Integration ins Hauptsystem

Das NeuroCore-Modul kann einfach ins Jarvis-Hauptsystem integriert werden:

```python
from brain.neuro_core import get_brain

brain = get_brain()

# Bei jeder Aufgabe das Gehirn nutzen
result = brain.process_task("Beschreibe die Aufgabe hier")
print(f"Aktive Neuronen: {result['active_neurons']}")
```

## Automatisches Lernen

Das Gehirn lernt automatisch bei jedem Denkprozess:
- Synapsen zwischen gleichzeitig aktiven Neuronen werden gestärkt
- Der Wissensstand steigt kontinuierlich
- Gehirnregionen werden je nach Aufgabentyp unterschiedlich aktiviert

## Technische Details

- **Python Backend**: Flask Server mit NeuroCore-Engine
- **Frontend**: HTML5 + Three.js für 3D-Grafik
- **Aktualisierungsrate**: 2 Sekunden für Daten, 60 FPS für Animation
- **Automatisches Denken**: Alle 5 Sekunden ein Hintergrundgedanke

## Anpassung

Anzahl der Neuronen ändern in `brain/neuro_core.py`:
```python
brain = NeuroCore(num_neurons=100)  # Statt 50
```

Lernrate anpassen:
```python
self.learning_rate = 0.05  # Höher = schnelleres Lernen
```

## Visualisierungsdetails

### Neuronen-Farben
- **Blau**: Niedrige Aktivität
- **Cyan/Türkis**: Mittlere Aktivität  
- **Weiß/Hellblau**: Hohe Aktivität (feuert!)

### Synapsen-Farben
- **Schwach sichtbar**: Keine aktuelle Aktivität
- **Hell leuchtend**: Starke Signalübertragung

### Gehirnregionen
- **Logic (Rot)**: Analytische Aufgaben
- **Memory (Türkis)**: Erinnerungsprozesse
- **Creativity (Lila)**: Kreative Lösungen
- **Learning (Gelb)**: Lernprozesse
