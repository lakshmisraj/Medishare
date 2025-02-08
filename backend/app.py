import streamlit as st
from auth import register_user, login_user

st.title("MediShare - Patient Portal")

# Toggle between Login & Registration
option = st.sidebar.radio("Navigation", ["Login", "Register", "Profile"])

if option == "Register":
    st.header("Register a New Account")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if name and email and password:
            if register_user(name, email, password):
                st.success("Registration Successful! You can now log in.")
            else:
                st.error("Email already exists.")
        else:
            st.error("All fields are required!")

elif option == "Login":
    st.header("Login to Your Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.success(f"Welcome, {user['name']}!")
            st.session_state["user"] = user  # ✅ Store user session
        else:
            st.error("Invalid email or password.")

elif option == "Profile":
    if "user" in st.session_state:
        st.header(f"Welcome, {st.session_state['user']['name']}!")
        st.write(f"**Email:** {st.session_state['user']['email']}")
    else:
        st.warning("You must log in to view your profile.")