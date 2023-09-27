import acquire as a
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_power_distribution(df):
    '''
    function takes in a dataframe of the raw opsd_german_daily data and plots histograms of the distributions of each column
    '''
    
    #visualize our distribution
    for col in df.columns:
        print(col)
        plt.hist(df[col])
        plt.show()
        
def prep_german_power(df):
    '''
    function takes in a dataframe of the raw opsd_german_daily data.
    
    returns df with date column changed to datetime and set to index, cleaned column names, and month and year columns added. backfill used to take care of null values
    '''
    # change column names to lowercase
    df.columns = df.columns.str.lower()

    
    # convert date column to datetime
    df.date = pd.to_datetime(df.date)
    
    # set index to datetimeindex
    df = df.set_index('date').sort_index()
    
    # add month and year column
    df['month'] = df.index.month
    df['year'] = df.index.year
    
    # fill missing values
    # fill make new column with total of wind and solar for missing wind+solar
    df['wind_and_solar'] = df['wind'] + df['solar']
    
    df = df.drop(columns=['wind+solar'])
    
    # fill missing values
    df = df.fillna(0)
    
    return df

def store_data_distribution(df):
    '''
    
    '''
    #visualize our distribution
    plt.hist(df.sale_amount)
    plt.title('Distribution of Sale_Amount')
    plt.show()
    
    #visualize our distribution
    plt.hist(df.item_price)
    plt.title('Distribution of Item_Price')
    plt.show()
    


def prep_store_data(df):
    '''
    
    '''
    # convert sale_date column to datetime
    df.sale_date = pd.to_datetime(df.sale_date)
    
    # set index to datetimeindex
    df = df.set_index('sale_date').sort_index()
    
    # add 'month' and 'day_of_week' columns
    df['month'] = df.index.month
    df['day_of_week'] = df.index.day_of_week
    
    # Add a column to dataframe, sales_total, which is a derived from sale_amount (total items) and item_price
    df['sales_total'] = df.sale_amount * df.item_price
    
    return df