#!/usr/bin/env python
# coding: utf-8

# **We start off by importing the frameworks required for our analysis** 

# In[171]:


import numpy as np 
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')
get_ipython().run_line_magic('matplotlib', 'inline')


# **The dataset below records the confirmed incidences of the COVID19 virus by date and location received from Johns Hopkins University in collaboration with the World Health Organisation**

# In[172]:


df = pd.read_csv('covid19clean.csv',parse_dates=['Date'])


# In[173]:


df.head()


# **It is good practice to check how many null values the dataset has (As this dataset has been cleaned already, it will show zero)**

# In[174]:


df.isnull().sum().sum()


# **It is helpful to seperate this data into values that are more relevant to our analysis of the effect of the COVID19 virus**

# In[175]:


totcases = ['Confirmed', 'Deaths', 'Recovered', 'Still Infected']

df['Still Infected'] = df['Confirmed'] - df['Deaths'] - df['Recovered']

# NA values must be substituted with zeroes as NA values do not help with data analysis
df[['Province/State']] = df[['Province/State']].fillna('NA')
df[totcases] = df[totcases].fillna(0)


# **We use temporary variables so as not to accidentally remove values from the dataset**

# In[176]:


temp = df.groupby('Date')['Confirmed', 'Deaths', 'Recovered', 'Still Infected'].sum().reset_index()
temp = temp[temp['Date']==max(temp['Date'])].reset_index(drop=True)
temp


# **Now we melt the dataframe in order to use Date as the identifier**

# In[177]:


tmp = temp.melt(id_vars="Date", value_vars=['Still Infected', 'Deaths', 'Recovered'])
fig = px.treemap(tmp, path=["variable"], values="value", height=200)
fig.show()


# **A cursory analysis shows that the COVID19 virus does not seem to have a high lethality rate however it can be inferred that transmission rates are high**

# In[178]:


dat = df.groupby(['Province/State','Country/Region'],as_index=False)['Province/State','Country/Region','Confirmed','Recovered','Deaths'].sum()


# **An example of querying one country, the United States**

# In[179]:


dat[dat['Country/Region'] == 'US']


# **A treemap can be used to show the prevalence of the virus around the world.**

# In[180]:


dat["world"] = "world"
fig = px.treemap(dat, path=['world', 'Country/Region'], values='Confirmed',
                  color_continuous_scale='RdBu',
                  color_continuous_midpoint=np.average(dat['Confirmed'], weights=dat['Confirmed']))
fig.update_layout(
    autosize=False,
    width=1000,
    height=1000)

fig.show()


# **China has by far the highest incidence of the virus followed by Italy, Republic of Korea and Iran** 

# **It is helpful to see what provinces in China had mortalities as this enables us to better understand protective measures**

# In[181]:


dat["world"] = "world"
fig = px.treemap(dat, path=['world', 'Country/Region', 'Province/State'], values='Deaths',
                  color_continuous_scale='RdBu',)
fig.update_traces(textposition='top center')
fig.update_layout(
    autosize=False,
    width=1000,
    height=1000)

fig.show()


# **Now we should look at the recovery rates around the world, we do this by finding the percentage of recovery by Country and Region**

# In[182]:


dat['recoverpct'] = dat['Recovered']/dat['Confirmed']
dat["world"] = "world"
fig = px.treemap(dat, path=['world', 'Country/Region'], values='recoverpct',
                  color_continuous_scale='RdBu')

fig.update_traces(textposition='top center')
fig.update_layout(
    autosize=False,
    width=1000,
    height=1000)
fig.show()


# In[183]:


del temp


# **In order to determine the transmission rate of the virus, we need to look at confirmed cases over time**

# In[184]:


temp = df.groupby('Date')['Still Infected', 'Deaths', 'Recovered'].sum().reset_index()
temp = temp.melt(id_vars="Date", value_vars=['Still Infected', 'Deaths', 'Recovered'],
                 var_name='Case', value_name='Count')
temp.head()

fig = px.bar(temp, x="Date", y="Count", color='Case',
             title='Cases over time')

fig.show()


# **Now we look at the deaths per day versus recoveries per day to determine how lethal this virus really is

# In[185]:


temp = df.groupby(['Country/Region', 'Date'])['Confirmed', 'Deaths', 'Recovered'].sum()
temp = temp.reset_index()

fig = px.bar(temp, x="Date", y="Deaths", color='Country/Region', orientation='v', height=600,
             title='Deaths', color_continuous_scale=px.colors.sequential.thermal)
fig.show()

fig = px.bar(temp, x="Date", y="Recovered", color='Country/Region', orientation='v', height=600,
             title='Recovered', color_continuous_scale=px.colors.sequential.thermal)
fig.show()


# ****An animated map known shows the spread of the virus over time (This needs to be run with the buttons below)****

# In[186]:


fig = px.choropleth(dat, 
                    locations="Country/Region", 
                    locationmode = "country names",
                    color="Confirmed", 
                    hover_name="Country/Region", 
                    animation_frame="Confirmed"
                   )

fig.update_layout(
    title_text = 'Spread of Coronavirus over time',
    title_x = 0.5,
    geo=dict(
        showframe = False,
        showcoastlines = False,
    ))
    
fig.show()

