"""
3D Brain Dashboard - Echtzeit Visualisierung des neuronalen Netzwerks
Zeigt das lernende Gehirn von Jarvis im Browser als 3D-Modell
"""

from flask import Flask, render_template_string, jsonify
import threading
import time
import sys
import os

# Füge parent directory zum Pfad hinzu
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brain.neuro_core import get_brain

app = Flask(__name__)

# Port aus Umgebungsvariable oder Standard 5000
import os
PORT = int(os.environ.get('BRAIN_PORT', 5000))

brain = get_brain()

# HTML Template für die 3D Visualisierung
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jarvis NeuroCore - 3D Gehirn Visualisierung</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0c0c1e 0%, #1a1a3e 50%, #0f0f2d 100%);
            overflow: hidden;
            color: #fff;
        }
        
        #container {
            display: flex;
            height: 100vh;
        }
        
        #brain-view {
            flex: 1;
            position: relative;
        }
        
        #sidebar {
            width: 350px;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(10px);
            padding: 20px;
            overflow-y: auto;
            border-left: 1px solid rgba(100, 150, 255, 0.3);
        }
        
        h1 {
            font-size: 24px;
            margin-bottom: 20px;
            background: linear-gradient(90deg, #00d4ff, #7b2ff7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        h2 {
            font-size: 16px;
            margin: 20px 0 10px 0;
            color: #00d4ff;
            border-bottom: 1px solid rgba(0, 212, 255, 0.3);
            padding-bottom: 5px;
        }
        
        .stat-box {
            background: rgba(0, 212, 255, 0.1);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            border: 1px solid rgba(0, 212, 255, 0.2);
        }
        
        .stat-value {
            font-size: 28px;
            font-weight: bold;
            color: #00d4ff;
        }
        
        .stat-label {
            font-size: 12px;
            color: #aaa;
            margin-top: 5px;
        }
        
        .region-bar {
            height: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            margin: 8px 0;
            overflow: hidden;
            position: relative;
        }
        
        .region-fill {
            height: 100%;
            border-radius: 10px;
            transition: width 0.5s ease;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 8px;
            font-size: 11px;
            font-weight: bold;
        }
        
        .region-logic { background: linear-gradient(90deg, #ff6b6b, #ff8e8e); }
        .region-memory { background: linear-gradient(90deg, #4ecdc4, #7eddd6); }
        .region-creativity { background: linear-gradient(90deg, #a78bfa, #c4b5fd); }
        .region-learning { background: linear-gradient(90deg, #fbbf24, #fcd34d); }
        
        .activity-log {
            font-family: 'Courier New', monospace;
            font-size: 11px;
            background: rgba(0, 0, 0, 0.5);
            border-radius: 5px;
            padding: 10px;
            max-height: 200px;
            overflow-y: auto;
        }
        
        .log-entry {
            margin: 3px 0;
            padding: 3px;
            border-left: 2px solid #00d4ff;
            padding-left: 8px;
        }
        
        .pulse {
            animation: pulse 1s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        #loading {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 18px;
            color: #00d4ff;
        }
    </style>
</head>
<body>
    <div id="container">
        <div id="brain-view">
            <div id="loading">Lade neuronales Netzwerk...</div>
        </div>
        <div id="sidebar">
            <h1>🧠 Jarvis NeuroCore</h1>
            
            <div class="stat-box">
                <div class="stat-value" id="total-neurons">0</div>
                <div class="stat-label">Neuronen</div>
            </div>
            
            <div class="stat-box">
                <div class="stat-value" id="total-synapses">0</div>
                <div class="stat-label">Synapsen</div>
            </div>
            
            <div class="stat-box">
                <div class="stat-value" id="total-thoughts">0</div>
                <div class="stat-label">Gedanken verarbeitet</div>
            </div>
            
            <div class="stat-box">
                <div class="stat-value" id="knowledge-level">0.00</div>
                <div class="stat-label">Wissensstand</div>
            </div>
            
            <h2>Gehirnregionen Aktivität</h2>
            <div class="region-bar">
                <div class="region-fill region-logic" id="bar-logic" style="width: 0%">Logic</div>
            </div>
            <div class="region-bar">
                <div class="region-fill region-memory" id="bar-memory" style="width: 0%">Memory</div>
            </div>
            <div class="region-bar">
                <div class="region-fill region-creativity" id="bar-creativity" style="width: 0%">Creativity</div>
            </div>
            <div class="region-bar">
                <div class="region-fill region-learning" id="bar-learning" style="width: 0%">Learning</div>
            </div>
            
            <h2>Aktivitäts-Log</h2>
            <div class="activity-log" id="activity-log">
                <div class="log-entry">System gestartet...</div>
            </div>
        </div>
    </div>
    
    <script>
        let scene, camera, renderer;
        let neuronSpheres = [];
        let synapseLines = [];
        let brainData = null;
        
        function init() {
            const container = document.getElementById('brain-view');
            
            // Szene erstellen
            scene = new THREE.Scene();
            
            // Kamera
            camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
            camera.position.z = 30;
            
            // Renderer
            renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
            renderer.setSize(container.clientWidth, container.clientHeight);
            renderer.setPixelRatio(window.devicePixelRatio);
            container.appendChild(renderer.domElement);
            
            // Licht
            const ambientLight = new THREE.AmbientLight(0x404040, 0.5);
            scene.add(ambientLight);
            
            const pointLight = new THREE.PointLight(0x00d4ff, 1, 100);
            pointLight.position.set(10, 10, 10);
            scene.add(pointLight);
            
            const pointLight2 = new THREE.PointLight(0x7b2ff7, 0.8, 100);
            pointLight2.position.set(-10, -10, 10);
            scene.add(pointLight2);
            
            document.getElementById('loading').style.display = 'none';
            
            // Daten laden
            loadBrainData();
            
            // Animation Loop
            animate();
        }
        
        function createNeurons(neurons) {
            // Alte Neuronen entfernen
            neuronSpheres.forEach(sphere => scene.remove(sphere));
            neuronSpheres = [];
            
            const geometry = new THREE.SphereGeometry(0.5, 16, 16);
            
            neurons.forEach(neuron => {
                const intensity = Math.min(neuron.activation, 1);
                const color = new THREE.Color().setHSL(0.6 + intensity * 0.2, 1, 0.5 + intensity * 0.3);
                
                const material = new THREE.MeshPhongMaterial({
                    color: color,
                    emissive: color,
                    emissiveIntensity: intensity * 0.5,
                    transparent: true,
                    opacity: 0.8 + intensity * 0.2
                });
                
                const sphere = new THREE.Mesh(geometry, material);
                sphere.position.set(neuron.x, neuron.y, neuron.z);
                sphere.userData = neuron;
                
                scene.add(sphere);
                neuronSpheres.push(sphere);
            });
        }
        
        function createSynapses(synapses) {
            // Alte Synapsen entfernen
            synapseLines.forEach(line => scene.remove(line));
            synapseLines = [];
            
            synapses.forEach(synapse => {
                const fromNeuron = neuronSpheres.find(s => s.userData.id === synapse.from);
                const toNeuron = neuronSpheres.find(s => s.userData.id === synapse.to);
                
                if (fromNeuron && toNeuron) {
                    const points = [fromNeuron.position, toNeuron.position];
                    const geometry = new THREE.BufferGeometry().setFromPoints(points);
                    
                    const intensity = Math.min(Math.abs(synapse.activity), 1);
                    const color = new THREE.Color().setHSL(0.5 + intensity * 0.3, 1, 0.6);
                    
                    const material = new THREE.LineBasicMaterial({
                        color: color,
                        transparent: true,
                        opacity: 0.1 + intensity * 0.4,
                        linewidth: 1
                    });
                    
                    const line = new THREE.Line(geometry, material);
                    scene.add(line);
                    synapseLines.push(line);
                }
            });
        }
        
        function updateVisuals() {
            if (!brainData) return;
            
            createNeurons(brainData.neurons);
            createSynapses(brainData.synapses);
            
            // Stats aktualisieren
            document.getElementById('total-neurons').textContent = brainData.stats.total_neurons;
            document.getElementById('total-synapses').textContent = brainData.stats.total_synapses;
            document.getElementById('total-thoughts').textContent = brainData.stats.thoughts;
            document.getElementById('knowledge-level').textContent = brainData.stats.knowledge_level.toFixed(2);
            
            // Regionen aktualisieren
            const regions = brainData.regions;
            document.getElementById('bar-logic').style.width = (regions.logic * 100) + '%';
            document.getElementById('bar-memory').style.width = (regions.memory * 100) + '%';
            document.getElementById('bar-creativity').style.width = (regions.creativity * 100) + '%';
            document.getElementById('bar-learning').style.width = (regions.learning * 100) + '%';
        }
        
        function addLogEntry(message) {
            const log = document.getElementById('activity-log');
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            entry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
            log.insertBefore(entry, log.firstChild);
            
            // Maximal 20 Einträge
            while (log.children.length > 20) {
                log.removeChild(log.lastChild);
            }
        }
        
        async function loadBrainData() {
            try {
                const response = await fetch('/api/brain-state');
                brainData = await response.json();
                updateVisuals();
                addLogEntry(`Gehirnzustand aktualisiert - ${brainData.stats.thoughts} Gedanken`);
            } catch (error) {
                console.error('Fehler beim Laden der Gehirndaten:', error);
            }
        }
        
        function animate() {
            requestAnimationFrame(animate);
            
            // Rotation des Gehirns
            if (neuronSpheres.length > 0) {
                neuronSpheres.forEach((sphere, i) => {
                    sphere.rotation.y += 0.001;
                    sphere.rotation.z += 0.0005;
                });
            }
            
            // Sanfte Kamerabewegung
            const time = Date.now() * 0.0005;
            camera.position.x = Math.sin(time) * 5;
            camera.position.y = Math.cos(time * 0.7) * 3;
            camera.lookAt(0, 0, 0);
            
            renderer.render(scene, camera);
        }
        
        // Initialisierung
        window.addEventListener('resize', () => {
            const container = document.getElementById('brain-view');
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        });
        
        init();
        
        // Alle 2 Sekunden Daten aktualisieren
        setInterval(loadBrainData, 2000);
        
        // Alle 5 Sekunden einen Gedanken simulieren
        setInterval(async () => {
            try {
                await fetch('/api/think', { method: 'POST' });
                addLogEntry('Neuer Gedanke generiert...');
            } catch (error) {
                console.error('Fehler beim Denken:', error);
            }
        }, 5000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/brain-state')
def get_brain_state():
    state = brain.get_state()
    return jsonify(state)

@app.route('/api/think', methods=['POST'])
def think():
    result = brain.process_task("Automatischer Denkprozess")
    return jsonify(result)

def run_dashboard(port=5000):
    """Starte das Dashboard"""
    print(f"🧠 Starte NeuroCore 3D Dashboard auf http://localhost:{port}")
    print("Öffne diesen Link in deinem Browser um das Gehirn zu sehen!")
    
    # Starte einen Hintergrund-Thread für kontinuierliches Denken
    def continuous_thinking():
        while True:
            time.sleep(3)
            brain.process_task("Hintergrundprozess")
    
    thinking_thread = threading.Thread(target=continuous_thinking, daemon=True)
    thinking_thread.start()
    
    # Verwende PORT Variable statt festem Parameter
    print(f"🧠 Starte NeuroCore 3D Dashboard auf http://localhost:{PORT}")
    print(f"Öffne diesen Link in deinem Browser um das Gehirn zu sehen!")
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

if __name__ == "__main__":
    run_dashboard()
