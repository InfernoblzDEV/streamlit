import streamlit as st 
import json

def create_account():
    username=st.text_input("Username")
    password=st.text_input("Password", type="password")
    if st.button("Submit"):
        with open('db.json', 'r') as f:
            data = json.load(f)

        data[username] = password
        with open('db.json', "w") as f:
            json.dump(data,f)

        st.success("Account created")

def login():
    username=st.text_input("Username")
    password=st.text_input("Password", type="password")
    if st.button("Login"):    
        with open('db.json') as f:
            data = json.load(f)  

        if username not in data:
            st.error("Incorrect username provided")
            return
        correctpass = data[username]
            
        if correctpass == password:
            st.success("Logged in")
            st.session_state.is_loggedin=True
        else:
            st.error("Incorrect password provided")

def view_users():
    with open('db.json') as f:
        data = json.load(f)  
    st.write(data)

def main():
    number=st.slider("Pick a number")
    st.text(f'The square number is {number**2}')


def logout():
    st.session_state.is_loggedin=False



if __name__=="__main__":
    
    if 'is_loggedin' not in st.session_state:
        st.session_state.is_loggedin=False

    
    
    if st.session_state.is_loggedin==False:
        with st.sidebar:
            selected=st.selectbox("Select an option", ["Create Account", "Login"])
        if selected=="Create Account":
            st.title("Create Account")
            st.divider()
            create_account()
        elif selected=="Login":
            st.title("Login Account")
            st.divider()
            login()
    if st.session_state.is_loggedin==True: 
        with st.sidebar:
            selected=st.selectbox("Select an option", ["Home", "View Users"])
            st.button('Log Out',on_click=logout)
        if selected=="View Users":
                st.title("View Accounts")
                st.divider()
                view_users()
        elif selected=="Home":
            st.title("Home Page")
            st.divider()
            main() 

