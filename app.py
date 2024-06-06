import streamlit as st 


def main():
    number=st.slider("Pick a number")
    st.text(f'The square number is {number**2}')





if __name__=="__main__":
    main()

