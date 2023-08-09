import streamlit as st
import hashlib
import sqlite3
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time

# Security
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

# DB Management
conn = sqlite3.connect('data.db')
c = conn.cursor()

def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)', (username, password))
    conn.commit()

def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    return data

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data

def main():
    st.title("Assignment Reminder App")
    
    create_usertable()  # Create user table if it doesn't exist
    
    menu = ["Home", "Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Home":
        st.subheader("Home")
    
    elif choice == "Login":
        st.subheader("Login Section")
    
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox("Login"):
            hashed_pswd = make_hashes(password)
    
            result = login_user(username, check_hashes(password, hashed_pswd))
            if result:
                st.success("Logged In as {}".format(username))
                st.subheader("Assignment Reminder App")
                
                years = st.number_input("Years", value=0)
                months = st.number_input("Months", value=0)
                weeks = st.number_input("Weeks", value=0)
                days = st.number_input("Days", value=0)
                hours = st.number_input("Hours", value=0)
                minutes = st.number_input("Minutes", value=0)
                seconds = st.number_input("Seconds", value=0)
                
                remind = st.text_input("What is the Assignment?")
                description = st.text_area("Assignment Description", "")
                
                target_time = datetime.now() + relativedelta(
                    years=years,
                    months=months,
                    days=days,
                    hours=hours,
                    minutes=minutes,
                    seconds=seconds,
                    weeks=weeks
                )
                
                countdown_time = target_time.strftime("%Y-%m-%d %H:%M:%S")
                
                start_button = st.button("Start Countdown")
                restart_button = st.button("Restart Countdown")
                
                timer_text = st.empty()
                is_counting = False
                
                while True:
                    if start_button and not is_counting:
                        is_counting = True
                        start_button = False
                    elif restart_button:
                        is_counting = False
                        start_button = True
                        restart_button = False
                    
                    if is_counting:
                        remaining_time = relativedelta(target_time, datetime.now())
                        timeformat = '{years}y {months}mo {weeks}w {days}d {hours}h {minutes}m {seconds}s'.format(
                            years=remaining_time.years,
                            months=remaining_time.months,
                            weeks=remaining_time.weeks,
                            days=remaining_time.days,
                            hours=remaining_time.hours,
                            minutes=remaining_time.minutes,
                            seconds=remaining_time.seconds
                        )
                        countdown_text = f"{countdown_time}: {timeformat}"
                        timer_text.markdown(countdown_text)
                        
                        if datetime.now() >= target_time:
                            is_counting = False
                            st.balloons()
                            st.write(f"Reminder: {remind}")
                            st.write(f"Description: {description}")
                    
                    time.sleep(1)
    
    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
    
        if st.button("Signup"):
            add_userdata(new_user, make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")
    
if __name__ == "__main__":
    main()
