import os
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

def grover_2qubits(target="11", shots=1024):
    """Grover para n=2 qubits buscando el estado target."""
    qc = QuantumCircuit(2, 2) 
    
    # Paso 1: Superposición uniforme
    qc.h([0, 1]) 
    
    # Paso 2: Oráculo de fase que marca el estado target
    if target == "11":
        qc.cz(0, 1)  # CZ invierte la fase únicamente en |11>
    elif target == "00":
        qc.x([0, 1])
        qc.cz(0, 1)
        qc.x([0, 1])
    elif target == "01":
        qc.x(1)      # Se corrige: x va en qubit 1 para aislar q1=0, q0=1
        qc.cz(0, 1)
        qc.x(1)
    elif target == "10":
        qc.x(0)      # Se corrige: x va en qubit 0 para aislar q1=1, q0=0
        qc.cz(0, 1)
        qc.x(0)
        
    # Paso 3: Difusor (Inversión alrededor de la media)
    qc.h([0, 1]) 
    qc.x([0, 1]) 
    qc.cz(0, 1) 
    qc.x([0, 1]) 
    qc.h([0, 1]) 
    
    # Medición de los qubits
    qc.measure([0, 1], [0, 1])

    # Ejecución del simulador local
    sim = AerSimulator() 
    counts = sim.run(qc, shots=shots).result().get_counts() 
    
    print(f"Grover buscando |{target}> ({shots} shots):") 
    for state, count in sorted(counts.items()): 
        pct = (count / shots) * 100 
        print(f"  |{state}>: {count:4d} ({pct:.1f}%)")
        
    # Validar el estado más probable
    top = max(counts, key=counts.get) 
    resultado = "CORRECTO" if top == target else "ERROR" 
    print(f"Estado más probable: |{top}> -> {resultado}")
    
    # Asegurar que la carpeta de capturas exista en Windows
    os.makedirs("capturas", exist_ok=True)
    
    # Generar y guardar el histograma correspondiente
    fig = plot_histogram(counts) 
    fig.savefig(f"capturas/grover_{target}.png", dpi=150) 
    plt.close(fig)  # Cierra la figura para liberar memoria en ciclos largos
    
    return counts 

if __name__ == "__main__": 
    # Probar el algoritmo iterando por los 4 estados objetivo posibles
    for t in ["00", "01", "10", "11"]: 
        grover_2qubits(target=t) 
        print("-" * 40) 