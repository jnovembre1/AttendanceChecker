import streamlit as st
import os
import psycopg2

st.title("streamlit connected to PostgreSQL")
st.write("this is a test of streamlit.")

# environment variable
st.write("POSTGRES_USER:", os.getenv("POSTGRES_USER", "not set"))
