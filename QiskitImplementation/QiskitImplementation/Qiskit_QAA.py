from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute
from qiskit import Aer

def amplitudeEstimation (regsize, iterations, shots, A, args):
    # from "Quantum amplitude estimation algorithms on IBM quantum devices" Rao et al. with methods from Suzuki et al.
    # https://arxiv.org/pdf/2008.02102.pdf
    

    onesMeasured = 0

    register = QuantumRegister(regsize)
    ancilla = QuantumRegister(1)
    measurement = ClassicalRegister(1)
    circuit = QuantumCircuit(register, ancilla, measurement)

    # A
    A(circuit, register, ancilla, args)

    for j in range(iterations):
        # Q = A S_0 A^-1 S_x
        # note: because quantum operations are like matrices, operations are applied right-to-left
        Q_Grover(circuit, register, ancilla, A, args)
    
    # measure ancilla into "measurement" after iterations of Q_Grover
    circuit.measure(ancilla, measurement)
    # set up simulator with "shots" shots
    simulator = Aer.get_backend('aer_simulator')
    simulation = execute(circuit, simulator, shots=shots)
    # get result of measuring it "shots" times, put it indictionary form, unpack in for loop
    result = simulation.result()
    counts = result.get_counts(circuit)
    # measured states will be only 1s and 0s since we only measure the ancilla
    for(measured_state, count) in counts.items():
        if measured_state == "1":
            onesMeasured = count

    return onesMeasured


"""
# Summary
Unitary operator that computes the definite integral of sin^2(x) from 0 to b with a Riemann sum.

# Input
## register
Qubit register -- The Riemann sum uses 2^n subintervals, where n is the length of the qubit register. 
## ancilla
Ancilla qubit
## args
1st argument should be upper bound of the integral, and 2nd argument should be 0, 0.5 or 1 for left, midpoint, or right Riemann sum, respectively (defaults to left Riemann sum).
"""
def intSinSq (circuit, register, ancilla, args):
    length = len(register)
    bmax = args[0]

    circuit.h(register)
    if args[1] == 0.5 or args[1] == 1.0:
        circuit.ry((args[1] * bmax) / IntAsDouble(2^length), ancilla)

    for i in range(length):
        circuit.cry((bmax / IntAsDouble(2^(length-1-i)), register[i], ancilla))


def Q_Grover(circuit, register, ancilla, A, args): 
	# S_x
    circuit.z(ancilla)
    # A
    ### create circuit of same size as the circuit we have passed as an argument (with the ancilla too)
    aReg = QuantumRegister(len(register))
    aAnc = QuantumRegister(1)
    aCircuit = QuantumCircuit(aReg, aAnc)
    ### pass this aCircuit through A in order to have it be purely the A operation
    A(aCircuit, aReg, aAnc, args)
    ### get inverse circuit of A operation
    aInverse = aCircuit.inverse()
    ### add it to the circuit? does this work this way or is this wrong?
    circuit = circuit + aInverse #questionable

    # S_0
    ### X on ancilla + register
    circuit.x(ancilla)
    circuit.x(register)
    ### H CX H == CZ
    circuit.h(ancilla)
    circuit.cx(register, ancilla)
    circuit.h(ancilla)
    ### X on ancilla + register again for cleanup
    circuit.x(register)
    circuit.x(ancilla)

    # A
    A(circuit, register, ancilla, args)
