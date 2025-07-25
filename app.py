import streamlit as st
from utils.encryption import encrypt_data, decrypt_data, hash_passkey
from utils.auth import increment_attempts, reset_attempts, check_login
import json
import os

# Data file
DATA_FILE = "data/storage.json"

# Ensure storage file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

# Load existing data
def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Save updated data
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Session state init
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

stored_data = load_data()

st.set_page_config(page_title="Secure Data System")
st.title("🔒 Secure Data Encryption System")

menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Home":
    st.subheader("🏠 Welcome")
    st.write("Securely store and retrieve your data using passkeys.")

elif choice == "Store Data":
    st.subheader("📂 Store Data")
    user_data = st.text_area("Enter Data:")
    passkey = st.text_input("Enter Passkey:", type="password")

    if st.button("Encrypt & Save"):
        if user_data and passkey:
            hashed = hash_passkey(passkey)
            encrypted = encrypt_data(user_data)
            stored_data[encrypted] = {"encrypted_text": encrypted, "passkey": hashed}
            save_data(stored_data)
            st.success("✅ Data encrypted and saved!")
        else:
            st.error("⚠️ All fields required.")

elif choice == "Retrieve Data":
    st.subheader("🔍 Retrieve Data")
    encrypted_input = st.text_area("Paste Encrypted Data:")
    passkey = st.text_input("Enter Passkey:", type="password")

    if st.button("Decrypt"):
        if encrypted_input and passkey:
            hashed = hash_passkey(passkey)
            result = decrypt_data(encrypted_input, hashed, stored_data)
            if result:
                reset_attempts()
                st.success(f"✅ Decrypted Data: {result}")
            else:
                st.session_state.failed_attempts = increment_attempts()
                remaining = 3 - st.session_state.failed_attempts
                st.error(f"❌ Incorrect passkey! Attempts left: {remaining}")
                if st.session_state.failed_attempts >= 3:
                    st.warning("🔒 Too many failed attempts! Redirecting to Login...")
                    st.experimental_rerun()
        else:
            st.error("⚠️ All fields required.")

elif choice == "Login":
    st.subheader("🔑 Reauthorization Required")
    login_pass = st.text_input("Enter Admin Password:", type="password")

    if st.button("Login"):
        if check_login(login_pass):
            reset_attempts()
            st.success("✅ Reauthorized! Go to Retrieve Data.")
        else:
            st.error("❌ Incorrect password!")
