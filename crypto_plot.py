import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Function to fetch historical data from Kraken API
def fetch_historical_data(pair="XXBTZUSD", interval=1440):
    """
    Fetch historical OHLC data for the given pair.
    - pair: Kraken currency pair, e.g., 'XXBTZUSD'.
    - interval: Time interval in minutes (1440 = 1 day).
    """
    url = "https://api.kraken.com/0/public/OHLC"
    params = {"pair": pair, "interval": interval}
    response = requests.get(url, params=params)
    data = response.json()

    # Handle API errors
    if data["error"]:
        st.error(f"API Error: {data['error']}")
        return None

    # Extract OHLC data
    result = data["result"]
    if pair in result:
        ohlc_data = result[pair]
        # Convert to DataFrame
        df = pd.DataFrame(
            ohlc_data,
            columns=["Time", "Open", "High", "Low", "Close", "VWAP", "Volume", "Count"]
        )
        # Convert timestamps to datetime
        df["Time"] = pd.to_datetime(df["Time"], unit="s")
        return df
    else:
        st.error("No data found for the selected pair.")
        return None

# Function to fetch asset pair details from Kraken API
def fetch_asset_pair_details():
    """
    Fetch information about tradable asset pairs from Kraken API.
    """
    url = "https://api.kraken.com/0/public/AssetPairs"
    response = requests.get(url)
    data = response.json()

    # Handle API errors
    if data["error"]:
        st.error(f"API Error: {data['error']}")
        return None

    # Extract asset pairs information
    return data["result"]

# Streamlit app layout
st.title("Kraken API: Interactive OHLC Metric Viewer")

# Fetch asset pair details and extract pair names
asset_pairs = fetch_asset_pair_details()

if asset_pairs is not None:
    available_pairs = list(asset_pairs.keys())

    # Select cryptocurrency pair from Kraken API
    pair = st.selectbox(
        "Select a Cryptocurrency Pair",
        available_pairs
    )

    # Select the metric to plot
    metric = st.selectbox(
        "Select Metric to Plot",
        ["Open", "High", "Low", "Close", "VWAP", "Volume", "Count"]
    )

    # Fetch historical data
    st.write(f"Fetching historical data for {pair}...")
    historical_data = fetch_historical_data(pair)

    if historical_data is not None:
        # Filter data for the past 3 months
        three_months_ago = pd.Timestamp.now() - pd.DateOffset(months=3)
        filtered_data = historical_data[historical_data["Time"] >= three_months_ago]

        # Ensure the selected metric is numeric
        filtered_data[metric] = filtered_data[metric].astype(float)

        # Interactive Plot using Plotly
        #st.write(f"### {metric} for the Past 3 Months")
        fig = px.line(
            filtered_data,
            x="Time",
            y=metric,
            title=f"3-Month {metric} for {pair}",
            labels={metric: f"{metric} (USD)", "Time": "Date"},
            line_shape="linear"
        )

        # Correct the hovertemplate to display the correct details
        fig.update_traces(
            line_color="purple", 
            hovertemplate="<b>Date:</b> %{x}<br><b>" + metric + "</b>: $%{y:.2f}<extra></extra>"
        )
        fig.update_layout(hovermode="x unified")

        # Display interactive plot
        st.plotly_chart(fig, use_container_width=True)

    # Display asset pair details
    st.write("### Asset Pair Details")
    asset_info = asset_pairs[pair]

    # Prepare the data for the DataFrame
    asset_details = {
        "Base Currency": [asset_info['base']],
        "Quote Currency": [asset_info['quote']],
        "Symbol": [asset_info['altname']],
        "Pair ID": [asset_info.get('pairid', 'N/A')],
        "Volume Information": [asset_info.get('volume', 'N/A')]
    }

    # Convert the dictionary to a DataFrame
    asset_df = pd.DataFrame(asset_details)

    # Set the "Base Currency" as the index
    asset_df.set_index('Base Currency', inplace=True)

    # Display the DataFrame
    st.dataframe(asset_df, use_container_width=True)

else:
    st.error("Failed to fetch asset pairs. Please try again later.")
