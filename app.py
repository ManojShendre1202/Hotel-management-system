import streamlit as st 
from streamlit_option_menu import option_menu
from src.HotelManagement.utils.common import fetch_admin  
from src.HotelManagement.components.authentication import *
from src.HotelManagement.components.admin_menu import *
from src.HotelManagement.components.user_menu import *

# Set page configuration
st.set_page_config(page_title="Hotel Management", page_icon="🏨", initial_sidebar_state='collapsed')


# Sidebar menu options
with st.sidebar:
    # Main menu options for Admin and User
    options = option_menu(
        menu_title="Menu",
        options=["Admin", "User"],
        icons=["person-vcard-fill", "people"],
        key="Main options"
    )

# Admin menu
if options == "Admin":
    if not session_state.logged_in_admin:
        # Check if admin is logged in
        if admin_login():  
            session_state.logged_in_admin = True

    if session_state.logged_in_admin:
        # Display admin menu options
        with st.sidebar:
            admin_choice = option_menu(
                menu_title="Admin",
                options=("Dashboard", "Room Management", "Room Service Management",
                         "User Management"),
                key="admin menu"
            )

        # Handle admin choices only if logged in
        if admin_choice == "Dashboard":
            dashboard()
        elif admin_choice == "Room Management":
            Room_Management()
        elif admin_choice == "User Management":
            User_management()
        elif admin_choice == "Room Service Management":
            room_service_management()
    else:
        st.write("Please login first to access admin options.")

    # Logout button for admin
    if session_state.logged_in_admin:
        if st.sidebar.button("Logout"):
            session_state.logged_in_admin = False
            st.success("Logged Out successfully!")

# User menu
if options == "User":
    with st.sidebar:
        if not session_state.logged_in_user:
            # Display login or sign-up options for users
            join = option_menu(
                menu_title="Menu",
                options=["Login", "Sign-Up"],
                key="Join"
            )

            if join == "Login":
                # Login functionality
                if login(): 
                    session_state.logged_in_user = True

            elif join == "Sign-Up":
                # Sign-up functionality
                sign_up()  

        # Logout button for user
        if session_state.logged_in_user:
            if st.sidebar.button("Logout", key="Logout"):
                session_state.logged_in_user = False
                st.success("Logged Out successfully!")

    # User menu options
    if session_state.logged_in_user:
        user_menu = option_menu(
            menu_title="User",
            options=("Home", "Room Availability", "Room Booking", "Room Service", "Feedback"),
            orientation="horizontal",
            key="User menu"
        )

        # Handle user menu options
        if user_menu == "Home":
            home()
        elif user_menu == "Room Availability":
            room_aval()
        elif user_menu == "Room Booking":
            room_booking()
        elif user_menu == "Room Service":
            room_service_table()
        elif user_menu == "Feedback":
            feedback_form()




