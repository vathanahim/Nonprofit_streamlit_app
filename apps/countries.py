
from numpy import empty
from requests.api import get
import streamlit as st
import pandas as pd
import requests
import xmltodict
import plotly.express as px
import pycountry

mapping = {country.name: country.alpha_2 for country in pycountry.countries}

def get_data(country):
    country = country
    host = "https://api.globalgiving.org"
    operation = "/api/public/projectservice/countries/"
    api_key = '51711d58-2372-4362-8126-22bf5847b9e8'
    url = host + operation + country +'/projects'+"?"+"api_key=" + api_key
    response = requests.get(url, verify=False)
    data_dict = xmltodict.parse(response.text)
    return data_dict

#env has one contactaddress edu has two
target_var = ['title','activities','contactAddress', 'contactCity','contactState' ,'contactCountry', 'contactPostal',
              'funding','goal','themeName']

#converting orderdict to list of list for each organization
def con_to_list_env(data_dict):
    data = []
    for i in range(len(data_dict['projects']['project'])):
        temp_list = []
        for j in target_var:
            temp = data_dict['projects']['project'][i][j]
            temp_list.append(temp)
        data.append(temp_list)
            
    return data

#convert list of list to dataframe            
def con_to_data_frame(data_input):
    df = pd.DataFrame(data_input, columns=target_var)
    df[['funding', 'goal']] = df[['funding', 'goal']].apply(pd.to_numeric)
    df['Additional Fund Needed'] = df.apply(lambda x: x['goal'] - x['funding'], axis=1)
    df['Additional Fund Needed'] = df['Additional Fund Needed'].astype(float)
    return df

data_disp = {}
i = 0

def app():

    choice = st.sidebar.selectbox("option", ("Data", "Analytics"))
   

    with st.form(key = "Search Country"):
        nav1, btn = st.beta_columns([3,1])
        with nav1:
            country_term = st.text_input("Insert Country Name")
        with btn:
            st.text('Search')
            search = st.form_submit_button(label='Search')

    st.success("Searching for Nonprofits in {}".format(country_term))

    global data_disp
    global i

    if search and country_term != empty:
        i = i+1
        if (i < 2):
            country_term = mapping[country_term]
            result = get_data(str(country_term))
            result = con_to_data_frame(con_to_list_env(result))
            data_disp = result.append(data_disp, ignore_index=True) 
        else:
            data_disp = {}
            country_term = mapping[country_term]
            result = get_data(str(country_term))
            result = con_to_data_frame(con_to_list_env(result))
            data_disp = result.append(data_disp, ignore_index=True) 

    if choice == "Data":
        result = pd.DataFrame.from_dict(data_disp)
        st.table(result)
    elif choice == 'Analytics':
        result = pd.DataFrame.from_dict(data_disp)
        fig = px.bar(result, x='title', y='Additional Fund Needed')
        fig.update_layout(width=900,height=600)
        st.plotly_chart(fig)

   


