import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# App setup
st.set_page_config(page_title="VLE Diagrams - n-Hexane and n-Heptane", layout="centered")
st.title("T-x-y and x-y Diagram for n-Hexane + n-Heptane System")

st.markdown("""
#### Submitted by: **Mohtashim Farooqui**  
**To:** Prof. Imran Mohammad  
**Department of Petrochemical Engineering**  
**UIT RGPV, Bhopal**

---

### System Studied: n-Hexane + n-Heptane

This app calculates and plots T-x-y and x-y diagrams for an ideal binary mixture using Raoult's Law and Antoine's Equation.
""")

# Antoine constants
antoine_constants = {
    "n-hexane": {"A": 6.8763, "B": 1171.53, "C": 224.0},
    "n-heptane": {"A": 6.893, "B": 1260.0, "C": 216.0}
}

def antoine_eq(T, A, B, C):
    return 10**(A - B / (C + T))  # P in mmHg

P_total = 760  # Total pressure in mmHg

def bubble_point_temp(x_hexane):
    def func(T):
        P_hex = antoine_eq(T, **antoine_constants["n-hexane"])
        P_hept = antoine_eq(T, **antoine_constants["n-heptane"])
        x_hept = 1 - x_hexane
        return x_hexane * P_hex + x_hept * P_hept - P_total
    return fsolve(func, 60)[0]  # Initial guess for T

# Generate data
x_vals = np.linspace(0, 1, 21)
T_vals = []
y_vals = []

for x in x_vals:
    T = bubble_point_temp(x)
    P_hex = antoine_eq(T, **antoine_constants["n-hexane"])
    y = (x * P_hex) / P_total
    T_vals.append(T)
    y_vals.append(y)

# T-x-y Diagram
st.subheader("T-x-y Diagram")
fig1, ax1 = plt.subplots()
ax1.plot(x_vals, T_vals, 'bo-', label='Liquid (x vs T)')
ax1.plot(y_vals, T_vals, 'ro--', label='Vapor (y vs T)')
ax1.set_xlabel("Mole Fraction of n-Hexane")
ax1.set_ylabel("Temperature (°C)")
ax1.set_title("T-x-y Diagram at 1 atm")
ax1.legend()
ax1.grid()
st.pyplot(fig1)

# x-y Diagram
st.subheader("x-y Diagram")
fig2, ax2 = plt.subplots()
ax2.plot(x_vals, y_vals, 'go-', label='x-y Curve')
ax2.plot([0, 1], [0, 1], 'k--', label='y = x')
ax2.set_xlabel("x (Liquid Mole Fraction of n-Hexane)")
ax2.set_ylabel("y (Vapor Mole Fraction of n-Hexane)")
ax2.set_title("x-y Diagram at 1 atm")
ax2.legend()
ax2.grid()
st.pyplot(fig2)

st.markdown("""
---

### Notes:
- Antoine Equation: $$P_{\text{sat}} = 10^{A - B / (C + T)}$$
- Bubble point T: $$x P_{hex} + (1 - x) P_{hept} = P_{\text{total}}$$
- Vapor mole fraction: $$y = \frac{x P_{hex}}{P_{\text{total}}}$$

This app visualizes VLE behavior of an ideal binary system.

""")
