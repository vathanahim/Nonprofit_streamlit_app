
import streamlit as st
import pandas as pd
import requests
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
@st.cache
def con_to_data_frame(data_input):
    df = pd.DataFrame(data_input, columns=target_var)
    df[['funding', 'goal']] = df[['funding', 'goal']].apply(pd.to_numeric)
    df['Additional Fund Needed'] = df.apply(lambda x: x['goal'] - x['funding'], axis=1)
    df['Additional Fund Needed'] = df['Additional Fund Needed'].astype(float)
    pd.set_option("display.max_columns", 100)
    return df

data_disp = {}

def app():
        
    choice = st.sidebar.selectbox("option", ("Data", "Analytics"))


    st.text("Generate NonProfit")
    generate = st.button(label="Press")

    global data_disp

    if generate:
        result = get_data(host, operation, api_key)
        result = con_to_data_frame(con_to_list_env(result))
        data_disp = result.append(data_disp, ignore_index=True) 

    if choice == "Data":
        st.success("Generate Data For Random 10 Non-Profits")
        result = pd.DataFrame.from_dict(data_disp)
        st.table(result.head(10))
        

    if choice == "Analytics":
        st.success("Generate Analytics For Random 10 Non-Profits")
        if  len(data_disp) != 1:
            result = pd.DataFrame.from_dict(data_disp)
            fig = px.bar(result, x='title', y='Additional Fund Needed')
            fig.update_layout(width=900,height=600)
            st.plotly_chart(fig)
            

# import streamlit as st
# import numpy as np
# import pandas as pd

# def create_table(n=7):
#     df = pd.DataFrame({"x": range(1, 11), "y": n})
#     df['x*y'] = df.x * df.y
#     return df


# def app():
#     st.title('Data Stats')

#     st.write("This is a sample data stats in the mutliapp.")
#     st.write("See `apps/data_stats.py` to know how to use it.")

#     st.markdown("### Plot Data")
#     df = create_table()

#     st.line_chart(df)


