#!/bin/bash

# 🚀 Jarvis AI - One-Click Installation Script
# Dieses Skript installiert alle Abhängigkeiten und startet das System

set -e  # Bei Fehlern abbrechen

echo "🤖 =========================================="
echo "🤖   JARVIS AI - One-Click Installation"
echo "🤖 =========================================="
echo ""

# Farben für Ausgabe
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Prüfen ob Python 3.10+ installiert ist
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 ist nicht installiert!${NC}"
    echo "Bitte installieren Sie Python 3.10 oder höher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${BLUE}✓ Python Version: $PYTHON_VERSION${NC}"

# Virtuelle Umgebung erstellen oder aktivieren
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Erstelle virtuelle Umgebung...${NC}"
    python3 -m venv venv
fi

echo -e "${BLUE}✓ Aktiviere virtuelle Umgebung${NC}"
source venv/bin/activate

# Abhängigkeiten installieren
echo -e "${YELLOW}📦 Installiere Abhängigkeiten...${NC}"

# requirements.txt erstellen falls nicht vorhanden
if [ ! -f "requirements.txt" ]; then
    cat > requirements.txt << EOF
flask>=2.3.0
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
numpy>=1.24.0
pillow>=10.0.0
pyautogui>=0.9.54
python-dotenv>=1.0.0
colorama>=0.4.6
EOF
fi

pip install --upgrade pip
pip install -r requirements.txt

echo -e "${GREEN}✓ Alle Abhängigkeiten installiert${NC}"

# Konfiguration erstellen
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚙️  Erstelle Konfigurationsdatei...${NC}"
    cat > .env << EOF
# Jarvis AI Konfiguration
# Tragen Sie hier Ihre API-Keys ein

# OpenAI (für Sprachmodell und Stimme)
OPENAI_API_KEY=your_openai_api_key_here

# Google Search API (optional für Websuche)
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_CX=your_google_cx_here

# Wetter API (optional)
OPENWEATHER_API_KEY=your_weather_api_key_here

# News API (optional)
NEWS_API_KEY=your_news_api_key_here

# System Einstellungen
JARVIS_NAME="Jarvis"
DEFAULT_VOICE="alloy"
SPEECH_RATE=1.0
DEBUG_MODE=false
EOF
    echo -e "${GREEN}✓ .env Datei erstellt - Bitte API-Keys eintragen!${NC}"
else
    echo -e "${BLUE}✓ .env Datei existiert bereits${NC}"
fi

# Verzeichnisstruktur prüfen
echo -e "${BLUE}✓ Überprüfe Projektstruktur...${NC}"

# Start-Skript erstellen
if [ ! -f "start_jarvis.sh" ]; then
    cat > start_jarvis.sh << 'SCRIPT'
#!/bin/bash
source venv/bin/activate
echo "🚀 Starte Jarvis AI..."
echo "🧠 NeuroCore 3D Brain: http://localhost:5000"
echo ""
python3 visuals/brain_dashboard.py &
sleep 2
python3 main.py
SCRIPT
    chmod +x start_jarvis.sh
    echo -e "${GREEN}✓ Start-Skript erstellt${NC}"
fi

echo ""
echo -e "${GREEN}=========================================="
echo -e "${GREEN}   Installation erfolgreich abgeschlossen!"
echo -e "${GREEN}==========================================${NC}"
echo ""
echo -e "${YELLOW}Nächste Schritte:${NC}"
echo "1. Trage deine API-Keys in die .env Datei ein"
echo "2. Starte Jarvis mit: ./start_jarvis.sh"
echo "3. Öffne das 3D-Gehirn Dashboard: http://localhost:5000"
echo ""
echo -e "${BLUE}Viel Spaß mit deinem KI-Assistenten! 🤖${NC}"
echo ""

# Optional: Direkt starten wenn gewünscht
read -p "Jarvis jetzt starten? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    ./start_jarvis.sh
fi
