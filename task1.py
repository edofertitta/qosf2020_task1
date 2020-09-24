from qiskit import *
from qiskit.quantum_info import random_statevector

import numpy as np
from numpy import pi, random, linalg, sign
from scipy import optimize
import cmath
import matplotlib.pyplot as plt

def vec_distance(angle, n, l, ref_vector, optimise=False, gradients=False):
  
    # Reshape the parameters vector into a matrix for convenience
    angle = angle.reshape((2*l, n))

    # Set Quantum circuit with n q-bits
    qreg_q = QuantumRegister(n, 'q')
    circuit = QuantumCircuit(qreg_q)
 
    # Reset all q-bits to |0> (not necessary)
    for i in range(n):
      circuit.reset(qreg_q[i])
    
    # Loop over all layers
    for w in range(l):
    # Loop over all q-bits
      for i in range(n):
        # Odd blocks
        circuit.rx(angle[2*w+1, i] , qreg_q[i])
        # Even blocks
        circuit.rz(angle[2*w, i] , qreg_q[i])
    # Loop over all q-bits
      for i in range(n):
        for j in range(i+1,n):
            circuit.cz(qreg_q[i], qreg_q[j])
    
    # Calculate the state vector
    simulator = Aer.get_backend('statevector_simulator')
    result = execute(circuit, backend = simulator).result()
    result_vector = result.get_statevector(circuit)

    # Calculate the norm of the distance between the state vector and the reference random vector
    distance = linalg.norm(result_vector - ref_vector)

    # If the function is passed to the optimiser, return only the cost function
    # Otherwise return the circuit and final vector (for tests and debugging)
    if optimise:
       return distance
    else:
       return distance, circuit, result_vector

#Number of q-bits / c-bits
n=4
#Number of layers
layers=[1,2,3,4,5]

maxiter=2000

#Random vector
ref_vector = random_statevector(2**n).data

# Setup output file 
f=open('output.txt', 'w')
print('REFERENCE VECTOR', ref_vector, file=f)

# Initialise list of distances vs layer number
min_distance = []
for l in layers:
    # Initialise random angles between 0 and 2pi - angles for odd(even) blocks have odd(even) indices
    angle_random = 2*pi*random.rand(2*l,n)

    # Minimise cost function 'vec_stance' by optimising the angles of Rx and Rz gates 
    res = optimize.minimize(vec_distance, angle_random, args=(n, l, ref_vector, True, False),
           method='BFGS',options={'disp':True,'maxiter':maxiter})

    # Optimised parameters
    final_angle = res.x

    # Calculate the distance and vector corresponding to the optimised angles 
    final_distance, final_circuit, final_vector = vec_distance(final_angle, n, l, ref_vector)

    # Update list of distances vs layer number
    min_distance.append(final_distance)   

    # Output final info 
    print('  ', file=f)
    print('NUMBER OF LAYERS', l, file=f)
    print('--------------------', file=f)
    print('FINAL DISTANCE', final_distance, file=f)
    print('FINAL ANGLES/pi', res.x/pi, file=f)
    print('FINAL VECTOR', final_vector, file=f)
    print('--------------------', file=f)


# Plot min. distance vs number of layers
fig, ax = plt.subplots(dpi=300, figsize=(10,5))
ax.set_xlabel("Number of layers", fontsize=12)
ax.set_ylabel("$min_{\\theta} || |\psi(\\theta) \\rightangle - |\phi \\rightangle ||$", fontsize=12)
ax.plot(layers, min_distance, linestyle='None', marker='o', markersize=10, markeredgewidth=0.7, markeredgecolor='black' , color='C0')
fig.savefig('plot_min_dist.png')

