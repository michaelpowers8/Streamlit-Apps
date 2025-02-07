import streamlit as st
from pandas import DataFrame
import numpy.random as random_array

st.header("Miscellaneous Stuff")

st.info("Learning how everything in this works")

st.balloons()

st.error("Something Failed... JK")

st.dataframe(random_array.rand(3,2))

st.text_input("Text Input")