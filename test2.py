import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
import requests

# Function to fetch Lottie animations
def load_lottie_url(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

def app():
    # Load Lottie animation for finance
    lottie_animation = load_lottie_url(
        #"https://assets4.lottiefiles.com/packages/lf20_5ngs2ksb.json"
        "https://lottie.host/cede9c4c-7503-47e4-9e70-b9ed3b161106/hG12ecv3Na.json"
    )

    st.title("Finance Portfolio Dashboard 📊")
    st.write(
        """
        Track and analyze your financial assets with ease. 
        Navigate through the app to see detailed portfolio insights and real-time cryptocurrency data.
        """
    )
    # Add portfolio details
    st.subheader("Portfolio Details")
    # Original dictionary
    portfolio_data = {
        "Stocks": {"Value": "$10,000", "Allocation": "40%"},
        "Crypto": {"Value": "$5,000", "Allocation": "20%"},
        "Bonds": {"Value": "$5,000", "Allocation": "40%"}
    }

    # Convert dictionary to DataFrame
    portfolio_df = pd.DataFrame(portfolio_data).T  # Transpose for better readability

    # Display the DataFrame in Streamlit
    st.dataframe(portfolio_df, use_container_width=True)

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

app()