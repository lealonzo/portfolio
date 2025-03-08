import streamlit as st
from streamlit_lottie import st_lottie
import requests

# Function to load Lottie animation
def load_lottie_url(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

# Streamlit Feedback Page
def feedback_page():
    st.title("Thank you for visiting my page!")

    # Display a cool animation for feedback
    lottie_animation = load_lottie_url(
        "https://lottie.host/a981940b-1ead-4646-9543-ca5b63c08a09/xBcgm283fQ.json"  # A feedback animation URL
    )

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
    
    # Display a message indicating where to send feedback
    st.write("""
        💬 **I'd love to hear from you!**  
        I'll be adding more side projects that would interest me to this page.
        \nIf you want to keep in touch, please send your comments to:  
        **leamonicaalonzo@gmail.com**        
    """)

# Run the feedback page
feedback_page()
