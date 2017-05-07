import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
from sklearn.linear_model import LinearRegression
import numpy as np


def currency_fmt(x, y):
    x = int(x)
    return "${0:,}".format(x)

def run_regression_price_squarefeet(filename):
    
    home_data = pd.read_csv(filename, encoding="latin1")
    home_data = home_data[home_data.price < 1500000]
    home_data = home_data[home_data.square_feet < 2500]

    price = home_data[['price']]
    square_feet = home_data[['square_feet']]
    
    model = LinearRegression().fit(square_feet, price)

    m = model.coef_[0]
    b = model.intercept_
    print("formula y= {0}x + {1}".format(m, b))

    ax = plt.subplot()
    plt.xticks(fontsize= 8)
    plt.yticks(fontsize=8)
    

    plt.scatter(square_feet, price , color="purple", s=4.5)
    ax.yaxis.set_major_formatter(tkr.FuncFormatter(currency_fmt))
    

    plt.plot(square_feet, model.predict(square_feet), color='black', linewidth=2)

    plt.title("Jersey City Housing Price Against Square Feet")
    plt.ylabel("Price")
    plt.xlabel("Square Feet")

    plt.show()

def plot_price_years(filename):
    home_data = pd.read_csv(filename, encoding="latin1")
    home_data = home_data[home_data.price < 1500000]

    ax = plt.subplot()
    ax.yaxis.set_major_formatter(tkr.FuncFormatter(currency_fmt))


    homes_1870_to_1889 = home_data[(home_data.year >= 1870) & (home_data.year <=1889)]
    homes_1890_to_1909 = home_data[(home_data.year >= 1890) & (home_data.year <=1909)]
    homes_1910_to_1929 = home_data[(home_data.year >= 1910) & (home_data.year <=1929)]
    homes_1930_to_1949 = home_data[(home_data.year >= 1930) & (home_data.year <=1949)]
    homes_1930_to_1949 = home_data[(home_data.year >= 1930) & (home_data.year <=1949)]
    homes_1950_to_1969 = home_data[(home_data.year >= 1950) & (home_data.year <=1969)]
    homes_1970_to_1989 = home_data[(home_data.year >= 1970) & (home_data.year <=1989)]
    homes_1990_to_2009 = home_data[(home_data.year >= 1990) & (home_data.year <=2009)]
    homes_2010_to_2029 = home_data[(home_data.year >= 2010) & (home_data.year <=2029)]

    plt.scatter(homes_1870_to_1889[['year']], homes_1870_to_1889[['price']], color = "red", label='1870-1889', s=25)
    plt.scatter(homes_1890_to_1909[['year']], homes_1890_to_1909[['price']], color = "blue", label='1890-1909', s=25)
    plt.scatter(homes_1910_to_1929[['year']], homes_1910_to_1929[['price']], color = "yellow", label='1910-1929', s=25)
    plt.scatter(homes_1930_to_1949[['year']], [homes_1930_to_1949['price']], color = "green", label='1930-1949', s=25)
    plt.scatter(homes_1950_to_1969[['year']], homes_1950_to_1969[['price']], color = "purple", label='1950-1969', s=25)
    plt.scatter(homes_1970_to_1989[['year']], homes_1970_to_1989[['price']], color = "pink", label='1970-1989', s=25)
    plt.scatter(homes_1990_to_2009[['year']], homes_1990_to_2009[['price']], color = "cyan", label='1990-2009', s=25)
    plt.scatter(homes_2010_to_2029[['year']], homes_2010_to_2029[['price']], color = "magenta", label='2010-2029', s=25)

    plt.legend(loc="upper right", fontsize=8, ncol=2)
    
    plt.xticks()
    plt.yticks()

    plt.title("Jersey City Homes | Year Built")
    plt.ylabel("Price")
    plt.xlabel("Year")

    plt.show()





if __name__=='__main__':

    # home_data_string = "home_detail-cleaned.csv"
    # run_regression_price_squarefeet(home_data_string)

    home_data_string = "home_detail-cleaned-year.csv"
    plot_price_years(home_data_string)