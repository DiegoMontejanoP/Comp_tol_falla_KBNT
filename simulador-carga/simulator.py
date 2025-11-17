from flask import Flask, jsonify, request
import threading
import time
import requests
import random
import json

app = Flask(__name__)


class SimuladorCarga:
    def __init__(self):
        self.activo = False
        self.hilos = []
        self.metricas = {
            'total_requests': 0,
            'requests_exitosos': 0,
            'requests_fallidos': 0,
            'tiempo_promedio': 0
        }

    def generar_carga(self, num_usuarios=10):
        servicios = ['suma', 'resta', 'multiplicacion', 'division', 'exponente']
        base_url = "http://frontend:5000"

        while self.activo:
            for _ in range(num_usuarios):
                if not self.activo:
                    break

                servicio = random.choice(servicios)
                a = random.uniform(-100, 100)
                b = random.uniform(-100, 100)

                inicio = time.time()
                try:
                    response = requests.post(
                        f"{base_url}/calcular",
                        json={'a': a, 'b': b, 'operacion': servicio},
                        timeout=10
                    )

                    self.metricas['total_requests'] += 1
                    if response.status_code == 200:
                        self.metricas['requests_exitosos'] += 1
                    else:
                        self.metricas['requests_fallidos'] += 1

                except Exception as e:
                    self.metricas['requests_fallidos'] += 1

                fin = time.time()
                self.metricas['tiempo_promedio'] = (
                                                           self.metricas['tiempo_promedio'] + (fin - inicio)
                                                   ) / 2

                time.sleep(random.uniform(0.1, 1.0))


simulador = SimuladorCarga()


@app.route('/simulador/iniciar', methods=['POST'])
def iniciar_simulacion():
    if not simulador.activo:
        data = request.json or {}
        num_usuarios = data.get('usuarios', 5)

        simulador.activo = True
        hilo = threading.Thread(target=simulador.generar_carga, args=(num_usuarios,))
        hilo.daemon = True
        hilo.start()
        simulador.hilos.append(hilo)

        return jsonify({
            'status': 'simulacion_iniciada',
            'usuarios_simulados': num_usuarios,
            'mensaje': f'Simulación iniciada con {num_usuarios} usuarios virtuales'
        })
    else:
        return jsonify({'error': 'La simulación ya está activa'}), 400


@app.route('/simulador/detener', methods=['POST'])
def detener_simulacion():
    simulador.activo = False
    # Esperar a que los hilos terminen
    for hilo in simulador.hilos:
        hilo.join(timeout=5)
    simulador.hilos.clear()

    return jsonify({
        'status': 'simulacion_detenida',
        'metricas_finales': simulador.metricas
    })


@app.route('/simulador/estado', methods=['GET'])
def estado_simulacion():
    return jsonify({
        'activo': simulador.activo,
        'metricas': simulador.metricas
    })


@app.route('/simulador/ajustar', methods=['POST'])
def ajustar_carga():
    if simulador.activo:
        data = request.json
        num_usuarios = data.get('usuarios', 5)

        # Reiniciar simulación con nuevo número de usuarios
        simulador.activo = False
        for hilo in simulador.hilos:
            hilo.join(timeout=5)
        simulador.hilos.clear()

        # Reiniciar con nueva carga
        simulador.activo = True
        hilo = threading.Thread(target=simulador.generar_carga, args=(num_usuarios,))
        hilo.daemon = True
        hilo.start()
        simulador.hilos.append(hilo)

        return jsonify({
            'status': 'carga_ajustada',
            'nuevos_usuarios': num_usuarios
        })
    else:
        return jsonify({'error': 'La simulación no está activa'}), 400


@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'servicio': 'simulador_carga'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)