import streamlit as st
import numpy as np
import pandas as pd
import time
import requests
# import simplejson as json
# import matplotlib.pyplot as plt
# from bokeh.plotting import figure, show
from math import pi
# from bokeh.io import output_notebook
# import plotly.figure_factory as ff
import plotly.graph_objects as go



def to_df(data):
    # Convert into DataFrame; Transpose; Rename columns; Index to datetime

    df = pd.DataFrame(data['Time Series (Daily)']).T.astype(float)
    df.columns = [x.split('. ')[-1] for x in df.columns]
    df = df.rename(columns={'dividend amount':'dividend', 'split coefficient':'split'})
    df.index = pd.to_datetime(df.index)
    return df


# Plot with Bokeh -- this doesn't work with streamlit currently
# output_notebook()

# Move widgets to sidebar
# period = st.sidebar.selectbox(
#     'Select period: ',
#     ['Last 100 trading days', 'All'])
# 'Period: ', period

ticker = st.sidebar.text_input('Enter Ticker: ', 'AAPL')

st.title(f'Ticker: {ticker.upper()}')

# Well, plotly works!
apikey = 'TAQKWLNW3GEANUR9'

url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker.upper()}&outputsize=compact&apikey={apikey}'
r = requests.get(url)
data = r.json()

df = to_df(data)

fig = go.Figure(data = [go.Candlestick(x = df.index,
                                    open = df['open'],
                                    high = df['high'],
                                    low  = df['low'],
                                    close= df['adjusted close']
                                    )
                        ]
                )

fig.update_layout(width = 900,
                  margin=dict(l=0, r=50, b=100, t=10, pad=4)
                 )


st.plotly_chart(fig, use_container_width=True)


# Overview
url_overview = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={apikey}'
r_overview = requests.get(url_overview).json()

expander = st.sidebar.expander('Company Overview')
desc = r_overview['Description']
expander.write(desc)

# Checkbox
# st.write('Checkbox:')

# if st.checkbox('Company Overview'):

# Selectbox
# st.write('Selectbox:')

# option = st.selectbox(
#     'Which number do you like best?',
#     df['first column'])

# 'You selected: ', option























