import streamlit as st
from streamlit_option_menu import option_menu
from src.HotelManagement.utils.common import *
import pandas as pd
from datetime import datetime, timedelta


def Dashboard():
    pass


def Room_Management():
    # Display menu options for room management
    menu = option_menu(
        menu_title="Room Management",
        options=("Add/Edit Rooms", "Update rooms status"),
        orientation='horizontal'
    )
    
    # Handle Add/Edit Rooms option
    if menu == "Add/Edit Rooms":
        room_menu = st.selectbox(":blue[Modify Rooms]", ("Add New Rooms", "Edit Existing Rooms"), key="room_menu")
        
        # Add New Rooms
        if room_menu == "Add New Rooms":
            # Display input fields for adding a new room
            room_id = st.text_input(":blue[Room Id]").lower()
            room_type = st.selectbox(":blue[Room Type]", ("Single Bedroom", "Double Bed Room", "Cottage", "Resort"))
            capacity = st.number_input(":blue[Capacity]", step=1)
            description = st.text_input(":blue[Description]")
            amenities = st.multiselect(":blue[Amenities]", ["Wifi", "TV", "AC", "Room service", "Smoking", "Pets allowed"])
            amenities_text = ", ".join(amenities)
            per_night_price = st.number_input(":blue[Price Per night]", step=1)
            availability = st.selectbox(":blue[Availability]", ("Available", "Not available"))
            room_status = st.selectbox(":blue[Room Status]", ("Clean", "Dirty", "Under Maintenance", "Out of Order", "Occupied", "Avaliable"))
            notes = st.text_input(":blue[Notes]", placeholder="Write any note for the room status, if needed!")

            # Add room button
            if st.button("Add Room", key="Add room"):
                if room_id and room_type and capacity and description and amenities and per_night_price and availability and room_status:
                    if insert_rooms(room_id, room_type, capacity, description, availability, per_night_price, amenities_text, room_status, notes):
                        st.success("Room added successfully!")
                    else:
                        st.error("Failed to add room. Please check logs for details.")
            else:
                st.error("Please fill in all the required fields.")
        
        # Edit Existing Rooms
        if room_menu == "Edit Existing Rooms":
            # Display input fields for editing an existing room
            room_id = st.text_input(":blue[Room Id]").lower()
            room_type = st.selectbox(":blue[Room Type]", ("Single Bedroom", "Double Bed Room", "Cottage", "Resort"))
            capacity = st.number_input(":blue:[Capacity]", step=1)
            description = st.text_input(":blue[Description]")
            amenities = st.multiselect(":blue[Amenities]", ["Wifi", "TV", "AC", "Room service", "Smoking", "Pets allowed"])
            amenities_text = ", ".join(amenities)
            per_night_price = st.number_input(":blue[Price Per night]", step=1)
            availability = st.selectbox(":blue[Availability]", ("Available", "Not available"))
            room_status = st.selectbox(":blue[Room Status]", ("Clean", "Dirty", "Under Maintenance", "Out of Order", "Occupied", "Avaliable"))
            notes = st.text_input(":blue[Notes]", placeholder="Write any note for the room status, if needed!")

            # Update rooms button
            if st.button("Update rooms", key="Update rooms"):
                if update_rooms(room_id, room_type, capacity, description, availability, per_night_price, amenities_text, room_status, notes):
                    st.success("Update successful")
                else:
                    st.error("Failed to update room. Please check logs for details.")

    # Handle Update rooms status option
    if menu == "Update rooms status":
        room_id = st.text_input(":blue[Room Id]").lower()
        room_status = st.selectbox(":blue[Room Status]", ("Clean", "Dirty", "Under Maintenance", "Out of Order", "Occupied", "Available"))
        availability = st.selectbox(":blue[Availability]", ("Available", "Not available"))

        # Update button
        if st.button("Update", key="Room_status"):
            if update_room_status(room_id, room_status, availability):
                st.success("Room Status Updated successfully")
            else:
                st.error("Failed to update room status. Please check logs for details.")

        data, column_names = get_rooms_with_unavailable_status()
        if data:
            df = pd.DataFrame(data, columns=column_names[0:4])
            st.write(df) 
        else:
            st.warning("No data found in the database.")


def room_service_management():
    tb1, tb2 = st.tabs(["Food","Others"])
    with tb1:
        data, column_names = get_food_service_details()
        
        if data:
            df = pd.DataFrame(data, columns=column_names)
            st.write(df) 
        else:
            st.warning("No data found in the database.")
    with tb2:
        data, column_names = get_room_service_table_details()
        
        if data:
            df = pd.DataFrame(data, columns=column_names)
            st.write(df) 
        else:
            st.warning("No data found in the database.")

def filter_dataframe(df, query):
    return df[df['name'].str.contains(query, case=False) |
              df['email'].str.contains(query, case=False) |
              df['room_id'].astype(str).str.contains(query, case=False)]

def User_management():
    user_manage = option_menu(menu_title="User Management", 
                options=("View", "Edit User", "Check-in/Check-out"),
                orientation="horizontal")
    
    # Handle User Management options
    if user_manage == "View":
        data, column_names = get_booking_details()
        if data:
            df = pd.DataFrame(data, columns=column_names)
            
            # Search bar
            search_query = st.text_input(':blue[Search by name, email, or room_id]', '')
            
            # Filter DataFrame based on search query
            filtered_df = filter_dataframe(df, search_query)
            
            # Display filtered DataFrame
            st.write(filtered_df) 
        else:
            st.warning("No data found in the database.")
        
    if user_manage == "Edit User":
        booking_id = st.number_input(":blue[Booking_id]", step = 1)
        name = st.text_input(":blue[Name]", placeholder="Please Enter your name").lower()
        id_type = st.selectbox(":blue[ID Type]", ("Aaddhar card","Pan card","Driving Licence","Passport"))
        id_number = st.number_input(":blue[ID number]", placeholder=f"Enter {id_type} number", step = 1)

        if st.button("Submit", key = "Edit user"):
            if update_user_details(booking_id, name, id_type, id_number):
                st.success("User Details Updated sucessfully!")

    if user_manage == "Check-in/Check-out":
        book_id = st.text_input(":blue[booking_id]", placeholder="Enter booking Id")
        ph_num = st.text_input(":blue[Phone_number]", placeholder="Enter phone number")
        if book_id or ph_num:
            fetch_room_details_by_phone(book_id, ph_num)
            data, column_names = get_booking_details()
            if data:
                df = pd.DataFrame(data, columns=column_names)
                st.write(df) 
                st.subheader("Check-in and change room status")
                with st.container():
                    room_id = st.text_input(":blue[Room Id]", key='room_id').lower()
                    room_status = st.selectbox(":blue[Room Status]", ("Clean", "Dirty", "Under Maintenance", "Out of Order", "Occupied", "Available"), key='room_status')
                    availability = st.selectbox(":blue[Availability]", ("Available", "Not available"), key='availability')
                    checked_in = st.selectbox(":blue[Check-in]", ("Check-in", "Check-out"), key='checked_in')

                    if room_id and room_status and availability and checked_in:
                        time = st.date_input(":blue[Check-in date]" if checked_in == "Check-in" else ":blue[Check-out date]", key='time')
                        button_label = "Check-in" if checked_in == "Check-in" else "Check-out"

                        if st.button("Submit", key='submit_button'):
                            if update_room_status(room_id, room_status, availability):
                                update_user_check_in(time, book_id, ph_num)
                                st.success("Room Status Updated successfully")
                            else:
                                st.error("Failed to update room status. Please check logs for details.")

            else:
                st.warning("No data found in the database.")
        else:
            st.warning("Please Enter credientials")


def filter_data_by_date(data, date_range):
    end_date = datetime.today().date()  # Convert to datetime.date
    if date_range == "Today":
        start_date = end_date
    elif date_range == "1 month":
        start_date = end_date - timedelta(days=30)
    elif date_range == "3 months":
        start_date = end_date - timedelta(days=90)
    elif date_range == "6 months":
        start_date = end_date - timedelta(days=180)
    elif date_range == "12 months":
        start_date = end_date - timedelta(days=365)
    else:
        return data
    return [row for row in data if start_date <= row[3] <= end_date]  # Assuming index 3 is the check_in date

    
def dashboard():
    feedback_data, feedback_columns = get_all_from_feedback()
    booking_data, booking_columns = get_complete_booking_details()
    # tb1, tb2 = st.tabs(["Table", "Graphs"])

    # with tb1:
    st.subheader(":green[Booking Details]")
    date_range_booking = st.selectbox(":blue[Select time period for booking details:]", ["Today", "1 month", "3 months", "6 months", "12 months"], key = "Table")
    filtered_booking_data = filter_data_by_date(booking_data, date_range_booking)
    df_booking = pd.DataFrame(filtered_booking_data, columns=booking_columns)
    st.write(df_booking)

    count = len(filtered_booking_data)
    st.info(f"Total booking: {count}")

    st.subheader(":green[Feedback Details]")
    df_feedback = pd.DataFrame(feedback_data, columns=feedback_columns)
    st.write(df_feedback)

    # with tb2:
    #     booking_table = pd.DataFrame(booking_data, columns=booking_columns)

    #     # Group by check-in date and count the number of room bookings for each date
    #     booking_count_by_date = booking_table.groupby('check_in').size().reset_index(name='booking_count')

    #     # Plot the line chart
    #     st.line_chart(data=booking_count_by_date.set_index('check_in'))


           


    
    