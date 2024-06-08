# import streamlit as st 
# import json
# import time 

# def create_user(username, password,placeholder):
#     with open('db.json', 'r') as f:
#             data = json.load(f)

#     if username in data:
#         placeholder.error("Username already exists")

#         return
#     data[username] = password
#     with open('db.json', "w") as f:
#         json.dump(data,f)

#         placeholder.success("Account created")

# def create_account():
#     username=st.text_input("Username")
#     password=st.text_input("Password", type="password")
#     time.sleep(3)
#     placeholder=st.empty()
#     st.button("Submit",on_click=create_user, args=(username, password,placeholder))
        
# def check_user(username, password,placeholder):
#     with open('db.json') as f:
#         data = json.load(f)  

#     if username not in data:
#         placeholder.error("Incorrect username provided")

#         return
    
#     correctpass = data[username]
        
#     if correctpass == password:
#         placeholder.success("Logged in")
#         st.session_state.is_loggedin=True
#     else:
#         placeholder.error("Incorrect password provided")


# def login():
#     username=st.text_input("Username")
#     password=st.text_input("Password", type="password")
#     placeholder=st.empty()
#     st.button("Login",on_click=check_user, args=(username, password,placeholder)) 
        


# def view_users():
#     with open('db.json') as f:
#         data = json.load(f)  
#     st.write(data)

# def main():
#     number=st.slider("Pick a number")
#     st.text(f'The square number is {number**2}')


# def logout():
#     st.session_state.is_loggedin=False



# if __name__=="__main__":
    
#     if 'is_loggedin' not in st.session_state:
#         st.session_state.is_loggedin=False

    
    
#     if st.session_state.is_loggedin==False:
#         with st.sidebar:
#             selected=st.selectbox("Select an option", ["Create Account", "Login"])
#         if selected=="Create Account":
#             st.title("Create Account")
#             st.divider()
#             create_account()
#         elif selected=="Login":
#             st.title("Login Account")
#             st.divider()
#             login()
#     if st.session_state.is_loggedin==True: 
#         with st.sidebar:
#             selected=st.selectbox("Select an option", ["Home", "View Users"])
#             st.button('Log Out',on_click=logout)
#         if selected=="View Users":
#                 st.title("View Accounts")
#                 st.divider()
#                 view_users()
#         elif selected=="Home":
#             st.title("Home Page")
#             st.divider()
#             main() 



import streamlit as st
import json
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def get_token():
    with open('secrets.json', 'r') as f:
        data = json.load(f)
    return data['token']

def send_email(username, email, pin):
    token = get_token()
    from_email = "signupconfirmation83@gmail.com"
    to_email = email
    subject = "Signup Confirmation"
    message = f"Hello, {username}\n\nYour Sign Up confirmation pin is: {pin}\n\nThank you for using Saral's App\n\nYou can ignore this mail if you have not signup"
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email,token )
        server.sendmail(from_email, to_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email:", e)
    finally:
        server.quit()


def load_users():
    with open('db.json') as f:
        data = json.load(f)  
    return data

def save_users(data):
    with open('db.json', "w") as f:
        json.dump(data,f)

def check_PIN(username, password, email, pin_input, data, pin):
    if pin_input == str(pin):
        data[username] = {'Password': password, 'Email': email}
        save_users(data)
        st.success("Successfully Created Account")
        st.session_state.signup_confirmation = False
    else:
        st.error("Incorrect Pin, Correct pin was: " + str(pin) + "You entered: " + pin_input, icon="🚨", )
        st.session_state.signup_confirmation = False
    


def signup_confirmation(username, password, email, pin, data):
    st.title("Sign Up Confirmation")
    st.divider()

    st.success("A pin has been sent to your mail, Please Verify it and create your account")

    pin_input = st.text_input("Enter Pin")
    

    st.button("Submit", on_click= lambda: check_PIN(username, password, email, pin_input, data, pin))


def create_user(username, password, email):
    st.session_state.signup_confirmation = True
    data = load_users()
    if username in data:
        st.error("Username already exists")
        return
    
    pin = random.randint(1000, 9999) 
    print(f'Pin Sent = {pin}')
    signup_confirmation(username, password, email, pin, data)
    send_email(username, email, pin)


def signup_page():
    if not st.session_state.signup_confirmation:
        st.title("Create Account")
        st.divider()
        username=st.text_input("Username", )
        password=st.text_input("Password", type="password", )
        email = st.text_input("Email", type="default")
        st.button("Submit",on_click=create_user, args=(username, password,email))


def login_user(username, password):
    data = load_users()
    if username not in data:
        st.error("Incorrect username provided")
        return
    correctpass = data[username]['Password']
    if correctpass == password:
        st.success("Logged in")
    else:
        st.error("Incorrect password provided")

def login_page():
    st.title("Login Account")
    st.divider()
    username=st.text_input("Username")
    password=st.text_input("Password", type="password")
    st.button("Login",on_click=login_user, args=(username, password))


def view_users():
    data = load_users()
    st.write(data)

def view_page():
    st.title("View Accounts")
    st.divider()
    view_users()

def logout():
    st.session_state.is_loggedin=False

def home_page(): 
    st.title("Welcome to the Saral's App")
    st.divider()

    
    

def main():
    if st.session_state.is_loggedin==False:
        with st.sidebar:
            selected=st.selectbox("Select an option", ["Create Account", "Login"])

        if selected=="Create Account":
            signup_page()

        elif selected=="Login":
            login_page()

    if st.session_state.is_loggedin==True:
        with st.sidebar:
            selected=st.selectbox("Select an option", ["Home", "View Users"])
            if selected == "Home":
                home_page()

            elif selected == "View Users":
                view_page()
            st.button('Log Out',on_click=logout)

if __name__ == "__main__":
    if 'is_loggedin' not in st.session_state:

        st.session_state.is_loggedin = False

    if 'signup_confirmation' not in st.session_state:
        st.session_state.signup_confirmation = False
    main() 
    # st.button('Continue',on_click=main) 
