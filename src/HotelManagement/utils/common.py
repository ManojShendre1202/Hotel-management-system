import mysql.connector
import os
import re
from src.HotelManagement import logger
from mysql.connector import (connection, cursor)
import streamlit as st
from dotenv import load_dotenv


load_dotenv()

def insert_user(username, email, password, phone_number):
    connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
    cursor = connection.cursor()
    cursor.execute("INSERT INTO user (username, email, password, phone_number) VALUES (%s, %s, %s, %s)", (username, email, password, phone_number))
    connection.commit()
    cursor.close()
    connection.close()
    
# fetch user data
def fetch_user(email):
        connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
        cursor = connection.cursor()
        cursor.execute("SELECT username, email, password FROM user WHERE email = %s", (email,))
        user_data = cursor.fetchone()
        if user_data:
            return user_data
        else:
            return None

# fetch usernames from the database
def fetch_username():
        connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
        cursor = connection.cursor()
        cursor.execute("SELECT username FROM user") 
        usernames = [row[0] for row in cursor.fetchall()]
        username_dict = {'username': usernames}
        cursor.close()
        connection.close()
        return username_dict


# fetch emails from the database
def fetch_email():
        connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
        cursor = connection.cursor()
        cursor.execute("SELECT email FROM user") 
        emails = [row[0] for row in cursor.fetchall()]
        email_dict = {'email': emails}
        cursor.close()
        connection.close()
        return email_dict


# check for the valid username entered by the user
def valid_username(username):
    pattern = r'^[a-zA-Z][a-zA-Z0-9_-]{2,15}$'
    return re.match(pattern, username) is not None


# check for the valid email entered by the user
def valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def fetch_admin(name):
    connection = mysql.connector.connect(
        host=os.getenv("host"),
        database=os.getenv("database"),
        user=os.getenv("user"),
        password=os.getenv("password"),
        auth_plugin=os.getenv("auth_plugin")
    )
    cursor = connection.cursor()
    cursor.execute("SELECT name, email, password FROM admin WHERE name = %s", (name,))
    admin_data = cursor.fetchone()
    if admin_data:
        cursor.close()
        connection.close()
        return admin_data
    else:
        cursor.close()
        connection.close()
        return None


def insert_rooms(room_id, room_type, capacity, description, availability, per_night_price, amenities, room_status, notes):
        connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
        cursor = connection.cursor()
        cursor.execute("INSERT INTO rooms (room_id, room_type, capacity, description, availability, per_night_price, amenities, room_status, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (room_id, room_type, capacity, description, availability, per_night_price, amenities, room_status, notes))
        connection.commit()
        cursor.close()
        connection.close()
        return True


def update_rooms(room_id, room_type, capacity, description, availability, per_night_price, amenities, room_status, notes):
        connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
        cursor = connection.cursor()
        cursor.execute("UPDATE rooms SET room_type = %s, capacity = %s, description = %s, availability = %s, per_night_price = %s, amenities = %s, room_status = %s, noptes = %s WHERE room_id = %s", (room_type, capacity, description, availability, per_night_price, amenities, room_status, notes, room_id))
        connection.commit()
        cursor.close()
        connection.close()
        return True


def update_room_status(room_id, room_status, availablity):
        connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
        cursor = connection.cursor()
        cursor.execute("UPDATE rooms SET room_status = %s, availability = %s WHERE room_id = %s", (room_status, availablity, room_id))
        connection.commit()
        cursor.close()
        connection.close()
        return True


def fetch_room_data():
        connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
        cursor = connection.cursor()
        cursor.execute("SELECT room_id, room_type, availability, per_night_price, amenities, room_status, description  FROM rooms WHERE availability = 'available' and (room_status = 'Clean' OR room_status = 'Available')")  
        data = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]
        cursor.close()
        connection.close()
        return data, column_names


def insert_booking_details(name, email, phone_number, address, id_type, id_number, check_in, check_out, guests, room_type, room_id):
        connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
        cursor = connection.cursor()
        cursor.execute("INSERT INTO booking_details (name, email, phone_number, address, id_type, id_number, check_in, check_out, guests, room_type, room_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (name, email, phone_number, address, id_type, id_number, check_in, check_out, guests, room_type, room_id))

        connection.commit()
        cursor.close()
        connection.close()
        return True


def fetch_room_price(room_type, room_id):
        connection = mysql.connector.connect(
            host = "localhost",
            database = "hotel_management",
            user = "root",
            password = "mypass@2002",
            auth_plugin="mysql_native_password"
        )

        cursor = connection.cursor()
        cursor.execute("SELECT per_night_price FROM rooms WHERE room_type = %s AND room_id = %s", (room_type, room_id))
        price = cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()
        if price:
            return price[0]
        else:
            return None
        
def fetch_booking_id(name, email):
    try:
        connection = mysql.connector.connect(
            host=os.getenv("host"),
            database=os.getenv("database"),
            user=os.getenv("user"),
            password=os.getenv("password"),
            auth_plugin=os.getenv("auth_plugin")
        )
        cursor = connection.cursor(buffered=False)  
        cursor.execute("SELECT Booking_id FROM booking_details WHERE name = %s AND email = %s", (name, email))
        booking_id = cursor.fetchone()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None  # Return None on error 
    finally:
        if cursor:  # Check if cursor exists
            cursor.close()
        if connection:  # Check if connection exists
            connection.close() 

    return booking_id

def fetch_room_status(room_id):
    connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
    cursor = connection.cursor()
    cursor.execute("SELECT availability, room_status FROM rooms WHERE room_id = %s", (room_id,))
    status = cursor.fetchall()
    cursor.close()
    connection.close()
    
    if status:
        availability, room_status = status[0]  # Access the first tuple in the list
        return availability, room_status
    else:
        return None

def get_room_ids():
        connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
        cursor = connection.cursor()
        query = "SELECT room_id FROM booking_details"
        cursor.execute(query)
        room_ids = cursor.fetchall() 
        return room_ids

def update_room_availability(room_id, new_availability):
        connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
        cursor = connection.cursor()
        cursor.execute("UPDATE rooms SET availability = %s WHERE room_id = %s", (new_availability, room_id))
        connection.commit()
        cursor.close()
        connection.close()
        logger.info(f"Room availability updated successfully for room ID {room_id}. New availability: {new_availability}")
        return True


def get_breakfast_menu():
    connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
    cursor = connection.cursor()
    cursor.execute("SELECT item_name, item_price FROM breakfast")
    breakfast_items = cursor.fetchall()
    breakfast_menu_items = [(item[0], float(item[1])) for item in breakfast_items]
    cursor.close()
    connection.close()
    return breakfast_menu_items


def get_lunch_dinner_menu():
    connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
    cursor = connection.cursor()
    cursor.execute("SELECT item_name, item_price FROM lunchDinner")
    lunch_dinner_items = cursor.fetchall()
    dinner_menu_items = [(item[0], float(item[1])) for item in lunch_dinner_items]
    cursor.close()
    connection.close()
    return dinner_menu_items

def get_snacks_beverages_menu():
    connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
    cursor = connection.cursor()
    cursor.execute("SELECT item_name, item_price FROM snacksBeverages")
    snacks_beverages_items = cursor.fetchall()
    snacks_menu_items = [(item[0], float(item[1])) for item in snacks_beverages_items]
    cursor.close()
    connection.close()
    return list(snacks_menu_items)

def insert_food_service_details(name, room_id, item, total_order_price):
    connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
    cursor = connection.cursor()

    cursor.execute("INSERT INTO room_service_table (name, room_id, food, price) VALUES (%s, %s, %s, %s)", (name, room_id, item, total_order_price))
    connection.commit()
    cursor.close()
    connection.close()
    return True

def insert_housekeeping(house_keeping, hk_note, room_id):
    connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
    cursor = connection.cursor()

    # Example SQL query - replace with your specific query
    cursor.execute("INSERT INTO room_service_table (house_keeping, hk_note, room_id) VALUES (%s, %s, %s)", (house_keeping, hk_note, room_id))
    
    connection.commit()
    cursor.close()
    connection.close()
    return True

def insert_room_amenities(room_amenities, amenities_notes, room_id):
    connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
    cursor = connection.cursor()

    # Example SQL query - replace with your specific query
    cursor.execute("INSERT INTO room_service_table (room_amenities, amenities_notes, room_id) VALUES (%s, %s, %s)", (room_amenities, amenities_notes, room_id))
    
    connection.commit()
    cursor.close()
    connection.close()
    return True

def insert_travel_assistance(travel_assistance, assistance_note, room_id):
    connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
    cursor = connection.cursor()
    cursor.execute("INSERT INTO room_service_table (travel_assistance, assistance_note, room_id) VALUES (%s, %s, %s)", (travel_assistance, assistance_note, room_id))
    connection.commit()
    cursor.close()
    connection.close()
    return True

def get_room_service_table_details():
    connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM room_service_table")
    room_service_table_requests = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    cursor.close()
    connection.close()
    return room_service_table_requests, column_names


def get_food_service_details():
    connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
    cursor = connection.cursor()
    cursor.execute("SELECT name, room_id, food, price FROM room_service_table")
    room_service_table_requests = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    cursor.close()
    connection.close()
    return room_service_table_requests, column_names



def get_rooms_with_unavailable_status():
    connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
    cursor = connection.cursor()
    sql_query = """
                SELECT room_id, availability, room_status
                FROM rooms
                WHERE availability = 'Not available'
                OR room_status IN ('Dirty', 'Under Maintenance', 'Out of Order', 'Occupied');
                """
    cursor.execute(sql_query)
    data = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    cursor.close()
    connection.close()
    return data, column_names


def get_booking_details():
    connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM booking_details")
    data = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    cursor.close()
    connection.close()
    return data, column_names


def update_user_details(booking_id, name, id_type, id_number):
        connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
        cursor = connection.cursor()
        cursor.execute("UPDATE booking_details SET name = %s, id_type = %s, id_number = %s WHERE booking_id = %s", (name, id_type, id_number, booking_id))
        connection.commit()
        cursor.close()
        connection.close()
        return True

def fetch_room_details_by_phone(book_id, phone_number):
    connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM booking_details WHERE booking_id = %s OR phone_number = %s", (book_id, phone_number))
    data = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    cursor.close()
    connection.close()
    return data, column_names

def update_user_check_in(check_in, booking_id, phone_number):
        connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
        cursor = connection.cursor()
        cursor.execute("UPDATE booking_details SET check_in = %s WHERE booking_id = %s OR phone_number = %s", (check_in, booking_id, phone_number))
        connection.commit()
        cursor.close()
        connection.close()
        return True

def update_user_check_out(check_out, booking_id, phone_number):
        connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
        cursor = connection.cursor()
        cursor.execute("UPDATE booking_details SET check_out = %s WHERE booking_id = %s OR phone_number = %s", (check_out, booking_id, phone_number))
        connection.commit()
        cursor.close()
        connection.close()
        return True

def insert_feedback(overall_experience, ui_feedback, features_feedback, performance, bugs_report, suggestions, customer_service_feedback, additional_comments, room_id):
    connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )

    cursor = connection.cursor()

    insert_query = """
    INSERT INTO feedback (overall_experience, ui_feedback, features_feedback, performance, bugs_report, suggestions, customer_service_feedback, additional_comments, room_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s. %s)
    """

    cursor.execute(insert_query, (overall_experience, ui_feedback, features_feedback, performance, bugs_report, suggestions, customer_service_feedback, additional_comments, room_id))
    connection.commit()
    cursor.close()
    connection.close()
    return True

def get_complete_room_data():
    connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM rooms")
    data = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    cursor.close()
    connection.close()
    return data, column_names

def get_all_from_feedback():
    connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
    cursor = connection.cursor()
    cursor.execute("SELECT room_id, overall_experience, performance, suggestions, additional_comments FROM feedback")
    data = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    cursor.close()
    connection.close()
    return data, column_names

def get_complete_booking_details():
    connection = mysql.connector.connect(
            host = os.getenv("host"),
database = os.getenv("database"),
user = os.getenv("user"),
password = os.getenv("password"),
auth_plugin=os.getenv("auth_plugin")
        )
    cursor = connection.cursor()
    cursor.execute("SELECT room_id, room_type, guests, check_in, check_out, address FROM booking_details")
    data = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    cursor.close()
    connection.close()
    return data, column_names
