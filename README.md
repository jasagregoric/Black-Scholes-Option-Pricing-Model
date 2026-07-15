# Black-Scholes Option Pricing Model

A Python-based interactive dashboard for pricing European options using the **Black-Scholes Model**.

The application allows users to explore option prices, visualize price sensitivity, and analyze option Greeks through interactive charts and heatmaps.

---

## Live Demo

Try the live application here:

[Black-Scholes Option Pricing Model]([https://your-streamlit-link.streamlit.app/](https://option-pricing-black-scholes-model.streamlit.app/))

---

## Features

### Option Pricing
- Calculate European **CALL** and **PUT** option prices
- Uses the Black-Scholes analytical pricing formula
- Adjustable parameters:
  - Stock Price (S)
  - Strike Price (K)
  - Time to Expiration (T)
  - Volatility (σ)
  - Risk-Free Interest Rate (r)

---

## Interactive Heatmaps

Visualize how option prices change with:

- Stock Price
- Volatility

Includes:
- CALL price heatmap
- PUT price heatmap
- Adjustable grid resolution
- Automatic hiding of cell values for large grids

---

## Price Analysis

### Option Price vs Stock Price

Shows how CALL and PUT prices change as the underlying asset price changes.

Includes:
- CALL price curve
- PUT price curve
- Strike price indicator

---

## Greeks Analysis

The application calculates and visualizes:

- Delta
- Gamma
- Vega
- Theta
- Rho

Features:
- Greeks vs Stock Price charts
- Expandable Greeks value table

---

## 3D Price Surface

Interactive 3D visualization showing:

- X-axis: Stock Price
- Y-axis: Volatility
- Z-axis: Option Price

Separate surfaces for:
- CALL options
- PUT options

---

## Mathematical Model

The Black-Scholes model calculates option prices using:

### d1

$$
d_1 =
\frac{
\ln(\frac{S}{K})+\left(r+\frac{\sigma^2}{2}\right)T
}
{\sigma\sqrt{T}}
$$

### d₂

$$
d_2=d_1-\sigma\sqrt{T}
$$

### Call Price

$$
C=S N(d_1)-Ke^{-rT}N(d_2)
$$

### Put Price

$$
P=Ke^{-rT}N(-d_2)-SN(-d_1)
$$

---

## Technologies Used

- Python
- Streamlit
- NumPy
- SciPy
- Pandas
- Matplotlib

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/black-scholes-option-pricing-model.git
