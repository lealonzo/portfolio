import streamlit as st

Home = st.Page("portfolio_overview.py", title="Home", icon=":material/home:")
crypto_plot = st.Page("crypto_plot.py", title="Plot Crypto", icon=":material/paid:")
test = st.Page("test.py", title="Feedback", icon=":material/chat:")


pg = st.navigation([Home, crypto_plot,test])
st.set_page_config(page_title="Lea's Portfolio", page_icon=":material/database:")
pg.run()