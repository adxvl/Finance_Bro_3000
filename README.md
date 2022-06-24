**General Description**

![alt text](https://github.com/adxvl/Finance_Bro_3000/blob/ed804cf65452ecb7f4aaf11c6e617657c194cd41/Finance_Bro_Icon.png) [^1]

<p align="center">
  <img width="460" height="300" src="[http://www.fillmurray.com/460/300](https://github.com/adxvl/Finance_Bro_3000/blob/ed804cf65452ecb7f4aaf11c6e617657c194cd41/Finance_Bro_Icon.png)">
</p>

This is the project of Adel El Mais for the course Programming - Introduction level at the University of St. Gallen supervised by Dr. Mario Silic.

The aim of the project was to create a program to calculate the Beta of any financial security for any given time period. This method for calculating the beta was inspired by the following Excel tutorial https://www.youtube.com/watch?v=ucKK528ApCw

-----

**How does the code work?**

When the code is executed, a window opens. The user is welcomed and asked to enter a ticker (e.g. AAPL) and a time period for which the user wants to calculate the beta. In the background, the program checks whether the user input is valid (e.g. ticker is valid, time period is not in the future, data availability, etc.). If this is not the case, an error message pops up and the user is prompted to try again by correcting the input. Once the validity of the data is confirmed, the program performs the calculation based on the Youtube tutorial included in the general description. The ticker is compared with the "CRSP U.S. Total Market Index", which serves as the market return. This data was taken from the Fama/French database, which is downloaded when the code is run (to get the latest data). The result - a graph of the price development of the financial asset visualised with the regression. Beta, Alfa and R² are also displayed in text form. For better understanding of the code check the comments in the ```Run_me.py``` file.

-----

**Example**

![alt text](https://github.com/adxvl/Finance_Bro_3000/blob/dd80b4a37a884c512b8255d750b3c540d6756926/Example/1.png)
**Pop-Up window**

![alt text](https://github.com/adxvl/Finance_Bro_3000/blob/dd80b4a37a884c512b8255d750b3c540d6756926/Example/2.png)
**User's input**

![alt text](https://github.com/adxvl/Finance_Bro_3000/blob/dd80b4a37a884c512b8255d750b3c540d6756926/Example/3.png)
**Data was found for AAPL**

![alt text](https://github.com/adxvl/Finance_Bro_3000/blob/dd80b4a37a884c512b8255d750b3c540d6756926/Example/4.png)
**The results**

![alt text](https://github.com/adxvl/Finance_Bro_3000/blob/dd80b4a37a884c512b8255d750b3c540d6756926/Example/Error_Example.png)
**An Error Example**

-----

**Prerequisites**

The program works with Python3.
In order to run it, please install the requirements from the requirements.txt file.
With pip, the requirements can be installed with a single line of code. More on this under instructions step 4.

-----

**Instructions**

1. Download the folder from GitHub
2. Unzip it
3. Install the requirements ```pip install -r requirements.txt```
4. Run ```Run_me.py```
5. Enter a ticker (e.g. AAPL) and a time period (e.g. 31.12.2010 - 31.12.2011)
6. Click "Check For Ticker"
7. If there is no error[^2] a button "Calculate" will appear. Click on it.
8. Watch the magic happen

-----

**Outlook**

To maximize the utility of this program, one needs to optimize it. One way would be to include different types of market returns as a reference point, such as the S&P 500. Another way would be to optimize the code and write it more smoothly and efficiently to reduce computation time and improve comprehension. The user interface is kept fairly simple, so there is room for improvement in this area. One could combine Python and HTML and create a web application that makes the program accessible online. Nevertheless, I will experiment with the code and optimize it in my spare time.


[^1]: Picture from https://www.etsy.com/ch/listing/1072807330/geldbecher-lustig-parodie-geschenk-gag
[^2]: If an error occurs, a message is displayed with the error and a "Clear" button will appear. Click on it in order to correct the entry and continue with step 7.
