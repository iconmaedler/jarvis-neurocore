"""
Lokale System-Tools für Jarvis
Bietet Zugriff auf Dateisystem, Terminal und System-Informationen
"""
import os
import subprocess
import platform
import shutil
from pathlib import Path
from datetime import datetime

TOOL_DECLARATION = {
    "name": "local_system_tools",
    "description": "Zugriff auf lokalen Computer: Dateien lesen/schreiben, Terminal-Befehle ausführen, System-Infos abrufen",
    "tools": [
        {
            "name": "read_file",
            "description": "Liest den Inhalt einer Datei vom lokalen System",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Pfad zur Datei (absolut oder relativ)"},
                    "encoding": {"type": "string", "description": "Datei-Encoding (default: utf-8)", "default": "utf-8"}
                },
                "required": ["file_path"]
            }
        },
        {
            "name": "write_file",
            "description": "Schreibt Inhalt in eine Datei (erstellt Verzeichnisse bei Bedarf)",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Pfad zur Datei"},
                    "content": {"type": "string", "description": "Zu schreibender Inhalt"},
                    "mode": {"type": "string", "description": "Schreibmodus: 'write' (überschreiben) oder 'append' (anhängen)", "enum": ["write", "append"], "default": "write"}
                },
                "required": ["file_path", "content"]
            }
        },
        {
            "name": "list_directory",
            "description": "Listet alle Dateien und Verzeichnisse in einem Ordner auf",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory_path": {"type": "string", "description": "Pfad zum Verzeichnis"},
                    "recursive": {"type": "boolean", "description": "Ob rekursiv alle Unterordner durchsucht werden sollen", "default": False}
                },
                "required": ["directory_path"]
            }
        },
        {
            "name": "execute_command",
            "description": "Führt einen Terminal-Befehl aus und gibt die Ausgabe zurück",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Der auszuführende Befehl"},
                    "working_directory": {"type": "string", "description": "Arbeitsverzeichnis für die Ausführung", "default": "."},
                    "timeout": {"type": "integer", "description": "Timeout in Sekunden (default: 30)", "default": 30}
                },
                "required": ["command"]
            }
        },
        {
            "name": "get_system_info",
            "description": "Ruft System-Informationen ab (CPU, RAM, OS, etc.)",
            "parameters": {
                "type": "object",
                "properties": {
                    "info_type": {"type": "string", "description": "Art der Information: 'all', 'os', 'hardware', 'disk'", "enum": ["all", "os", "hardware", "disk"], "default": "all"}
                }
            }
        },
        {
            "name": "search_files",
            "description": "Sucht nach Dateien anhand eines Musters im Dateisystem",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "Suchmuster (z.B. '*.py', 'config*')"},
                    "search_path": {"type": "string", "description": "Startverzeichnis für die Suche", "default": "."},
                    "max_results": {"type": "integer", "description": "Maximale Anzahl an Ergebnissen", "default": 50}
                },
                "required": ["pattern"]
            }
        }
    ]
}


def read_file(parameters, player=None, session_memory=None):
    """Liest den Inhalt einer Datei"""
    file_path = parameters.get("file_path")
    encoding = parameters.get("encoding", "utf-8")
    
    try:
        path = Path(file_path).expanduser().resolve()
        
        # Sicherheitscheck: Verhindere Zugriff außerhalb des Home-Verzeichnisses
        home = Path.home()
        try:
            path.relative_to(home)
        except ValueError:
            # Erlaube auch /workspace und aktuelle Arbeitsverzeichnisse
            if not str(path).startswith("/workspace") and not str(path).startswith(os.getcwd()):
                return {"error": f"Zugriff verweigert: Datei liegt außerhalb erlaubter Bereiche ({path})"}
        
        if not path.exists():
            return {"error": f"Datei nicht gefunden: {path}"}
        
        if not path.is_file():
            return {"error": f"Pfad ist keine Datei: {path}"}
        
        content = path.read_text(encoding=encoding)
        return {
            "success": True,
            "file_path": str(path),
            "size_bytes": len(content),
            "content": content
        }
    except Exception as e:
        return {"error": f"Fehler beim Lesen der Datei: {str(e)}"}


def write_file(parameters, player=None, session_memory=None):
    """Schreibt Inhalt in eine Datei"""
    file_path = parameters.get("file_path")
    content = parameters.get("content")
    mode = parameters.get("mode", "write")
    
    try:
        path = Path(file_path).expanduser().resolve()
        
        # Sicherheitscheck
        home = Path.home()
        if not str(path).startswith(str(home)) and not str(path).startswith("/workspace") and not str(path).startswith(os.getcwd()):
            return {"error": f"Zugriff verweigert: Datei liegt außerhalb erlaubter Bereiche ({path})"}
        
        # Erstelle Verzeichnis falls nötig
        path.parent.mkdir(parents=True, exist_ok=True)
        
        write_mode = "a" if mode == "append" else "w"
        with open(path, write_mode, encoding="utf-8") as f:
            f.write(content)
        
        return {
            "success": True,
            "file_path": str(path),
            "action": "created" if mode == "write" else "appended",
            "bytes_written": len(content)
        }
    except Exception as e:
        return {"error": f"Fehler beim Schreiben der Datei: {str(e)}"}


def list_directory(parameters, player=None, session_memory=None):
    """Listet Verzeichnisinhalt auf"""
    directory_path = parameters.get("directory_path", ".")
    recursive = parameters.get("recursive", False)
    
    try:
        path = Path(directory_path).expanduser().resolve()
        
        if not path.exists():
            return {"error": f"Verzeichnis nicht gefunden: {path}"}
        
        if not path.is_dir():
            return {"error": f"Pfad ist kein Verzeichnis: {path}"}
        
        items = []
        if recursive:
            for item in path.rglob("*"):
                rel_path = item.relative_to(path)
                items.append({
                    "name": item.name,
                    "path": str(item),
                    "relative_path": str(rel_path),
                    "type": "directory" if item.is_dir() else "file",
                    "size": item.stat().st_size if item.is_file() else None
                })
        else:
            for item in path.iterdir():
                items.append({
                    "name": item.name,
                    "path": str(item),
                    "type": "directory" if item.is_dir() else "file",
                    "size": item.stat().st_size if item.is_file() else None
                })
        
        return {
            "success": True,
            "directory": str(path),
            "count": len(items),
            "items": items
        }
    except Exception as e:
        return {"error": f"Fehler beim Listen des Verzeichnisses: {str(e)}"}


def execute_command(parameters, player=None, session_memory=None):
    """Führt Terminal-Befehl aus"""
    command = parameters.get("command")
    working_directory = parameters.get("working_directory", ".")
    timeout = parameters.get("timeout", 30)
    
    # Sicherheitsfilter für gefährliche Befehle
    dangerous_patterns = ["rm -rf /", "mkfs", "dd if=", ":(){:|:&}", "> /dev/sda"]
    for pattern in dangerous_patterns:
        if pattern in command:
            return {"error": f"Befehl blockiert aus Sicherheitsgründen: Enthält '{pattern}'"}
    
    try:
        cwd = Path(working_directory).expanduser().resolve()
        if not cwd.exists():
            return {"error": f"Arbeitsverzeichnis nicht gefunden: {cwd}"}
        
        result = subprocess.run(
            command,
            shell=True,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        return {
            "success": True,
            "command": command,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "execution_time_ms": result.elapsed.total_seconds() * 1000 if hasattr(result, 'elapsed') else None
        }
    except subprocess.TimeoutExpired:
        return {"error": f"Befehl-Timeout nach {timeout} Sekunden"}
    except Exception as e:
        return {"error": f"Fehler bei der Befehlsausführung: {str(e)}"}


def get_system_info(parameters, player=None, session_memory=None):
    """Ruft System-Informationen ab"""
    info_type = parameters.get("info_type", "all")
    
    try:
        info = {}
        
        if info_type in ["all", "os"]:
            info["os"] = {
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
                "python_version": platform.python_version(),
                "hostname": platform.node()
            }
        
        if info_type in ["all", "hardware"]:
            # CPU Info
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    cpu_lines = f.readlines()
                    cpu_info = {}
                    for line in cpu_lines:
                        if ':' in line:
                            key, value = line.split(':', 1)
                            if key.strip() == 'model name':
                                cpu_info['model'] = value.strip()
                                break
                    info["cpu"] = cpu_info
            except:
                info["cpu"] = {"available": False}
            
            # RAM Info
            try:
                with open('/proc/meminfo', 'r') as f:
                    mem_lines = f.readlines()
                    mem_info = {}
                    for line in mem_lines[:3]:
                        if ':' in line:
                            key, value = line.split(':', 1)
                            mem_info[key.strip()] = value.strip()
                    info["memory"] = mem_info
            except:
                info["memory"] = {"available": False}
        
        if info_type in ["all", "disk"]:
            disk_usage = shutil.disk_usage("/")
            info["disk"] = {
                "total_gb": round(disk_usage.total / (1024**3), 2),
                "used_gb": round(disk_usage.used / (1024**3), 2),
                "free_gb": round(disk_usage.free / (1024**3), 2),
                "percent_used": round((disk_usage.used / disk_usage.total) * 100, 2)
            }
        
        info["timestamp"] = datetime.now().isoformat()
        
        return {"success": True, "info": info}
    except Exception as e:
        return {"error": f"Fehler beim Abrufen der System-Infos: {str(e)}"}


def search_files(parameters, player=None, session_memory=None):
    """Sucht nach Dateien im Dateisystem"""
    pattern = parameters.get("pattern")
    search_path = parameters.get("search_path", ".")
    max_results = parameters.get("max_results", 50)
    
    try:
        path = Path(search_path).expanduser().resolve()
        if not path.exists():
            return {"error": f"Suchpfad nicht gefunden: {path}"}
        
        results = []
        for file in path.rglob(pattern):
            if len(results) >= max_results:
                break
            results.append({
                "name": file.name,
                "path": str(file),
                "relative_path": str(file.relative_to(path)),
                "type": "directory" if file.is_dir() else "file",
                "size": file.stat().st_size if file.is_file() else None
            })
        
        return {
            "success": True,
            "pattern": pattern,
            "search_path": str(path),
            "count": len(results),
            "results": results
        }
    except Exception as e:
        return {"error": f"Fehler bei der Dateisuche: {str(e)}"}
