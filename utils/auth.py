# Authentication and attempt tracking

MAX_ATTEMPTS = 3

def check_login(password):
    return password == "admin123"

def increment_attempts():
    return min(MAX_ATTEMPTS, get_attempts() + 1)

def reset_attempts():
    import streamlit as st
    st.session_state.failed_attempts = 0

def get_attempts():
    import streamlit as st
    return st.session_state.get("failed_attempts", 0)
