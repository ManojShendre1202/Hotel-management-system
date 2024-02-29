import streamlit as st
from src.HotelManagement.utils.common import *


class SessionState:
    def __init__(self):
        self.logged_in_user = False
        self.logged_in_admin = False


session_state = SessionState()


def logout_user():
    session_state.logged_in_user = False
    st.write("Logged out successfully!")


def admin_logout():
    session_state.logged_in_admin = False
    st.write("Logged out successfully!")


def sign_up():
    with st.container():
        st.subheader(':green[Sign Up]')
        username = st.text_input(':blue[Username]', placeholder='Enter your username')
        email = st.text_input(':blue[Email]', placeholder='Enter your email')
        phone_number = st.text_input("Phone number")
        password1 = st.text_input(':blue[Password]', type='password', placeholder='Enter your password')
        password2 = st.text_input(':blue[Re-enter Password]', type='password', placeholder='Re-enter your password')

        if st.button("Sign Up"):
            if username and email and password1 and password2:
                if len(password1) >= 6:
                    if password1 == password2:
                        if valid_username(username):
                            if username not in fetch_username():
                                if valid_email(email):
                                    if email not in fetch_email():
                                        insert_user(username, email, password2, phone_number)
                                        st.success("Account added successfully")
                                        st.balloons()
                                        login()
                                    else:
                                        st.error('Email already exists')
                                else:
                                    st.warning('Invalid email format')
                            else:
                                st.error('Username already exists')
                        else:
                            st.warning('Invalid username')
                            logger.info(f"Invalid username {username}")
                    else:
                        st.warning("Passwords don't match")
                else:
                    st.warning('Password should contain at least 6 characters')
            else:
                st.warning('All fields are required')


def login():
    with st.container():
        with st.sidebar:
            email = st.text_input(":blue[Email]", placeholder="Enter your email", key = "auth")
            password = st.text_input(":blue[Password]", placeholder="Enter your password", type="password", key = "userpass")

            if st.button("Login"):
                if email and password:
                    user_data = fetch_user(email)
                    if user_data:
                        emails = user_data[1]
                        passwords = user_data[2]
                        if email == emails and password == passwords:
                            session_state.logged_in_user = True
                            return True
                        else:
                            st.error("Invalid password")
                            print(password, passwords)
                    else:
                        st.error("invalid email")
                elif email:
                    st.warning("Enter your password")
                else:
                    st.warning("Enter your username")


def admin_login():
    with st.container():
        with st.sidebar:
            name = st.text_input("name", placeholder="Enter your username")
            password = st.text_input("Password", placeholder="Enter your password", type="password")

            if st.button("Login"):
                if name and password:
                    admin_data = fetch_admin(name)
                    if admin_data:
                        names = admin_data[0]
                        passwords = admin_data[2]
                        if name == names:
                            if password == passwords:
                                session_state.logged_in_admin = True
                                return True
                            else:
                                st.error("Wrong password")
                        else:
                            st.error("invalid name")

                elif name:
                    st.warning("Enter your password")
                else:
                    st.warning("Enter your username")
