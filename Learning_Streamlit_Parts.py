import streamlit as st
from time import sleep
import numpy.random as random_array

st.header("Miscellaneous Stuff")

st.info("Learning how everything in this works")

st.balloons()

st.error("Something Failed... JK")

st.dataframe(random_array.rand(3,2))

st.text_input("Text Input")

st.button("BUTTON")

st.code("Code")

st.checkbox("Checkbox")

#st.download_button("Download",random_array.rand(3,2),"Download_Data.csv",mime='text/csv')

uploaded_file = st.file_uploader("Choose a file",accept_multiple_files=True)

st.html("<h1>Cheers HTML</h1>")

progress_text:str = "Operation in progress. Please wait."
my_bar = st.progress(0, text=progress_text)
for percent_complete in range(100):
    sleep(0.01)
    my_bar.progress(percent_complete + 1, text=progress_text)
sleep(1)
my_bar.empty()