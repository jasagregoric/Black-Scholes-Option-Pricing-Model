import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import norm
from numpy import log, sqrt, exp
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mp
from mpl_toolkits.mplot3d import Axes3D

st.set_page_config(
    page_title="Black-Scholes Model",
    layout="wide"
)

class BlackScholes:
    def __init__(self, stock_price, exercise_price, interest_rate, time_to_expiration, volatility):
        self.stock_price = stock_price
        self.exercise_price = exercise_price
        self.interest_rate = interest_rate
        self.time_to_expiration = time_to_expiration
        self.volatility = volatility

    def calculate_d1_d2(self, ):
        stock_price = self.stock_price
        exercise_price = self.exercise_price
        interest_rate = self.interest_rate
        time_to_expiration = self.time_to_expiration
        volatility = self.volatility

        d1 = (log((stock_price / exercise_price)) + (interest_rate + (volatility ** 2) / 2) * time_to_expiration) / (volatility * sqrt(time_to_expiration))
        d2 = d1 - volatility * sqrt(time_to_expiration)

        return (d1, d2)

    
    def calculate_call_put(self, ):
        stock_price = self.stock_price
        exercise_price = self.exercise_price
        interest_rate = self.interest_rate
        time_to_expiration = self.time_to_expiration

        d1, d2 = self.calculate_d1_d2()
        call = (stock_price * norm.cdf(d1)) - (exercise_price * exp(-(interest_rate * time_to_expiration)) * norm.cdf(d2))
        put = (exercise_price * exp(-(interest_rate * time_to_expiration)) * norm.cdf(-d2)) - stock_price * norm.cdf(-d1)
        return (call, put)
    
    def call(self, min_price, max_price, o_min, o_max, size_x, size_y):
        values = np.zeros(shape=(size_y, size_x))

        x_increment = (max_price - min_price) / (size_x - 1)
        y_increment = (o_max - o_min) / (size_y - 1)

        for i in range(size_y):
            volatility = o_min + i * y_increment

            for j in range(size_x):
                stock_price = min_price + j * x_increment

                model = BlackScholes(
                    stock_price,
                    self.exercise_price,
                    self.interest_rate,
                    self.time_to_expiration,
                    volatility
                )

                call, put = model.calculate_call_put()

                values[i][j] = call

        return values
    
    def put(self, min_price, max_price, o_min, o_max, size_x, size_y):
        values = np.zeros(shape=(size_y, size_x))

        x_increment = (max_price - min_price) / (size_x - 1)
        y_increment = (o_max - o_min) / (size_y - 1)

        for i in range(size_y):
            volatility = o_min + i * y_increment

            for j in range(size_x):
                stock_price = min_price + j * x_increment

                model = BlackScholes(
                    stock_price,
                    self.exercise_price,
                    self.interest_rate,
                    self.time_to_expiration,
                    volatility
                )

                call, put = model.calculate_call_put()

                values[i][j] = put

        return values
    
    def greeks(self, ):
        stock_price = self.stock_price
        exercise_price = self.exercise_price
        interest_rate = self.interest_rate
        time_to_expiration = self.time_to_expiration
        volatility = self.volatility

        d1, d2 = self.calculate_d1_d2()

        delta_call = norm.cdf(d1)
        delta_put = norm.cdf(d1) - 1

        gamma = norm.pdf(d1) / (stock_price * volatility * sqrt(time_to_expiration))

        vega = stock_price * norm.pdf(d1) * sqrt(time_to_expiration)

        theta_call = -((stock_price * norm.pdf(d1) * volatility)/(2 * sqrt(time_to_expiration))) - (interest_rate * exercise_price * exp(-interest_rate * time_to_expiration) * norm.cdf(d2))
        theta_put =  -((stock_price * norm.pdf(d1) * volatility)/(2 * sqrt(time_to_expiration))) + (interest_rate * exercise_price * exp(-interest_rate * time_to_expiration) * norm.cdf(-d2))

        rho_call = exercise_price * time_to_expiration * exp(-interest_rate * time_to_expiration) * norm.cdf(d2)
        rho_put = -(exercise_price * time_to_expiration * exp(-interest_rate * time_to_expiration) * norm.cdf(-d2))

        return [delta_call, delta_put, gamma, vega, theta_call, theta_put, rho_call, rho_put]


with st.sidebar:
    st.subheader("⚙️ Model Parameters")

    stock_price = st.number_input(
        "Stock Price (S)",
        value=100.0,
        help="Current market price of the underlying asset"
    )

    exercise_price = st.number_input(
        "Strike Price (X)",
        value=120.0,
        help="Exercise price of the option"
    )

    time_to_expiration = st.number_input(
        "Time to Expiration (T)",
        value=1.0,
        help="Time remaining until expiration in years"
    )

    volatility = st.number_input(
        "Volatility (σ)",
        value=0.2,
        step=0.01,
        help="Annualized volatility"
    )

    interest_rate = st.number_input(
        "Risk-Free Rate (r)",
        value=0.05,
        step=0.01,
        help="Annual risk-free interest rate"
    )

    st.markdown("---")

    st.subheader("Heatmap Settings")

    spot_min = st.number_input(
        "Minimum Stock Price",
        min_value=0.01,
        value=stock_price * 0.8,
        step=1.0
    )

    spot_max = st.number_input(
        "Maximum Stock Price",
        min_value=0.01,
        value=stock_price * 1.2,
        step=1.0
    )

    o_min = st.slider(
        "Minimum Volatility",
        min_value=0.01,
        max_value=1.0,
        value=volatility * 0.5,
        step=0.01
    )

    o_max = st.slider(
        "Maximum Volatility",
        min_value=0.01,
        max_value=1.0,
        value=volatility * 1.5,
        step=0.01
    )

    st.markdown("#### Heatmap Resolution")

    col1, col2 = st.columns(2)

    with col1:
        x_size = st.number_input(
            "X Size",
            min_value=3,
            max_value=100,
            value=10,
            step=1,
            help="Number of columns in the heatmap."
        )

    with col2:
        y_size = st.number_input(
            "Y Size",
            min_value=3,
            max_value=100,
            value=10,
            step=3,
            help="Number of rows in the heatmap."
        )

    st.markdown("---")

    calculate_btn = st.button(
        "Generate Heatmap",
        use_container_width=True
    )

def plot_heatmap(bs_model, spot_range, vol_range):

    call_prices = np.zeros((len(vol_range), len(spot_range)))
    put_prices = np.zeros((len(vol_range), len(spot_range)))

    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):

            bs_temp = BlackScholes(
                stock_price=spot,
                exercise_price=bs_model.exercise_price,
                interest_rate=bs_model.interest_rate,
                time_to_expiration=bs_model.time_to_expiration,
                volatility=vol
            )

            call, put = bs_temp.calculate_call_put()

            call_prices[i, j] = call
            put_prices[i, j] = put


    # Show values only for small grids
    show_values = len(spot_range) <= 15 and len(vol_range) <= 15


    # Reduce axis labels for large grids
    max_ticks = 10

    x_step = max(1, len(spot_range) // max_ticks)
    y_step = max(1, len(vol_range) // max_ticks)

    x_ticks = range(0, len(spot_range), x_step)
    y_ticks = range(0, len(vol_range), y_step)


    # CALL HEATMAP
    fig_call, ax_call = plt.subplots(figsize=(10, 8))

    sns.heatmap(
        call_prices,
        xticklabels=np.round(spot_range, 2),
        yticklabels=np.round(vol_range, 2),
        annot=show_values,
        fmt=".2f",
        cmap="RdYlGn",
        ax=ax_call
    )

    ax_call.set_title("CALL")
    ax_call.set_xlabel("Spot Price")
    ax_call.set_ylabel("Volatility")


    # PUT HEATMAP
    fig_put, ax_put = plt.subplots(figsize=(10, 8))

    sns.heatmap(
        put_prices,
        xticklabels=np.round(spot_range, 2),
        yticklabels=np.round(vol_range, 2),
        annot=show_values,
        fmt=".2f",
        cmap="RdYlGn",
        ax=ax_put
    )

    ax_put.set_title("PUT")
    ax_put.set_xlabel("Spot Price")
    ax_put.set_ylabel("Volatility")


    fig_call.tight_layout()
    fig_put.tight_layout()

    return fig_call, fig_put

col1, col2 = st.columns([6, 1])

with col2:
    st.write("`Created by:`")
    linkedin_url = "https://www.linkedin.com/in/ja%C5%A1a-gregori%C4%8D-310458422/"
    st.markdown(f'<a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Jaša Gregorič`</a>', unsafe_allow_html=True)

st.title("Black-Scholes Pricing Model")


bs_model = BlackScholes(
    stock_price,
    exercise_price,
    interest_rate,
    time_to_expiration,
    volatility
)

call_price, put_price = bs_model.calculate_call_put()

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div style="
        background:#1f4e79;
        padding:12px;
        border-radius:10px;
        text-align:center;
        color:white;
    ">
        <div style="font-size:18px; font-weight:600;">
            CALL
        </div>
        <div style="font-size:28px; font-weight:bold; margin-top:4px;">
            ${call_price:.2f}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="
        background:#dc3545;
        padding:12px;
        border-radius:10px;
        text-align:center;
        color:white;
    ">
        <div style="font-size:18px; font-weight:600;">
            PUT
        </div>
        <div style="font-size:28px; font-weight:bold; margin-top:4px;">
            ${put_price:.2f}
        </div>
    </div>
    """, unsafe_allow_html=True)


spot_range = np.linspace(
    spot_min,
    spot_max,
    int(x_size)
)

vol_range = np.linspace(
    o_max,
    o_min,
    int(y_size)
)


fig_call, fig_put = plot_heatmap(
    bs_model,
    spot_range,
    vol_range
)

col1, col2 = st.columns([1,1])

with col1:
    st.subheader("CALL")
    st.pyplot(fig_call, width="stretch")

with col2:
    st.subheader("PUT")
    st.pyplot(fig_put, width="stretch")

def plot_price_curve(bs_model, min_price, max_price):

    stock_prices = np.linspace(min_price, max_price, 100)

    call_prices = []
    put_prices = []

    for stock_price in stock_prices:

        model = BlackScholes(
            stock_price,
            bs_model.exercise_price,
            bs_model.interest_rate,
            bs_model.time_to_expiration,
            bs_model.volatility
        )

        call, put = model.calculate_call_put()

        call_prices.append(call)
        put_prices.append(put)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        stock_prices,
        call_prices,
        color="#1f4e79",
        linewidth=2.5,
        label="Call"
    )

    ax.plot(
        stock_prices,
        put_prices,
        color="red",
        linewidth=2.5,
        label="Put"
    )

    # Strike price
    ax.axvline(
        bs_model.exercise_price,
        color="black",
        linestyle="--",
        linewidth=1.5,
        label="Strike Price"
    )

    ax.set_title("Option Price vs Stock Price")
    ax.set_xlabel("Stock Price")
    ax.set_ylabel("Option Price")

    ax.grid(True, alpha=0.3)
    ax.legend()

    fig.tight_layout()

    return fig

st.markdown("---")

st.subheader("Option Price vs Stock Price")

price_curve = plot_price_curve(
    bs_model,
    spot_min,
    spot_max
)

st.pyplot(price_curve, width="stretch")

def plot_greeks_vs_stock(bs_model, min_price, max_price):

    stock_prices = np.linspace(min_price, max_price, 100)

    delta_call = []
    delta_put = []
    gamma = []
    vega = []
    theta_call = []
    theta_put = []
    rho_call = []
    rho_put = []


    for stock_price in stock_prices:

        model = BlackScholes(
            stock_price,
            bs_model.exercise_price,
            bs_model.interest_rate,
            bs_model.time_to_expiration,
            bs_model.volatility
        )

        greeks = model.greeks()

        delta_call.append(greeks[0])
        delta_put.append(greeks[1])
        gamma.append(greeks[2])
        vega.append(greeks[3])
        theta_call.append(greeks[4])
        theta_put.append(greeks[5])
        rho_call.append(greeks[6])
        rho_put.append(greeks[7])


    # Create 4 plots
    fig, axs = plt.subplots(
        2,
        2,
        figsize=(14, 10)
    )


    # Delta
    axs[0,0].plot(stock_prices, delta_call, label="Call Delta")
    axs[0,0].plot(stock_prices, delta_put, label="Put Delta")

    axs[0,0].set_title("Delta vs Stock Price")
    axs[0,0].set_xlabel("Stock Price")
    axs[0,0].set_ylabel("Delta")
    axs[0,0].legend()
    axs[0,0].grid(True)


    # Gamma
    axs[0,1].plot(stock_prices, gamma, color="purple")

    axs[0,1].set_title("Gamma vs Stock Price")
    axs[0,1].set_xlabel("Stock Price")
    axs[0,1].set_ylabel("Gamma")
    axs[0,1].grid(True)


    # Vega
    axs[1,0].plot(stock_prices, vega, color="orange")

    axs[1,0].set_title("Vega vs Stock Price")
    axs[1,0].set_xlabel("Stock Price")
    axs[1,0].set_ylabel("Vega")
    axs[1,0].grid(True)


    # Theta + Rho
    axs[1,1].plot(stock_prices, theta_call, label="Call Theta")
    axs[1,1].plot(stock_prices, theta_put, label="Put Theta")
    axs[1,1].plot(stock_prices, rho_call, label="Call Rho")
    axs[1,1].plot(stock_prices, rho_put, label="Put Rho")

    axs[1,1].set_title("Theta & Rho vs Stock Price")
    axs[1,1].set_xlabel("Stock Price")
    axs[1,1].set_ylabel("Value")
    axs[1,1].legend()
    axs[1,1].grid(True)


    fig.suptitle(
        "Black-Scholes Greeks vs Stock Price",
        fontsize=16
    )

    fig.tight_layout()

    return fig
    

st.markdown("---")

st.subheader("Greeks vs Stock Price")

greeks_chart = plot_greeks_vs_stock(
    bs_model,
    spot_min,
    spot_max
)

st.pyplot(
    greeks_chart,
    width="stretch"
)

with st.expander("View Greeks Values"):

    greeks_values = bs_model.greeks()

    greeks_df = pd.DataFrame({
        "Greek": [
            "Call Delta",
            "Put Delta",
            "Gamma",
            "Vega",
            "Call Theta",
            "Put Theta",
            "Call Rho",
            "Put Rho"
        ],
        "Value": [
            greeks_values[0],
            greeks_values[1],
            greeks_values[2],
            greeks_values[3],
            greeks_values[4],
            greeks_values[5],
            greeks_values[6],
            greeks_values[7]
        ]
    })

    greeks_df["Value"] = greeks_df["Value"].round(4)

    st.dataframe(
        greeks_df,
        hide_index=True,
        use_container_width=True
    )

def plot_3d_surface(bs_model, min_price, max_price, min_vol, max_vol, option="call"):

    stock_prices = np.linspace(min_price, max_price, 50)
    volatilities = np.linspace(min_vol, max_vol, 50)

    X, Y = np.meshgrid(stock_prices, volatilities)

    Z = np.zeros_like(X)


    for i in range(len(volatilities)):
        for j in range(len(stock_prices)):

            model = BlackScholes(
                stock_prices[j],
                bs_model.exercise_price,
                bs_model.interest_rate,
                bs_model.time_to_expiration,
                volatilities[i]
            )

            call, put = model.calculate_call_put()

            if option == "call":
                Z[i, j] = call
            else:
                Z[i, j] = put


    fig = plt.figure(figsize=(10, 8))

    ax = fig.add_subplot(
        111,
        projection="3d"
    )


    surface = ax.plot_surface(
        X,
        Y,
        Z,
        cmap="viridis",
        edgecolor="none"
    )


    ax.set_title(
        f"3D Surface - {option.upper()} Price"
    )

    ax.set_xlabel(
        "Stock Price"
    )

    ax.set_ylabel(
        "Volatility"
    )

    ax.set_zlabel(
        "Option Price"
    )


    fig.colorbar(
        surface,
        shrink=0.5,
        aspect=10
    )


    fig.tight_layout()

    return fig

st.markdown("---")

st.subheader("3D Option Price Surface")


col1, col2 = st.columns(2)


with col1:

    call_surface = plot_3d_surface(
        bs_model,
        spot_min,
        spot_max,
        o_min,
        o_max,
        "call"
    )

    st.pyplot(
        call_surface,
        width="stretch"
    )


with col2:

    put_surface = plot_3d_surface(
        bs_model,
        spot_min,
        spot_max,
        o_min,
        o_max,
        "put"
    )

    st.pyplot(
        put_surface,
        width="stretch"
    )
