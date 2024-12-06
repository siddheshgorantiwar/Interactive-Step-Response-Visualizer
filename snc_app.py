import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lti, step

def calculate_time_metrics(t, y, steady_state):
    rise_time = t[np.where(y >= 0.9 * steady_state)[0][0]] - t[np.where(y >= 0.1 * steady_state)[0][0]]
    settling_indices = np.where(np.abs(y - steady_state) <= 0.02 * steady_state)[0]
    settling_time = t[settling_indices[0]] if len(settling_indices) > 0 else None
    peak_time = t[np.argmax(y)]
    overshoot = (np.max(y) - steady_state) / steady_state * 100 if steady_state > 0 else 0

    return rise_time, settling_time, peak_time, overshoot

st.title("Interactive Step Response Visualizer")

st.sidebar.header("System Parameters")
system_type = st.sidebar.selectbox("Select System Type", ("First-Order", "Second-Order"))

if system_type == "First-Order":
    K = st.sidebar.slider("Gain (K)")
    T = st.sidebar.slider("Time Constant (T)")
    
    numerator = [K]
    denominator = [T, 1]
    system = lti(numerator, denominator)

elif system_type == "Second-Order":
    K = st.sidebar.slider("Gain (K)", 0.1, 10.0, 1.0, 0.1)
    zeta = st.sidebar.slider("Damping Ratio (\u03b6)", 0.0, 2.0, 0.7, 0.1)
    omega_n = st.sidebar.slider("Natural Frequency (\u03c9n)", 0.1, 10.0, 1.0, 0.1)

    numerator = [K * omega_n**2]
    denominator = [1, 2 * zeta * omega_n, omega_n**2]
    system = lti(numerator, denominator)

t, y = step(system)
steady_state = K
rise_time, settling_time, peak_time, overshoot = calculate_time_metrics(t, y, steady_state)

fig, ax = plt.subplots()
ax.plot(t, y, label="Step Response")
ax.axhline(y=steady_state, color='r', linestyle='--', label="Steady State")
ax.set_title(f"Step Response of {system_type} System")
ax.set_xlabel("Time")
ax.set_ylabel("Output")
ax.legend()
ax.grid()
st.pyplot(fig)

st.subheader("Time-Domain Metrics")
st.write(f"**Rise Time**: {rise_time:.2f} seconds")
st.write(f"**Settling Time**: {settling_time:.2f} seconds" if settling_time else "Settling Time: Not found")
st.write(f"**Peak Time**: {peak_time:.2f} seconds")
st.write(f"**Overshoot**: {overshoot:.2f}%")
