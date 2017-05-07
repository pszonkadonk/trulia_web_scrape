import pandas as pd 
import numpy as np
from sklearn import cluster
from sklearn.preprocessing import normalize
from matplotlib import pyplot
from ZillowServices import ZillowServices
import statsmodels.api as sm
import seaborn as sns 


""" Return a normalized dataframe """

def normalize_dataframe(df):
    return (df-df.mean()) / (df.max() - df.min())


""" Run and plot a multiple linear regression
    to analyze the effect of tax assessment and 
    square feet of a home on the last sold price """

def tax_assessment_and_finished_sqft():

    zillow = ZillowServices()
    sales_df = zillow.get_zillow_sales_data("all_counties")
    sales_df = sales_df[['tax_assessment', 'finished_sqft', 'last_sold_price']]
    sales_df = sales_df.dropna()

    #normalize data
    sales_df_norm = normalize_dataframe(sales_df) 

    # Build, fit and plot model
    X = sales_df_norm[['tax_assessment', 'finished_sqft']]
    X = sm.add_constant(X)
    y = sales_df_norm['last_sold_price']

    model = sm.OLS(y, X, missing="drop").fit()
    print(model.summary())

    X = sales_df[['tax_assessment']]
    regression_plot = sns.regplot(x = X, y = y, data = sales_df_norm, scatter_kws={'s':4},
                line_kws={'color': 'black'}, color='red')
    regression_plot.set(xlabel="Tax Assessment (2015)", ylabel="Final Sale Price")

    sns.plt.show()

""" Run a regressoin to compare the age of a home
    on its final price """

def year_built(county_file):

    zillow = ZillowServices()
    sales_df = zillow.get_zillow_sales_data(county_file)
    sales_df = sales_df[['year_built', 'last_sold_price']]
    sales_df = sales_df.dropna()

    X = sales_df[['year_built']]
    X = sm.add_constant(X)
    y = sales_df['last_sold_price']


    model = sm.OLS(y, X, missing="drop").fit()

    print(model.summary())

    X = sales_df[['year_built']]
    regression_plot = sns.regplot(x = X, y = y, data = sales_df, scatter_kws={'s':4},
                line_kws={'color': 'black'}, color='purple')

    regression_plot.set(xlabel="Year Built", ylabel="Final Sale Price")

    sns.plt.show()

    """Runs a multiple linear regression on multiple dependent variables
        on the final sale price.  This includes tax assessment, square 
        footage, bathrooms, and bedrooms. """

def all_attributes(county_file):
    zillow = ZillowServices()
    sales_df = zillow.get_zillow_sales_data(county_file)
    sales_df = sales_df[['tax_assessment', 'finished_sqft', 'year_built',
                        'bathroom', 'bedrooms', 'last_sold_price']]
    sales_df = sales_df.dropna()

    sales_df_norm = normalize_dataframe(sales_df) 

    X = sales_df_norm[['tax_assessment', 'finished_sqft', 'year_built',
                        'bathroom', 'bedrooms']]
    X = sm.add_constant(X)
    y = sales_df_norm['last_sold_price']

    model = sm.OLS(y, X, missing="drop").fit()

    print(model.summary())

    X = sales_df_norm[['tax_assessment']]
    regression_plot = sns.regplot(x = X, y = y, data = sales_df_norm, scatter_kws={'s':4},
                line_kws={'color': 'black'}, color='purple')

    regression_plot.set(xlabel="Tax Assessment (2015)", ylabel="Final Sale Price")

    sns.plt.show()

"""Create binary dependent variable classifer on use code"""

def use_code_labeler(row, use_code):
    if(row['use_code'] == use_code):
        return 1
    else:
        return 0

"""Create binary classifier on independent county variable """

def county_labeler(row, county):
    if(row['county'].lower() == county.lower()):
        return 1
    else:
        return 0


"""Creates binary classifiers of dependent variables
    and runs a logistic regression to on a particular county.
    In addition, this function will compute confidence intervals
    as well as odd ratios """ 


def logit_county_predictor(county, county_file):

    zillow = ZillowServices()
    sales_df = zillow.get_zillow_sales_data(county_file)
    sales_df = sales_df.dropna()

    # remove homes that are not single family, condos, apts, or townhouses
    sales_df = sales_df[sales_df.use_code.isin(['SingleFamily', 'Condominium',
                                                 'Apartment', 'Townhouse', 'MultiFamily2To4'])]
    sales_df.ix[sales_df.use_code == 'Apartment', 'use_code'] = 'Condominium'
    sales_df.ix[sales_df.use_code == 'Townhouse', 'use_code'] = 'Condominium'

    sales_df['SingleFamily'] = sales_df.apply(lambda row: use_code_labeler(row, 'SingleFamily'), axis=1)
    sales_df['Condominium'] = sales_df.apply(lambda row: use_code_labeler(row,'Condominium'), axis=1)
    sales_df['MultiFamily2To4'] = sales_df.apply(lambda row: use_code_labeler(row,'MultiFamily2To4'), axis=1)
    

    sales_df['county_descriptor'] =  sales_df.apply(lambda row: county_labeler(row, county), axis=1)

    sales_df = sales_df[['county_descriptor', 'use_code', 'year_built','SingleFamily','Condominium',
                        'MultiFamily2To4', 'finished_sqft', 'bathroom', 'bedrooms']]

    sales_df['intercept'] = 1.0
    

    logit = sm.Logit(sales_df['county_descriptor'], sales_df[['Condominium','MultiFamily2To4', 
                                                            'finished_sqft', 'intercept']])
    logit.fit_regularized(maxiter=50)
                    

    result = logit.fit()

    print(result.summary())
    print(county + " confidence interval: ")
    print(result.conf_int())
    print(np.exp(result.params))
        

all_attributes("all_counties")
