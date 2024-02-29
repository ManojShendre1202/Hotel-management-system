import streamlit as st
from streamlit_option_menu import option_menu
from src.HotelManagement.utils.common import *
import pandas as pd
from src.HotelManagement.components.admin_menu import Room_Management

# Function to check if the room id is present in the list got from the database
def check_room_id(room_id):
    room_ids = get_room_ids()
    if room_ids is not None:
        room_ids = [row[0] for row in room_ids] 
        if room_id in room_ids:
            return True
        else:
            return False
    else:
        print("Unable to retrieve room IDs from the database.")

def home():
    st.header("Welcome to Hotel Vista 💫", divider="rainbow")
    st.image("vista.jpg")

def room_aval():
    data, column_names = fetch_room_data()
    
    if data:
        df = pd.DataFrame(data, columns=column_names)
        st.subheader(":green[All the Avaliable rooms are shown here]")
        st.write(df) 
        st.info("Please note the room ID for further Booking")
    else:
        st.warning("No data found in the database.")

def room_booking():
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(":blue[Name]", placeholder="Please Enter your name").lower()
        email = st.text_input(":blue[Email]", placeholder="Please enter your email")
        phone_number = st.text_input(":blue[Phone number]",placeholder="Enter your phone number")
        address = st.text_input(":blue[Address]", placeholder="Enter your address")
        id_type = st.selectbox(":blue[ID Type]", ("Aaddhar card","Pan card","Driving Licence","Passport"))
        id_number = st.text_input(":blue[ID number]", placeholder=f"Enter {id_type} number")

        if name and email and phone_number and address and id_type and id_number:
            with col2:
                room_id = st.text_input(":blue[Room ID]", placeholder="Please enter the room ID you selected.").lower()
                check_in = st.date_input(":blue[Check-in]")
                check_out = st.date_input(":blue[Check-out]")
                if check_out < check_in:
                    st.warning("Check-out date cannot be before Check-in date.")
                else:
                    number_of_days = (check_out - check_in).days
                    st.write(":green[Number of days:]", number_of_days)
                guests = st.number_input(":blue[Number of Guests]", step = 1)
                room_type = st.selectbox(":blue[Room Type]",("Single Bedroom","Double Bed Room","Cottage","Resort"))
                
                if st.button("submit", key="Room_final_button"):
                    if check_in and check_out and guests and room_type:
                            room_status_all = fetch_room_status(room_id)
                            if room_status_all:
                                availability, room_status = room_status_all
                                if availability == "Available" and room_status == "Clean" or "Available":
                                    if not check_room_id(room_id):
                                        base_price = fetch_room_price(room_type, room_id)
                                        price = base_price * number_of_days
                                        insert_booking_details(name, email, phone_number, address, id_type, id_number, check_in, check_out, guests, room_type, room_id)
                                        update_room_availability(room_id, "Not available")
                                        booking_id = fetch_booking_id(name, email)
                                        st.info(f"Total price = {price}")
                                        st.info(f"Book ID = {booking_id}")
                                        st.info("Booking is done successfully")
                                    else:
                                        st.error("Error: Room ID already exists in the list.")
                                else:
                                    st.error("We apologize, but the room is currently unavailable for booking. Please visit the Room Availability section to check for available rooms.")
                            else:
                                st.error("Room is not available for booking. Please select another room.")


def get_menu(menu_name):
    if menu_name == "Breakfast":
        return get_breakfast_menu()
    elif menu_name == "LunchDinner":
        return get_lunch_dinner_menu()
    elif menu_name == "SnacksBeverages":
        return get_snacks_beverages_menu()


def calculate_price(base_price, quantity):
    return base_price * quantity

def room_service_table():
    st.info("For any further details please contact 8884812422")
    room_id = st.text_input(":blue[Enter your Room ID]").lower()
    name = st.text_input(":blue[Name]",placeholder="Please Enter your name").lower()
    with st.sidebar:
        service_menu = option_menu(
            menu_title="Room Service",
            options=("Food Order","Housekeeping","Room Amenities Requests","Concierge Assistance")
        )

    if service_menu == "Food Order":
        selected_items = {}
        total_order_price = 0

        # Define tabs
        tb1, tb2, tb3, tb4 = st.tabs(["Breakfast", "Lunch/Dinner", "Snacks", "Order details"])

        with tb1:
            menu_name = "Breakfast"
            menu_items = get_menu(menu_name)

            st.header(f"{menu_name} Menu:")
            for item in menu_items:
                item_name, base_price = item
                quantity = st.number_input(f"{item_name}:", min_value=0, max_value=10, step=1)
                total_price = calculate_price(base_price, quantity)
                st.write(f"- {item_name}: Quantity - {quantity}, Total Price - ${total_price:.2f}")
                selected_items[item_name] = quantity
                total_order_price += total_price

        with tb2:
            menu_name = "LunchDinner"
            menu_items = get_menu(menu_name)

            st.header(f"{menu_name} Menu:")
            for item in menu_items:
                item_name, base_price = item
                quantity = st.number_input(f"{item_name}:", min_value=0, max_value=10, step=1)
                total_price = calculate_price(base_price, quantity)
                st.write(f"- {item_name}: Quantity - {quantity}, Total Price - ${total_price:.2f}")
                selected_items[item_name] = quantity
                total_order_price += total_price

        with tb3:
            menu_name = "SnacksBeverages"
            menu_items = get_menu(menu_name)

            st.header(f"{menu_name} Menu:")
            for item in menu_items:
                item_name, base_price = item
                quantity = st.number_input(f"{item_name}:", min_value=0, max_value=10, step=1)
                total_price = calculate_price(base_price, quantity)
                st.write(f"- {item_name}: Quantity - {quantity}, Total Price - ${total_price:.2f}")
                selected_items[item_name] = quantity
                total_order_price += total_price
        
        with tb4:
            cl1, cl2 = st.columns(2)
            selected_items_list = {item: quantity for item, quantity in selected_items.items() if quantity >= 1}

            with cl1:
                st.subheader("Selected Items", divider='rainbow')
                items = [item for item in selected_items_list.keys()]
                food_items = ', '.join(items)
                for item in items:
                    st.info(item)
            
            with cl2:
                st.subheader("Quantities", divider='rainbow')
                for quantity in selected_items_list.values():
                    st.info(quantity)
            # Display total order price and submit button
            st.info(f"Total Order Price: Rs{total_order_price:.2f}")
            if st.button("Submit", key="Final"):
                if insert_food_service_details(name, room_id, food_items, total_order_price):
                    st.success("Order Confirmed!")
    

    elif service_menu == "Housekeeping":
        housekeeping_service = st.selectbox("Please select the housekeeping service you require", ("Room Cleaning", "Bathroom Cleaning", "Trash Removal", "Special Requests Handling"))
        if housekeeping_service:
            house_keeping_note = st.text_input("Additional Note", placeholder="Please enter any special requests you may have")
            if st.button("Submit", key = "House keeping"):
                insert_housekeeping(housekeeping_service, house_keeping_note, room_id)
                st.success("House keeping will be available in couple of Minutes, Thank  You!")

    elif service_menu == "Room Amenities Requests":
        selected_request = st.radio("Please select your amenity request", ["Extra Bedding", "Toiletries", "Mini Bar Items", "Electronic Items Request"])
        if selected_request:
            Room_amenities_note = st.text_input("Additional Details", placeholder="Please provide any additional details about your request")
            if st.button("Submit", key = "Amenities"):
                insert_room_amenities(selected_request, Room_amenities_note, room_id)
                st.success("Amenities will be available in couple of minutes, Thank You!")

    elif service_menu == "Concierge Assistance":
        language = st.selectbox("Please select your preferred language", ("Kannada", "Hindi", "English", "Other"))
        if language == "Other":
            language = st.text_input("Other Language", placeholder="Please specify your preferred language")
        if language:
            travel_asst_note = st.text_input("Additional details", placeholder="Please provide any additional details about your request")
            if st.button("Submit", key = "Travel"):
                insert_travel_assistance(language, travel_asst_note, room_id)
                st.success("Thank you for your selection. We will arrange for a tourist expert to assist you.")


import streamlit as st

def feedback_form():
    st.subheader(":green[Insight Echo: Your Voice Shapes Our Path]", divider='rainbow')
    room_id = st.text_input("room_id", placeholder="Please Etner your room id", key = "Feedback")
    overall_exp = st.slider(":blue[Rate your overall experience (1-10)]", 1, 10, key="overall_exp")
    ui_feedback = st.text_area(":blue[Feedback on user interface]", key="ui_feedback")
    features_feedback = st.text_area(":blue[Feedback on features]", key="features_feedback")
    performance = st.slider(":blue[Rate the app's performance (1-10)]", 1, 10, key="performance")
    bugs_report = st.text_area(":blue[Report any bugs or technical issues]", key="bugs_report")
    suggestions = st.text_area(":blue[Suggestions for improvement]", key="suggestions")
    customer_service_feedback = st.text_area(":blue[Feedback on customer service]", key="customer_service_feedback")
    additional_comments = st.text_area(":blue[Any additional comments]", key="additional_comments")

    if st.button("Submit Feedback", key="submit_button"):
        if insert_feedback(overall_exp, ui_feedback, features_feedback, performance, bugs_report, suggestions, customer_service_feedback, additional_comments, room_id):
            st.success("Thank You for you valueable feedback")




