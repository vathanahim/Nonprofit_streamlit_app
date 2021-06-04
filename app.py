
import streamlit as st
import pandas as pd
import requests
import json
import xmltodict
import plotly.express as px

host = "https://api.globalgiving.org"
operation = "/api/public/projectservice/featured/projects"
api_key = '51711d58-2372-4362-8126-22bf5847b9e8'

#get data from api
def get_data(host, operation, api_key):
    url = host + operation + "?"+"api_key=" + api_key
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

def main():
        
    st.text("Generate NonProfit")
    generate = st.button(label="Generate NonProfit")
            
    types = ["Data", "Bar Graph", "Map"]

    if generate:  
        nav1, nav2 = st.beta_columns([3,2])
        st.success("Generating Random 10 Non-Profits")
        result = get_data(host, operation, api_key)
        result = con_to_data_frame(con_to_list_env(result))
        st.table(result.head(5))
        fig = px.bar(result, x='title', y='Additional Fund Needed')
        st.plotly_chart(fig) 



if __name__ == "__main__":
    main()