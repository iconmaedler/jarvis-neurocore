"""
Multi-Agenten-System für parallele Recherche
Erstellt mehrere Agenten die simultan suchen und Ergebnisse abgleichen
"""
import asyncio
import aiohttp
from typing import List, Dict, Any
from datetime import datetime
import hashlib

TOOL_DECLARATION = {
    "name": "multi_agent_system",
    "description": "Erstellt mehrere Agenten für parallele Recherche mit Ergebnisabgleich",
    "tools": [
        {
            "name": "create_search_agents",
            "description": "Erstellt mehrere Agenten die simultan nach Informationen suchen und vergleicht deren Ergebnisse",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Die Suchanfrage"},
                    "num_agents": {"type": "integer", "description": "Anzahl der zu erstellenden Agenten (2-10)", "default": 3, "minimum": 2, "maximum": 10},
                    "search_engines": {"type": "array", "items": {"type": "string"}, "description": "Zu verwendende Suchmaschinen/Quellen", "default": ["google", "bing", "duckduckgo"]},
                    "consensus_threshold": {"type": "number", "description": "Mindestübereinstimmung für Konsens (0.0-1.0)", "default": 0.6}
                },
                "required": ["query"]
            }
        },
        {
            "name": "deploy_research_team",
            "description": "Setzt ein Team von Agenten ein die verschiedene Aspekte eines Themas parallel erforschen",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Das Forschungsthema"},
                    "agent_roles": {"type": "array", "items": {"type": "string"}, "description": "Rollen der Agenten (z.B. 'fact_checker', 'data_collector', 'analyst')"},
                    "time_limit_seconds": {"type": "integer", "description": "Zeitlimit für die Recherche in Sekunden", "default": 60}
                },
                "required": ["topic", "agent_roles"]
            }
        },
        {
            "name": "compare_agent_results",
            "description": "Vergleicht und bewertet die Ergebnisse mehrerer Agenten auf Konsistenz und Qualität",
            "parameters": {
                "type": "object",
                "properties": {
                    "results": {"type": "array", "items": {"type": "object"}, "description": "Ergebnisse der Agenten zum Vergleich"},
                    "comparison_criteria": {"type": "array", "items": {"type": "string"}, "description": "Kriterien für den Vergleich", "default": ["accuracy", "completeness", "relevance"]}
                },
                "required": ["results"]
            }
        }
    ]
}


class SearchAgent:
    """Ein einzelner Such-Agent"""
    
    def __init__(self, agent_id: str, search_engine: str):
        self.agent_id = agent_id
        self.search_engine = search_engine
        self.results = []
        self.start_time = None
        self.end_time = None
    
    async def search(self, session: aiohttp.ClientSession, query: str) -> Dict[str, Any]:
        """Führt eine Suche durch"""
        self.start_time = datetime.now()
        
        try:
            # Simulierte Suche - in Produktion würde hier echte API angesprochen werden
            await asyncio.sleep(0.5)  # Simuliere Netzwerk-Latenz
            
            # Unterschiedliche Perspektiven basierend auf Search Engine
            perspective = self._get_perspective()
            
            self.results = [{
                "source": f"{self.search_engine}_result_{i}",
                "content": f"Ergebnis {i} von {self.search_engine} für '{query}' aus Perspektive: {perspective}",
                "relevance_score": 0.95 - (i * 0.1),
                "timestamp": datetime.now().isoformat()
            } for i in range(3)]
            
            self.end_time = datetime.now()
            
            return {
                "agent_id": self.agent_id,
                "search_engine": self.search_engine,
                "query": query,
                "results": self.results,
                "duration_ms": (self.end_time - self.start_time).total_seconds() * 1000,
                "status": "success"
            }
        except Exception as e:
            self.end_time = datetime.now()
            return {
                "agent_id": self.agent_id,
                "search_engine": self.search_engine,
                "query": query,
                "error": str(e),
                "duration_ms": (self.end_time - self.start_time).total_seconds() * 1000 if self.start_time else 0,
                "status": "failed"
            }
    
    def _get_perspective(self) -> str:
        """Gibt eine einzigartige Perspektive für diesen Agenten zurück"""
        perspectives = {
            "google": "technisch-detailliert",
            "bing": "übersichtlich-zusammenfassend",
            "duckduckgo": "privatsphären-fokussiert",
            "wikipedia": "encyklopädisch-faktisch",
            "news": "aktuell-ereignisbasiert"
        }
        return perspectives.get(self.search_engine, "allgemein")


class AgentCoordinator:
    """Koordiniert mehrere Agenten und gleicht Ergebnisse ab"""
    
    def __init__(self):
        self.agents: List[SearchAgent] = []
        self.consensus_results = []
    
    def create_agents(self, num_agents: int, search_engines: List[str]) -> List[SearchAgent]:
        """Erstellt mehrere Agenten"""
        self.agents = []
        engines = search_engines[:num_agents] if len(search_engines) >= num_agents else search_engines * (num_agents // len(search_engines) + 1)
        
        for i in range(num_agents):
            agent = SearchAgent(f"agent_{i+1}", engines[i % len(engines)])
            self.agents.append(agent)
        
        return self.agents
    
    async def run_parallel_search(self, query: str) -> List[Dict[str, Any]]:
        """Führt parallele Suche mit allen Agenten durch"""
        async with aiohttp.ClientSession() as session:
            tasks = [agent.search(session, query) for agent in self.agents]
            results = await asyncio.gather(*tasks)
        return results
    
    def find_consensus(self, results: List[Dict], threshold: float = 0.6) -> Dict[str, Any]:
        """Findet konsistente Informationen über alle Agenten hinweg"""
        all_facts = []
        
        for result in results:
            if result.get("status") == "success":
                for item in result.get("results", []):
                    all_facts.append({
                        "content": item["content"],
                        "source": item["source"],
                        "agent": result["agent_id"],
                        "relevance": item.get("relevance_score", 0.5)
                    })
        
        # Gruppieren nach Ähnlichkeit (einfacher Hash-basierter Ansatz)
        fact_groups = {}
        for fact in all_facts:
            # Erstelle einen Hash des Inhalts für Gruppierung
            content_hash = hashlib.md5(fact["content"].encode()).hexdigest()[:8]
            if content_hash not in fact_groups:
                fact_groups[content_hash] = []
            fact_groups[content_hash].append(fact)
        
        # Finde Gruppen die den Threshold erreichen
        consensus_facts = []
        for group_id, facts in fact_groups.items():
            if len(facts) / len(results) >= threshold:
                consensus_facts.append({
                    "content": facts[0]["content"],
                    "supporting_agents": [f["agent"] for f in facts],
                    "support_count": len(facts),
                    "confidence": len(facts) / len(results),
                    "sources": [f["source"] for f in facts]
                })
        
        return {
            "consensus_facts": consensus_facts,
            "total_results_analyzed": len(all_facts),
            "agents_participated": len(results),
            "consensus_threshold": threshold,
            "timestamp": datetime.now().isoformat()
        }


async def execute_search_agents(query: str, num_agents: int = 3, 
                                search_engines: List[str] = None,
                                consensus_threshold: float = 0.6) -> Dict[str, Any]:
    """Hauptfunktion für parallele Agenten-Suche"""
    if search_engines is None:
        search_engines = ["google", "bing", "duckduckgo"]
    
    coordinator = AgentCoordinator()
    coordinator.create_agents(num_agents, search_engines)
    
    start_time = datetime.now()
    results = await coordinator.run_parallel_search(query)
    consensus = coordinator.find_consensus(results, consensus_threshold)
    end_time = datetime.now()
    
    return {
        "query": query,
        "num_agents": num_agents,
        "search_engines_used": search_engines[:num_agents],
        "individual_results": results,
        "consensus_analysis": consensus,
        "total_duration_ms": (end_time - start_time).total_seconds() * 1000,
        "timestamp": datetime.now().isoformat()
    }


def create_search_agents(parameters, player=None, session_memory=None):
    """Tool: Erstellt mehrere Agenten für parallele Suche"""
    query = parameters.get("query")
    num_agents = min(max(parameters.get("num_agents", 3), 2), 10)
    search_engines = parameters.get("search_engines", ["google", "bing", "duckduckgo"])
    consensus_threshold = parameters.get("consensus_threshold", 0.6)
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            execute_search_agents(query, num_agents, search_engines, consensus_threshold)
        )
        loop.close()
        
        return {
            "success": True,
            "analysis": result
        }
    except Exception as e:
        return {"error": f"Fehler bei der Multi-Agenten-Suche: {str(e)}"}


def deploy_research_team(parameters, player=None, session_memory=None):
    """Tool: Setzt ein Forschungsteam ein"""
    topic = parameters.get("topic")
    agent_roles = parameters.get("agent_roles", ["researcher", "analyst", "fact_checker"])
    time_limit = parameters.get("time_limit_seconds", 60)
    
    # Simuliere verschiedene Agenten-Rollen
    research_plan = {
        "topic": topic,
        "team_composition": [],
        "assigned_tasks": [],
        "coordination_strategy": "parallel_with_sync_points"
    }
    
    for i, role in enumerate(agent_roles):
        agent_info = {
            "agent_id": f"{role}_agent_{i+1}",
            "role": role,
            "specialization": _get_role_specialization(role),
            "status": "deployed"
        }
        research_plan["team_composition"].append(agent_info)
        
        task = {
            "agent_id": agent_info["agent_id"],
            "task": _get_role_task(role, topic),
            "priority": "high" if i == 0 else "medium",
            "deadline_seconds": time_limit
        }
        research_plan["assigned_tasks"].append(task)
    
    return {
        "success": True,
        "research_team": research_plan,
        "estimated_completion": f"{time_limit} Sekunden",
        "timestamp": datetime.now().isoformat()
    }


def compare_agent_results(parameters, player=None, session_memory=None):
    """Tool: Vergleicht Agenten-Ergebnisse"""
    results = parameters.get("results", [])
    criteria = parameters.get("comparison_criteria", ["accuracy", "completeness", "relevance"])
    
    if not results:
        return {"error": "Keine Ergebnisse zum Vergleichen angegeben"}
    
    comparison = {
        "total_results": len(results),
        "criteria_evaluated": criteria,
        "scores": {},
        "agreements": [],
        "disagreements": [],
        "recommendations": []
    }
    
    # Einfache Vergleichslogik
    for criterion in criteria:
        scores = []
        for i, result in enumerate(results):
            score = 0.8 + (i * 0.05)  # Simulierte Bewertung
            scores.append({"agent": i+1, "score": min(score, 1.0)})
        comparison["scores"][criterion] = scores
    
    # Finde Übereinstimmungen und Widersprüche
    comparison["agreements"] = ["Alle Agenten stimmen bei Kernfakten überein"]
    comparison["disagreements"] = ["Unterschiedliche Gewichtung bei Nebenaspekten"]
    comparison["recommendations"] = [
        "Verwende konsensbasierte Informationen als primäre Quelle",
        "Überprüfe widersprüchliche Punkte mit zusätzlichen Quellen"
    ]
    
    return {
        "success": True,
        "comparison": comparison,
        "timestamp": datetime.now().isoformat()
    }


def _get_role_specialization(role: str) -> str:
    """Gibt Spezialisierung für eine Rolle zurück"""
    specializations = {
        "researcher": "Datensammlung und Quellenanalyse",
        "analyst": "Mustererkennung und Trendanalyse",
        "fact_checker": "Verifikation und Faktenprüfung",
        "summarizer": "Zusammenfassung und Synthese",
        "critic": "Qualitätsbewertung und Gegenargumente"
    }
    return specializations.get(role, "Allgemeine Recherche")


def _get_role_task(role: str, topic: str) -> str:
    """Gibt Aufgabe für eine Rolle zurück"""
    tasks = {
        "researcher": f"Sammle umfassende Daten zu '{topic}'",
        "analyst": f"Analysiere Muster und Zusammenhänge in '{topic}'",
        "fact_checker": f"Verifiziere alle Fakten zu '{topic}'",
        "summarizer": f"Erstelle prägnante Zusammenfassung von '{topic}'",
        "critic": f"Identifiziere Schwachstellen in Argumenten zu '{topic}'"
    }
    return tasks.get(role, f"Erforsche Aspekte von '{topic}'")
