
# coding: utf-8

# In[ ]:


import tkinter
import tkinter.messagebox
from tkinter import *
import webbrowser
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import quandl
import datetime
import matplotlib.dates as mdates
import statsmodels.api as sm
import statsmodels.tsa.stattools as ts
import statsmodels.formula.api as sm
from pandas import Series
from statsmodels.tsa.stattools import adfuller
from pandas import DataFrame
from sklearn.linear_model import LinearRegression
from upstox_api.api import *

s = Session ('7yQdosvDbb9CiQitGlnOX6jGM5CnRL816vxJdo7a')
s.set_redirect_uri ('https://upstox.com')
s.set_api_secret ('zrmhi4q3p4')
link = s.get_login_url()
webbrowser.open_new_tab(link)
def proces():
    code = Entry.get(E1)
    startdate_day = Entry.get(E2)
    enddate_day = Entry.get(E3)
    startdate_intra = Entry.get(E4)
    enddate_intra = Entry.get(E5)
    s.set_code (code)
    access_token = s.retrieve_access_token()
    u = Upstox ('7yQdosvDbb9CiQitGlnOX6jGM5CnRL816vxJdo7a', access_token)
    u.get_master_contract('NSE_EQ')
    u.get_master_contract('NSE_FO')
    u.get_master_contract('NSE_INDEX')
    A=1+1
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    df3 = pd.DataFrame()
    df4 = pd.DataFrame()
    ##### Daily data
    with open(r'C:\Users\Anil Jain\Desktop\fnoStocks.txt') as fp:
        lines = fp.readlines()
        for line in lines:
            stock = line.rstrip()
            try:
                df1[stock] = pd.DataFrame.from_dict(u.get_ohlc(u.get_instrument_by_symbol('NSE_EQ',stock), OHLCInterval.Day_1,datetime.strptime(startdate_day, '%d/%m/%Y').date(),datetime.strptime(enddate_day, '%d/%m/%Y').date()))['close']
                df1.dropna(inplace=True)
            except:
                pass
    # #####nifty data
    with open(r'C:\Users\Anil Jain\Desktop\fnifty.txt') as fp1:
        lines1 = fp1.readlines()
        for line in lines1:
            nifty = line.rstrip()
            try:
                df2[nifty] = pd.DataFrame.from_dict(u.get_ohlc(u.get_instrument_by_symbol('NSE_INDEX',nifty), OHLCInterval.Day_1,datetime.strptime(startdate_day, '%d/%m/%Y').date(),datetime.strptime(enddate_day, '%d/%m/%Y').date()))['close']
                df2.dropna(inplace=True)
            except:
                pass 
    ###### minutes timeframe
    with open(r'C:\Users\Anil Jain\Desktop\fnoStocks.txt') as fp2:
        lines2 = fp2.readlines()
        for line in lines2:
            stock = line.rstrip()
            try:
                df3[stock] = pd.DataFrame.from_dict(u.get_ohlc(u.get_instrument_by_symbol('NSE_EQ',stock), OHLCInterval.Minute_30,datetime.strptime(startdate_intra, '%d/%m/%Y').date(),datetime.strptime(enddate_intra, '%d/%m/%Y').date()))['close']
                df3.dropna(inplace=True)
            except:
                pass
    # #####nifty data
    with open(r'C:\Users\Anil Jain\Desktop\fnifty.txt') as fp3:
        lines3 = fp3.readlines()
        for line in lines3:
            nifty = line.rstrip()
            try:
                df4[nifty] = pd.DataFrame.from_dict(u.get_ohlc(u.get_instrument_by_symbol('NSE_INDEX',nifty), OHLCInterval.Minute_30,datetime.strptime(startdate_intra, '%d/%m/%Y').date(),datetime.strptime(enddate_intra, '%d/%m/%Y').date()))['close']
                df4.dropna(inplace=True)
            except:
                pass 
    frames2 = [df3,df4]
    df_intra = pd.concat(frames2,axis = 1)
    frames1 = [df1,df2]
    df_day = pd.concat(frames1,axis = 1)

    df_day.fillna(df_day.mean(),inplace = True)
    df_intra.fillna(df_intra.mean(),inplace = True)

    def find_cointegrated_pairs(dataframe):
        n = dataframe.shape[1] # the length of dateframe
        keys = dataframe.columns # get the column names
        pairs = []
        for i in range(n):
            for j in range(i+1,n): # for j bigger than i
                ### MAIN LOGIC WAS DELETED # record the contract with that p-value
        return pairs
    ######reversed
    def find_cointegrated_pairs2(dataframe):
        n = dataframe.shape[1] # the length of dateframe
        keys = dataframe.columns # get the column names
        pairs2 = []
        for i in reversed(range(n)):
            for j in range(i+1,n): # for j bigger than i
                #### MAIN LOGIC WAS DELETED
        return pairs2

    split_day = int(len(df_day) * 1)
    split_intra = int(len(df_intra) * 1)
    #run our dataframe (up to the split point) of ticker price data through our co-integration function and store results
    pairs1 = find_cointegrated_pairs(df_day[:split_day])
    pairs2 = find_cointegrated_pairs2(df_day[:split_day])
    pairs3 = find_cointegrated_pairs(df_intra[:split_intra])
    pairs4 = find_cointegrated_pairs2(df_intra[:split_intra])
    pstart1 = pd.DataFrame(pairs1)
    pend2 = pd.DataFrame(pairs2)
    pstart3 = pd.DataFrame(pairs3)
    pend4 = pd.DataFrame(pairs4)
    frames1 = [pstart1, pend2]
    frames2 = [pstart3,pend4]
    result1 = pd.DataFrame(pd.concat(frames1))
    result2 = pd.DataFrame(pd.concat(frames2))

    export_excel = result1.to_excel (r'C:\Users\Anil Jain\Desktop\daily files\nifty\pair_daily_data.xlsx',index = None, header=True)
    export_excel = result2.to_excel (r'C:\Users\Anil Jain\Desktop\daily files\nifty\pair_intra_data.xlsx',index = None, header=True)

top = tkinter.Tk()
L1 = Label(top, text="Code",).grid(row=1,column=0)
L2 = Label(top, text="Start_date_day",).grid(row=2,column=0)
L3 = Label(top, text="end_date_day",).grid(row=3,column=0)
L4 = Label(top, text="Start_date_intra",).grid(row=4,column=0)
L5 = Label(top, text="End_date_intra",).grid(row=5,column=0)
E1 = Entry(top, bd =5)
E1.grid(row=1,column=1)
E2 = Entry(top, bd =5)
E2.grid(row=2,column=1)
E3 = Entry(top, bd =5)
E3.grid(row=3,column=1)
E4 = Entry(top, bd =5)
E4.grid(row=4,column=1)
E5 = Entry(top, bd =5)
E5.grid(row=5,column=1)
B=Button(top, text ="Generate_Excel",command = proces).grid(row=6,column=1,)

top.mainloop()

