"""
NeuroCore - Neuronales Netzwerk Gehirn für Jarvis
Simuliert ein lernendes neuronales Netz mit 3D-Visualisierung
"""

import numpy as np
import time
import threading
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
import json

@dataclass
class Neuron:
    id: int
    x: float
    y: float
    z: float
    activation: float = 0.0
    bias: float = 0.0
    connections: List[int] = field(default_factory=list)
    
    def fire(self) -> float:
        """Neuron feuert und gibt Aktivität zurück"""
        self.activation = max(0, self.activation + np.random.uniform(0.1, 0.3))
        return self.activation

@dataclass
class Synapse:
    from_neuron: int
    to_neuron: int
    weight: float
    activity: float = 0.0
    
    def transmit(self, signal: float) -> float:
        """Signal übertragen"""
        self.activity = signal * self.weight
        return self.activity

class NeuroCore:
    """Das künstliche Gehirn von Jarvis"""
    
    def __init__(self, num_neurons: int = 50):
        self.neurons: Dict[int, Neuron] = {}
        self.synapses: List[Synapse] = []
        self.learning_rate = 0.01
        self.total_thoughts = 0
        self.knowledge_level = 0.0
        self.active_regions: Dict[str, float] = {
            'logic': 0.0,
            'memory': 0.0,
            'creativity': 0.0,
            'learning': 0.0
        }
        
        self._initialize_brain(num_neurons)
        self._lock = threading.Lock()
        
    def _initialize_brain(self, num_neurons: int):
        """Initialisiere das neuronale Netzwerk"""
        # Erstelle Neuronen in 3D-Raum (kugelförmig angeordnet)
        for i in range(num_neurons):
            # Kugelkoordinaten für gleichmäßige Verteilung
            phi = np.arccos(-1 + (2 * i) / num_neurons)
            theta = np.sqrt(num_neurons * np.pi) * phi
            
            radius = 10 + np.random.uniform(-2, 2)
            x = radius * np.sin(phi) * np.cos(theta)
            y = radius * np.sin(phi) * np.sin(theta)
            z = radius * np.cos(phi)
            
            self.neurons[i] = Neuron(id=i, x=x, y=y, z=z)
        
        # Verbinde Neuronen (jedes Neuron mit 3-7 zufälligen Nachbarn)
        for neuron_id, neuron in self.neurons.items():
            num_connections = np.random.randint(3, 8)
            possible_targets = [n for n in self.neurons.keys() if n != neuron_id]
            targets = np.random.choice(possible_targets, 
                                     size=min(num_connections, len(possible_targets)), 
                                     replace=False)
            
            for target in targets:
                weight = np.random.uniform(-1, 1)
                self.synapses.append(Synapse(
                    from_neuron=neuron_id,
                    to_neuron=target,
                    weight=weight
                ))
                neuron.connections.append(target)
    
    def think(self, task_complexity: float = 0.5) -> Dict:
        """Führe einen Denkprozess durch"""
        with self._lock:
            self.total_thoughts += 1
            
            # Aktiviere zufällige Neuronen basierend auf Aufgabenkomplexität
            num_active = int(len(self.neurons) * task_complexity)
            active_neurons = np.random.choice(
                list(self.neurons.keys()), 
                size=num_active, 
                replace=False
            )
            
            # Feuere aktive Neuronen
            total_activity = 0
            for neuron_id in active_neurons:
                activity = self.neurons[neuron_id].fire()
                total_activity += activity
                
                # Übertrage Signale durch Synapsen
                for synapse in self.synapses:
                    if synapse.from_neuron == neuron_id:
                        signal = synapse.transmit(activity)
                        if synapse.to_neuron in self.neurons:
                            self.neurons[synapse.to_neuron].activation += signal
            
            # Lerne aus dem Prozess (Hebb'sche Lernregel)
            self._learn(active_neurons)
            
            # Aktualisiere Gehirnregionen
            self._update_regions(task_complexity)
            
            return {
                'active_neurons': len(active_neurons),
                'total_activity': total_activity,
                'thoughts': self.total_thoughts,
                'knowledge': self.knowledge_level
            }
    
    def _learn(self, active_neurons: np.ndarray):
        """Stärke Verbindungen zwischen aktiven Neuronen"""
        for synapse in self.synapses:
            if synapse.from_neuron in active_neurons and synapse.to_neuron in active_neurons:
                # Hebb'sche Lernregel: "Neurons that fire together, wire together"
                synapse.weight += self.learning_rate * np.random.uniform(0.01, 0.05)
                synapse.weight = np.clip(synapse.weight, -2, 2)
        
        self.knowledge_level += 0.001 * len(active_neurons)
    
    def _update_regions(self, complexity: float):
        """Aktualisiere die Aktivität der Gehirnregionen"""
        self.active_regions['logic'] = np.clip(self.active_regions['logic'] + complexity * 0.1, 0, 1)
        self.active_regions['memory'] = np.clip(self.active_regions['memory'] + 0.05, 0, 1)
        self.active_regions['creativity'] = np.clip(self.active_regions['creativity'] + np.random.uniform(0, 0.1), 0, 1)
        self.active_regions['learning'] = np.clip(self.active_regions['learning'] + 0.02, 0, 1)
        
        # Langsamer Abbau der Aktivität
        for region in self.active_regions:
            self.active_regions[region] *= 0.95
    
    def get_state(self) -> Dict:
        """Gib den aktuellen Gehirnzustand zurück"""
        with self._lock:
            neurons_data = []
            for neuron in self.neurons.values():
                neurons_data.append({
                    'id': int(neuron.id),
                    'x': float(neuron.x),
                    'y': float(neuron.y),
                    'z': float(neuron.z),
                    'activation': float(neuron.activation),
                    'connections': [int(c) for c in neuron.connections]
                })
            
            synapses_data = []
            for synapse in self.synapses[:100]:  # Nur erste 100 für Performance
                synapses_data.append({
                    'from': int(synapse.from_neuron),
                    'to': int(synapse.to_neuron),
                    'weight': float(synapse.weight),
                    'activity': float(synapse.activity)
                })
            
            return {
                'neurons': neurons_data,
                'synapses': synapses_data,
                'regions': {k: float(v) for k, v in self.active_regions.items()},
                'stats': {
                    'total_neurons': int(len(self.neurons)),
                    'total_synapses': int(len(self.synapses)),
                    'thoughts': int(self.total_thoughts),
                    'knowledge_level': float(self.knowledge_level)
                }
            }
    
    def process_task(self, task_description: str) -> Dict:
        """Verarbeite eine Aufgabe und simuliere Denken"""
        complexity = min(len(task_description) / 100, 1.0)
        result = self.think(complexity)
        return result


# Singleton Instanz
_brain_instance: Optional[NeuroCore] = None

def get_brain() -> NeuroCore:
    global _brain_instance
    if _brain_instance is None:
        _brain_instance = NeuroCore()
    return _brain_instance

if __name__ == "__main__":
    # Test des Gehirns
    brain = get_brain()
    print("Gehirn initialisiert!")
    print(f"Neuronen: {len(brain.neurons)}")
    print(f"Synapsen: {len(brain.synapses)}")
    
    for i in range(5):
        result = brain.process_task(f"Testaufgabe {i}")
        print(f"Gedanke {i}: {result}")
