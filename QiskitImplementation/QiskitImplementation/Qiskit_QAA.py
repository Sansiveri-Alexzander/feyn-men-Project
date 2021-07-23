from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute
from qiskit import Aer

def IQAE(regsize, bmax, shots, iterations):
    arr = []

    register = QuantumRegister(regsize)
    ancilla = QuantumRegister(1)
    measurement = ClassicalRegister(1)
    circuit = QuantumCircuit(register, ancilla, measurement)

    for i in range(shots):
        circuit.h(register)
        Rop(circuit, register, ancilla, bmax)

        for j in range(iterations+1):
            Q_Grover(circuit, register, ancilla, bmax)

        circuit.measure(ancilla, measurement)
        simulator = Aer.get_backend('aer_simulator')
        simulation = execute(circuit, simulator, shots=1)
        result = simulation.result()
        counts = result.get_counts(circuit)
        for(measured_state, count) in counts.items():
            if measured_state == "1":
                arr += True
            elif measured_state == "0":
                arr += False

    return arr

def Rop (circuit, register, ancilla, bmax):
    length = len(register)
    circuit.ry(bmax / (2**length), ancilla)
    for i in range(length):
        circuit.cry(register[i], (bmax / (2**length -1 -i)), ancilla)


def Q_Grover(circuit, register, ancilla, bmax): 
	#I didn't make this function controlled because it was only used in the controlled manner 
	#in the CamplitudeAmplification operation which wasn't ever used
	circuit.z(ancilla)

	#U_I
	inverse(Rop(circuit, register, ancilla, bmax)) #I believe this reverses the circuit steps of the Rop operation
	circuit.h(register)

	circuit.x(ancilla)
	circuit.x(register)
	circuit.h(ancilla)
	circuit.cx(register, ancilla)
	circuit.h(ancilla)
	circuit.x(register)
	circuit.x(ancilla)

	circuit.h(register)
	Rop(circuit, register, ancilla, bmax)
