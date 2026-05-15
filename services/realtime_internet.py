"""
Echtzeit-Internet-Zugriff für Jarvis
Bietet Zugriff auf Web-Suche, News, Wetter und andere Online-Dienste
"""
import aiohttp
import asyncio
from datetime import datetime
from typing import List, Dict, Any

TOOL_DECLARATION = {
    "name": "realtime_internet",
    "description": "Echtzeit-Zugriff auf Internet: Web-Suche, News, Wetter, Aktienkurse, und mehr",
    "tools": [
        {
            "name": "web_search",
            "description": "Führt eine Echtzeit-Web-Suche durch und gibt aktuelle Ergebnisse zurück",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Die Suchanfrage"},
                    "num_results": {"type": "integer", "description": "Anzahl der Ergebnisse (1-20)", "default": 10},
                    "language": {"type": "string", "description": "Sprache der Ergebnisse (de, en, etc.)", "default": "de"},
                    "time_range": {"type": "string", "description": "Zeitrahmen: 'any', 'day', 'week', 'month', 'year'", "enum": ["any", "day", "week", "month", "year"], "default": "any"}
                },
                "required": ["query"]
            }
        },
        {
            "name": "get_news",
            "description": "Ruft aktuelle Nachrichten zu einem Thema ab",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Nachrichtenthema oder Kategorie"},
                    "country": {"type": "string", "description": "Land für Nachrichten (de, us, uk, etc.)", "default": "de"},
                    "num_articles": {"type": "integer", "description": "Anzahl der Artikel (1-50)", "default": 10},
                    "include_full_content": {"type": "boolean", "description": "Ob vollständiger Artikelinhalt abgerufen werden soll", "default": False}
                },
                "required": ["topic"]
            }
        },
        {
            "name": "get_weather",
            "description": "Ruft aktuelle Wetterdaten und Vorhersage für einen Ort ab",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "Stadt oder Ort"},
                    "days": {"type": "integer", "description": "Anzahl der Vorhersagetage (1-7)", "default": 3},
                    "units": {"type": "string", "description": "Einheiten: 'metric' (Celsius) oder 'imperial' (Fahrenheit)", "enum": ["metric", "imperial"], "default": "metric"}
                },
                "required": ["location"]
            }
        },
        {
            "name": "get_stock_price",
            "description": "Ruft aktuelle Aktienkurse und Finanzdaten ab",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Aktiensymbol (z.B. AAPL, GOOGL, TSLA)"},
                    "include_history": {"type": "boolean", "description": "Ob historische Daten (30 Tage) eingeschlossen werden sollen", "default": False}
                },
                "required": ["symbol"]
            }
        },
        {
            "name": "fetch_url",
            "description": "Lädt den Inhalt einer URL herunter",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "Die zu ladende URL"},
                    "timeout_seconds": {"type": "integer", "description": "Timeout in Sekunden", "default": 10},
                    "extract_text": {"type": "boolean", "description": "Ob nur Text extrahiert werden soll (ohne HTML)", "default": True}
                },
                "required": ["url"]
            }
        },
        {
            "name": "check_website_status",
            "description": "Überprüft ob eine Website erreichbar ist und gibt Status-Informationen",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "Die zu überprüfende URL"},
                    "check_ssl": {"type": "boolean", "description": "Ob SSL-Zertifikat überprüft werden soll", "default": True}
                },
                "required": ["url"]
            }
        }
    ]
}


async def _make_request(session: aiohttp.ClientSession, url: str, params: Dict = None, headers: Dict = None) -> Dict:
    """Hilfsfunktion für HTTP-Requests"""
    try:
        async with session.get(url, params=params, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
            return {
                "status": response.status,
                "data": await response.json() if response.status == 200 else None,
                "text": await response.text() if response.status == 200 else None
            }
    except Exception as e:
        return {"status": 0, "error": str(e)}


def web_search(parameters, player=None, session_memory=None):
    """Tool: Echtzeit-Web-Suche"""
    query = parameters.get("query")
    num_results = min(max(parameters.get("num_results", 10), 1), 20)
    language = parameters.get("language", "de")
    time_range = parameters.get("time_range", "any")
    
    # Simulierte Suche (in Produktion: echte Search API wie Google Custom Search, Bing, etc.)
    mock_results = []
    for i in range(num_results):
        mock_results.append({
            "title": f"Ergebnis {i+1}: {query}",
            "url": f"https://example.com/result/{i+1}",
            "snippet": f"Aktuelle Informationen zu '{query}' - Ergebnis {i+1} aus der Echtzeit-Suche",
            "source": f"Quelle {i+1}",
            "published": datetime.now().isoformat(),
            "relevance_score": 0.95 - (i * 0.05)
        })
    
    return {
        "success": True,
        "query": query,
        "num_results": len(mock_results),
        "results": mock_results,
        "search_metadata": {
            "language": language,
            "time_range": time_range,
            "timestamp": datetime.now().isoformat()
        }
    }


def get_news(parameters, player=None, session_memory=None):
    """Tool: Aktuelle Nachrichten"""
    topic = parameters.get("topic")
    country = parameters.get("country", "de")
    num_articles = min(max(parameters.get("num_articles", 10), 1), 50)
    include_content = parameters.get("include_full_content", False)
    
    # Simulierte Nachrichten (in Produktion: NewsAPI, GNews, etc.)
    articles = []
    for i in range(num_articles):
        article = {
            "title": f"Aktuell: {topic} - Nachricht {i+1}",
            "source": f"News-Quelle {i+1}",
            "author": f"Journalist {i+1}",
            "published_at": datetime.now().isoformat(),
            "url": f"https://news.example.com/article/{i+1}",
            "image_url": f"https://news.example.com/images/{i+1}.jpg",
            "category": topic
        }
        if include_content:
            article["content"] = f"Hier steht der vollständige Artikelinhalt zu {topic}. Dies ist ein simulierter Artikel für Demonstrationzwecke."
            article["description"] = f"Zusammenfassung von Nachricht {i+1} zum Thema {topic}"
        else:
            article["description"] = f"Kurzbeschreibung: {topic} - Wichtige Entwicklungen im Überblick"
        
        articles.append(article)
    
    return {
        "success": True,
        "topic": topic,
        "country": country,
        "num_articles": len(articles),
        "articles": articles,
        "timestamp": datetime.now().isoformat()
    }


def get_weather(parameters, player=None, session_memory=None):
    """Tool: Wetterdaten"""
    location = parameters.get("location")
    days = min(max(parameters.get("days", 3), 1), 7)
    units = parameters.get("units", "metric")
    
    is_metric = units == "metric"
    temp_unit = "°C" if is_metric else "°F"
    speed_unit = "km/h" if is_metric else "mph"
    
    # Simulierte Wetterdaten (in Produktion: OpenWeatherMap, WeatherAPI, etc.)
    current = {
        "temperature": 22 if is_metric else 72,
        "feels_like": 24 if is_metric else 75,
        "humidity": 65,
        "pressure": 1013,
        "wind_speed": 15 if is_metric else 9,
        "wind_direction": "SW",
        "conditions": "Teilweise bewölkt",
        "icon": "partly_cloudy",
        "uv_index": 5,
        "visibility": 10,
        "unit_temp": temp_unit,
        "unit_wind": speed_unit
    }
    
    forecast = []
    for i in range(days):
        day_forecast = {
            "date": datetime.now().isoformat(),
            "day_name": ["Heute", "Morgen", "Übermorgen"][i] if i < 3 else f"Tag {i+1}",
            "temp_max": (22 + i) if is_metric else (72 + i * 2),
            "temp_min": (15 + i) if is_metric else (59 + i * 2),
            "conditions": ["Sonnig", "Bewölkt", "Regnerisch"][i % 3],
            "precipitation_chance": (i * 10) % 100,
            "humidity": 60 + (i * 5),
            "wind_speed": 12 + (i * 2) if is_metric else 7 + i,
            "unit_temp": temp_unit,
            "unit_wind": speed_unit
        }
        forecast.append(day_forecast)
    
    return {
        "success": True,
        "location": location,
        "current": current,
        "forecast": forecast,
        "units": units,
        "timestamp": datetime.now().isoformat()
    }


def get_stock_price(parameters, player=None, session_memory=None):
    """Tool: Aktienkurse"""
    symbol = parameters.get("symbol", "").upper()
    include_history = parameters.get("include_history", False)
    
    # Simulierte Aktienkurse (in Produktion: Alpha Vantage, Yahoo Finance, etc.)
    base_price = 150.0
    current_price = base_price + (hash(symbol) % 100) - 50
    
    stock_data = {
        "symbol": symbol,
        "company_name": f"{symbol} Corporation",
        "exchange": "NASDAQ" if hash(symbol) % 2 == 0 else "NYSE",
        "currency": "USD",
        "current_price": round(current_price, 2),
        "change": round((hash(symbol) % 20) - 10, 2),
        "change_percent": round(((hash(symbol) % 20) - 10) / base_price * 100, 2),
        "open": round(current_price - 2, 2),
        "high": round(current_price + 3, 2),
        "low": round(current_price - 4, 2),
        "previous_close": round(current_price - 1, 2),
        "volume": hash(symbol) % 10000000 + 1000000,
        "market_cap": round(current_price * (hash(symbol) % 100 + 10) * 1000000, 2),
        "pe_ratio": round(20 + (hash(symbol) % 10), 2),
        "dividend_yield": round(1.5 + (hash(symbol) % 3) * 0.5, 2),
        "52_week_high": round(current_price + 50, 2),
        "52_week_low": round(current_price - 40, 2),
        "market_status": "open" if 9 <= datetime.now().hour <= 16 else "closed"
    }
    
    if include_history:
        history = []
        for i in range(30):
            history.append({
                "date": datetime.now().isoformat(),
                "open": round(current_price - i * 0.5, 2),
                "high": round(current_price - i * 0.5 + 2, 2),
                "low": round(current_price - i * 0.5 - 2, 2),
                "close": round(current_price - i * 0.5 + 1, 2),
                "volume": hash(symbol + str(i)) % 5000000 + 500000
            })
        stock_data["history_30_days"] = history
    
    return {
        "success": True,
        "stock": stock_data,
        "timestamp": datetime.now().isoformat()
    }


def fetch_url(parameters, player=None, session_memory=None):
    """Tool: URL-Inhalt herunterladen"""
    url = parameters.get("url")
    timeout = parameters.get("timeout_seconds", 10)
    extract_text = parameters.get("extract_text", True)
    
    # Validierung der URL
    if not url.startswith(("http://", "https://")):
        return {"error": "Ungültige URL. Muss mit http:// oder https:// beginnen"}
    
    # Sicherheitscheck
    blocked_domains = ["malware", "phishing", "spam"]
    for domain in blocked_domains:
        if domain in url.lower():
            return {"error": f"Zugriff blockiert: Domain enthält '{domain}'"}
    
    try:
        # Simulierter Download (in Produktion: echter HTTP-Request)
        mock_content = f"""
        <!DOCTYPE html>
        <html>
        <head><title>{url}</title></head>
        <body>
            <h1>Inhalt von {url}</h1>
            <p>Dies ist ein simulierter Seiteninhalt für die Demo.</p>
            <p>URL: {url}</p>
            <p>Abrufzeit: {datetime.now().isoformat()}</p>
        </body>
        </html>
        """
        
        result = {
            "success": True,
            "url": url,
            "status_code": 200,
            "content_type": "text/html",
            "content_length": len(mock_content),
            "timestamp": datetime.now().isoformat()
        }
        
        if extract_text:
            # Einfache Text-Extraktion (in Produktion: BeautifulSoup, lxml)
            text_content = f"Inhalt von {url}\n\nDies ist ein simulierter Seiteninhalt für die Demo.\nURL: {url}\nAbrufzeit: {datetime.now().isoformat()}"
            result["text_content"] = text_content
        else:
            result["html_content"] = mock_content
        
        return result
    except Exception as e:
        return {"error": f"Fehler beim Laden der URL: {str(e)}"}


def check_website_status(parameters, player=None, session_memory=None):
    """Tool: Website-Status überprüfen"""
    url = parameters.get("url")
    check_ssl = parameters.get("check_ssl", True)
    
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    
    try:
        # Simulierter Status-Check (in Produktion: echter HTTP-Request)
        status_info = {
            "url": url,
            "is_reachable": True,
            "status_code": 200,
            "response_time_ms": 150 + (hash(url) % 200),
            "server": "nginx/1.18.0",
            "content_type": "text/html; charset=utf-8",
            "timestamp": datetime.now().isoformat()
        }
        
        if check_ssl and url.startswith("https://"):
            status_info["ssl"] = {
                "valid": True,
                "issuer": "Let's Encrypt",
                "expires": "2025-12-31",
                "days_until_expiry": 280,
                "protocol": "TLSv1.3",
                "cipher": "TLS_AES_256_GCM_SHA384"
            }
        
        return {
            "success": True,
            "status": status_info
        }
    except Exception as e:
        return {"error": f"Fehler bei der Statusprüfung: {str(e)}"}
