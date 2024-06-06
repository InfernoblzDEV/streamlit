import streamlit as st 


def main():
    number=st.slider("Pick a number")
    st.text('The square number is {number**2}'.format(number))





if __name__=="__main__":
    main()

