#make sure these libraries are installed before running the program
import yfinance as yf
import pandas as pd
import numpy as np
import pandas_datareader as data
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date
from zipfile import ZipFile
from sklearn import linear_model
import urllib.request
import zipfile
import tkinter as tk
from tkinter import ttk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import Calendar, DateEntry


#functions used to clear current content in order to reuse the program without restarting it. Each possible scenario has been taken into account.


#function to restart because of a date problem
def clear_DateProblem():
    label_DateProblem.destroy()
    ClearErrorButton.pack_forget()

#function to restart because of a data problem (missing, incomplete, etc.)  
def clear_DataProblem():
    label_DataProblem.destroy()
    ClearErrorButton.pack_forget()
    
#function to restart because of a ticker was not found 
def clear_TickerNotFound():
    label_TickerNotFound.destroy()
    label_Exception.destroy()
    ClearErrorButton.pack_forget()

#function to restart after successfully calculating the Beta of a security
def clear_results():
    global CheckTickerButton
    regression_results.destroy()
    start_again.pack_forget()
    stock_chart.get_tk_widget().pack_forget()
    regression_chart.get_tk_widget().pack_forget()
    CheckTickerButton = Button(root, text="Check For Ticker", padx=10, pady=10, command=IsTickerValid)
    CheckTickerButton.pack()

#function to restart because of an error while calculating the beta of the given security
def clear_error():
    global CheckTickerButton
    label_Exception.destroy()
    ClearErrorButton.pack_forget()
    CheckTickerButton = Button(root, text="Check For Ticker", padx=10, pady=10, command=IsTickerValid)
    CheckTickerButton.pack()
    
    
#Check whether the input (ticker) from user can be used on yfinance
def IsTickerValid():
    #global is often used in order to reuse the variables outside this function
    global stock_ticker, stock_data, df, label_TickerFound, label_DateProblem, label_DataProblem, label_TickerNotFound, from_date_input, till_date_input, ClearErrorButton, label_Exception, Calculate_button
    
    try: 
        #using the users input (ticker) yfinance will try to get the company name
        stock_ticker = stock.get()
        company_name = yf.Ticker(stock_ticker).info['longName']
        from_date_input = from_date.get()
        till_date_input = till_date.get()
        
        #to avoid mistakes by users, each scenario regarding the (from - until) date has been implemented
        today = date.today()
        today_formated = today.strftime("%d.%m.%Y")
        
        if from_date_input > till_date_input and from_date_input <= today_formated :
            label_DateProblem = tk.Label(root, text=f"Start date {from_date_input} cannot be after end date {till_date_input}. Press 'Clear' to try again.", bg = "white", font= "Helvetica 12 bold")
            label_DateProblem.pack(pady = 30)
            ClearErrorButton = Button(root, text="Clear", padx=10, pady=10, command=clear_DateProblem)
            ClearErrorButton.pack(pady=10)
            
        if from_date_input == till_date_input and from_date_input <= today_formated:
            label_DateProblem = tk.Label(root, text=f"Start date {from_date_input} cannot be the same as the end date {till_date_input}. Press 'Clear' to try again.", bg = "white", font= "Helvetica 12 bold")
            label_DateProblem.pack(pady = 30)
            ClearErrorButton = Button(root, text="Clear", padx=10, pady=10, command=clear_DateProblem)
            ClearErrorButton.pack(pady=10)         
        
        if from_date_input >= today_formated or till_date_input > today_formated:
            label_DateProblem = tk.Label(root, text=f"Date cannot be in the future. Press 'Clear' to try again.", bg = "white", font= "Helvetica 12 bold")
            label_DateProblem.pack(pady = 30)
            ClearErrorButton = Button(root, text="Clear", padx=10, pady=10, command=clear_DateProblem)
            ClearErrorButton.pack(pady=10)    
                
        if from_date_input < today_formated and till_date_input <= today_formated and from_date_input < till_date_input:
            #adjusting the date due to specifics of yfinance api
            from_date_adjusted = (datetime.strptime(from_date_input, "%d.%m.%Y") + timedelta(days = 1)).strftime("%Y-%m-%d")
            till_date_adjusted = (datetime.strptime(till_date_input, "%d.%m.%Y") + timedelta(days = 1)).strftime("%Y-%m-%d")

            #download the required data into a dataframe
            stock_data = yf.download(stock_ticker, start = from_date_adjusted, end = till_date_adjusted)["Adj Close"]
            df = pd.DataFrame(stock_data)
            
            #another error warning in case the data is unavailable despite having that ticker on yfinance
            if df.empty == True:
                label_DataProblem = tk.Label(root, text=f"Cannot find data for {stock_ticker}. Press 'Clear' to try again with a different Ticker.", bg = "white", font= "Helvetica 12 bold")
                label_DataProblem.pack(pady = 30)
                ClearErrorButton = Button(root, text="Clear", padx=10, pady=10, command=clear_DataProblem)
                ClearErrorButton.pack(pady=10)
                
            #if the ticker was found, dates are good, and the data is downloaded we can proceed with the calculation of the beta
            else:
                CheckTickerButton.pack_forget()
                Calculate_button = Button(root, text="Calculate", padx=10, pady=10, command=StockFetching)
                Calculate_button.pack(pady=10)
                label_TickerFound = tk.Label(root, text=f"{stock_ticker}, was found. Press 'Calculate' to calculate the Beta of {company_name} between {from_date_input} and {till_date_input}.", bg = "white", font= "Helvetica 12 bold")
                label_TickerFound.pack(pady = 30)
                
    #An error warning in case ticker was not found on yfinance
    except Exception as e:
        label_TickerNotFound = tk.Label(root, text=f"Cannot find {stock_ticker} data, check your spelling. Otherwise it probably does not exist on yfinance or the given dates are not available. Press 'Clear' to try again.", bg = "white", font= "Helvetica 12 bold")
        label_TickerNotFound.pack(pady = 30)
        label_Exception = tk.Label(root, text=f"Error 101: {e}", bg = "white", font= "Helvetica 12 bold")
        label_Exception.pack(pady = 30)
        ClearErrorButton = Button(root, text="Clear", padx=10, pady=10, command=clear_TickerNotFound)
        ClearErrorButton.pack(pady=10)
        
    
#after we made sure that the data exists we can start by calculating its beta with the following function
def StockFetching():
    global regression_results, start_again, ClearErrorButton, label_Exception, stock_chart, regression_chart
    
    label_TickerFound.destroy()
    
    try:
        #Calculate the percentage change of each day and add a new column to the dataframe with the results
        df["Return"]=(df["Adj Close"]).pct_change()
        
        #To calculate the beta we will use the Fama and French research data acting as the market to which the asset will be compared to. In order to have the latest version with the latest data it will be downloaded when using this program
        ff_url = "http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_daily_CSV.zip"
        #Download the file and save it
        #We will name it fama_french.zip file
        urllib.request.urlretrieve(ff_url,"fama_french.zip")
        zip_file = zipfile.ZipFile("fama_french.zip", "r")
        #Next we extract the file data
        #We will call it ff_factors.csv
        zip_file.extractall()
        #Make sure you close the file after extraction
        zip_file.close()
        
        #skipping the first 3 rows cz they contain unecessary data
        ff_factors = pd.read_csv("F-F_Research_Data_Factors_daily.csv", skiprows = 3)
        #droping the last row cz it contains unecessary data
        ff_factors.drop(index = ff_factors.index[-1], axis = 0, inplace = True)
        #Change name
        ff_factors.rename(columns={"Unnamed: 0":"Date"}, inplace = True)
        #Change date format to merge cells
        ff_factors["Date"] = pd.to_datetime(ff_factors["Date"], format='%Y%m%d')
        #Fama French numbers are in % which is why we divide them by 100 to work with the same unit
        ff_factors[["Mkt-RF", "SMB", "HML", "RF"]]= ff_factors[["Mkt-RF", "SMB", "HML", "RF"]]/100

        #Merge the 2 DFs together
        merged_df = pd.merge(df,ff_factors,on = "Date")
        #Create a new column and calculate the excess return
        merged_df["Excess Return"]=((merged_df["Return"])-merged_df["RF"])
        #Drop the first row because the return is NaN
        merged_df.drop(index = merged_df.index[0], axis = 0, inplace = True)

        #defining variables for the regression
        X = merged_df[["Mkt-RF"]].values
        y = merged_df["Excess Return"].values

        #create and fit the regression model
        lm = linear_model.LinearRegression()
        model = lm.fit(X,y)
        predictions = lm.predict(X)

        #This is the R² score of our model
        r_2 = lm.score(X,y)

        #beta -> asset compared to the market
        beta_factor_array = lm.coef_
        beta_factor = np.ndarray.__float__(beta_factor_array)

        #alfa -> abnormal rate of return (excess return regardless of market)
        alfa_factor = lm.intercept_ * 100

        Calculate_button.pack_forget()
        
        #If user wants to calculate the beta of another asset, this button will delete everything and the user can start again
        start_again = Button(root, text="Clear the window and start again", padx=10, pady=10, command=clear_results)
        start_again.pack(pady=10)
        
        #The results (Beta, Alfa and R² score) are displayed
        regression_results = tk.Label(root, text=f"{stock_ticker} has a Beta-factor of {beta_factor:.4f} and an Alfa-factor of {alfa_factor:.4f} for the period between {from_date_input} and {till_date_input}. The R² score is {r_2:.4f}.", pady = 10, bg = "white", font = "Helvetica 14 bold")
        regression_results.pack(fill="x", pady=10)
        
        #show stock data (adjusted closing price on our window)
        stock_graph = plt.Figure(figsize=(6,5), dpi=100)
        ax1 = stock_graph.add_subplot(111)
        stock_chart = FigureCanvasTkAgg(stock_graph, root)
        stock_chart.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        stock_data.plot(legend=True, ax=ax1)
        ax1.set_title(f"{stock_ticker} Adj Closing Price")
        
        #show regression model (y = excess return (compared to Market return), X = Market return)
        regression_graph = plt.Figure(figsize=(6,3), dpi=100)
        ax2 = regression_graph.add_subplot(111)
        regression_chart = FigureCanvasTkAgg(regression_graph, root)
        regression_chart.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH)
        ax2.scatter(X, y,color = "steelblue")
        ax2.plot(X, model.predict(X), color = "k")
        ax2.set_title(f"{stock_ticker}'s linear Regression")
    
    #if any error happens along the calculation this error message will be displayed
    except Exception as p:
        label_Exception = tk.Label(root, text=f"Error 102: {p}. Press 'Clear' to try again.", bg = "white", font= "Helvetica 12 bold")
        label_Exception.pack(pady = 30)
        ClearErrorButton = Button(root, text="Clear", padx=10, pady=10, command=clear_error)
        ClearErrorButton.pack(pady=10)
    


#parameters for Tkinter window
root = Tk()
root.geometry("1450x750")
root.configure(background="white")
icon_photo = PhotoImage(file = "Finance_Bro_3000-main/Finance_Bro_Icon.png") #from https://www.etsy.com/ch/listing/1072807330/geldbecher-lustig-parodie-geschenk-gag
root.iconphoto(False, icon_photo)
root.title("Your Everyday Finance Bro")

#start widgets inside the window
welcome_label = tk.Label(root, text="Welcome to Finance Bro 3000. To calculate the Beta of a stock enter a valid ticker:", bg = "white", font= "Helvetica 18 bold")
welcome_label.pack(pady = 20)

#asset entry by user
stock = Entry(root)
stock.pack(pady=10)

#date "from" entry by user
from_label = tk.Label(root, text="From:", bg = "white", font= "Helvetica 14 bold")
from_label.pack( padx=5, pady=5)

from_date = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd.mm.y')
from_date.pack( padx=5, pady=5)

#date "until" entry by user
until_label = tk.Label(root, text="Until:", bg = "white", font= "Helvetica 14 bold")
until_label.pack( padx=5, pady=5)

till_date = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd.mm.y')
till_date.pack( padx=5, pady=10)

#first step in determining wether the ticker is available and checks the entered dates
CheckTickerButton = Button(root, text="Check For Ticker", padx=10, pady=10, command=IsTickerValid)
CheckTickerButton.pack()

#loop for Tkinter
root.mainloop()
