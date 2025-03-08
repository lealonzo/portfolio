import streamlit as st
import pandas as pd
import requests
import random
from streamlit_lottie import st_lottie

# Function to fetch Lottie animations
def load_lottie_url(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

# Function to fetch crypto asset pairs from Kraken
def fetch_crypto_pairs():
    url = "https://api.kraken.com/0/public/AssetPairs"
    response = requests.get(url)
    data = response.json()
    if data["error"]:
        st.error("Failed to fetch asset pairs.")
        return []
    return list(data["result"].keys())

def app():
    # Load Lottie animation for finance
    lottie_animation = load_lottie_url(
        "https://lottie.host/cede9c4c-7503-47e4-9e70-b9ed3b161106/hG12ecv3Na.json"
    )

    st.title("Finance Portfolio Dashboard 📊")
    st.write(
        """
        Track and analyze your cryptocurrency portfolio. 
        Select a start date, choose cryptocurrencies, and get real-time data insights.
        """
    )

    # Start Date Selection
    start_date = st.date_input("Select Start Date", pd.to_datetime("2021-01-01"))

    # Fetch available cryptocurrencies from Kraken API
    crypto_pairs = fetch_crypto_pairs()

    # Select cryptocurrencies to include in portfolio
    selected_pairs = st.multiselect("Select Cryptocurrencies", options=crypto_pairs, default=["XXBTZUSD", "XETHZUSD"])

    # Input the total initial value for the portfolio
    initial_total_value = st.number_input("Enter Initial Total Portfolio Value", min_value=0, value=10000)

    # Allow the user to set allocation for each selected cryptocurrency
    allocations = []
    for pair in selected_pairs:
        allocation = st.slider(f"Set Allocation for {pair}", 0, 100, 100 // len(selected_pairs))
        allocations.append(allocation)

    # Input the cash allocation
    cash_allocation = st.slider("Set Allocation for Cash", 0, 100, 10)  # Default cash allocation to 10%

    # Ensure the total allocation sums to 100% and adjust the cryptocurrency allocations accordingly
    total_allocation = sum(allocations) + cash_allocation
    if total_allocation != 100:
        ratio = (100 - cash_allocation) / sum(allocations) if sum(allocations) != 0 else 1
        allocations = [allocation * ratio for allocation in allocations]

    # Generate random initial and current values for cryptocurrencies
    initial_values = [(initial_total_value * allocation) / 100 for allocation in allocations]
    current_values = [random.randint(1000, 5000) for _ in range(len(selected_pairs))]

    # Generate random initial and current values for cash
    initial_cash_value = (initial_total_value * cash_allocation) / 100
    current_cash_value = initial_cash_value  # Assuming cash has no gain/loss for now

    # Calculate percentage gain/loss
    percentage_gain_loss = [
        ((current - initial) / initial) * 100 if initial != 0 else 0
        for initial, current in zip(initial_values + [initial_cash_value], current_values + [current_cash_value])
    ]

    # Create Portfolio DataFrame
    portfolio_data = {
        "Cryptocurrency": selected_pairs + ["Cash"],
        "Initial Value": [f"${value:,.2f}" for value in initial_values] + [f"${initial_cash_value:,.2f}"],
        "Allocation": [f"{allocation:.2f}%" for allocation in allocations] + [f"{cash_allocation:.2f}%"],
        "Current Value": [f"${value:,.2f}" for value in current_values] + [f"${current_cash_value:,.2f}"],
        "% Gain/Loss": [f"{gain_loss:.2f}%" for gain_loss in percentage_gain_loss]
    }
    
    portfolio_df = pd.DataFrame(portfolio_data)
    portfolio_df.set_index("Cryptocurrency", inplace=True)

    # Display Portfolio DataFrame
    st.write("### Portfolio Overview")
    st.dataframe(portfolio_df, use_container_width=True)

    # Calculate total current portfolio value
    total_current_value = sum(current_values) + current_cash_value
    st.write(f"### Total Current Portfolio Value: ${total_current_value:,.2f}")

    # Display animation
    if lottie_animation:
        st_lottie(
            lottie_animation,
            speed=1,
            reverse=False,
            loop=True,
            quality="high",
            height=400,
            width=700,
        )
    else:
        st.write("Unable to load animation.")

# Run the app
app()
