# Task 1 for QOSF Mentorship Program

I have used qiskit libraries to construct the quantum circuit(s) with Rx, Rz and CZ gates and to generate a random reference vector as described in https://docs.google.com/document/d/1Ow3v8Y4rYBdgxXNxKV9ZUAM4bwL6211U6DWCcByZ4A4/edit

The optimisation of the randomly initalised angles (in range 0-2pi) of the rotation gates, is carried out with a classical BFGS algorithm.

Number of q-bits and layers are inputs in the script.

Please find attached example outputs for 4 qubits: the descent of the minimised distance vs 1-5 layers (plot_min_dist.png) and a collection of information and parameters (output.txt), including the randomy genereated reference vector, the optimised vector, the optimised parameters etc
