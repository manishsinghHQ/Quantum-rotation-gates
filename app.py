import streamlit as st
import numpy as np
import random
import matplotlib.pyplot as plt

st.set_page_config(page_title="Quantum Rotation Gate Optimizer")

st.title("⚛️ Quantum Rotation Gate Optimization")
st.write("This demo replaces classical mutation with quantum rotation gates.")

# Parameters
num_qubits = st.slider("Number of Qubits", 5, 50, 20)
iterations = st.slider("Iterations", 10, 200, 100)
theta = st.slider("Rotation Angle", 0.001, 0.1, 0.01)

# Initialize qubits
def initialize_qubits(n):
    qubits = []
    for _ in range(n):
        alpha = 1/np.sqrt(2)
        beta = 1/np.sqrt(2)
        qubits.append([alpha, beta])
    return np.array(qubits)

# Observe qubits → binary solution
def observe(qubits):
    solution = []

    for alpha, beta in qubits:
        r = random.random()

        if r < alpha**2:
            solution.append(0)
        else:
            solution.append(1)

    return solution

# Fitness function
def fitness(solution):
    return sum(solution)

# Quantum rotation gate update
def rotate(qubits, solution, best_solution, theta):

    for i in range(len(qubits)):
        alpha, beta = qubits[i]

        if solution[i] != best_solution[i]:

            if best_solution[i] == 1:
                delta = theta
            else:
                delta = -theta

            rotation = np.array([
                [np.cos(delta), -np.sin(delta)],
                [np.sin(delta), np.cos(delta)]
            ])

            new_state = rotation @ np.array([alpha, beta])
            qubits[i] = new_state

    return qubits


if st.button("Run Optimization"):

    qubits = initialize_qubits(num_qubits)

    best_solution = None
    best_fit = -1

    history = []

    for _ in range(iterations):

        solution = observe(qubits)
        fit = fitness(solution)

        if fit > best_fit:
            best_fit = fit
            best_solution = solution

        qubits = rotate(qubits, solution, best_solution, theta)

        history.append(best_fit)

    st.success(f"Best Fitness Found: {best_fit}")

    st.write("Best Solution:")
    st.write(best_solution)

    # Plot progress
    fig, ax = plt.subplots()
    ax.plot(history)
    ax.set_xlabel("Iterations")
    ax.set_ylabel("Best Fitness")
    ax.set_title("Optimization Progress")

    st.pyplot(fig)
