
import streamlit as st
from apps import randomize, countries
from multiapp import MultiApp

app = MultiApp()

#add app
app.add_app("Randomize", randomize.app)
app.add_app("Country Search", countries.app)

# Run the app
app.run()
