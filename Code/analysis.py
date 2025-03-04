# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from linearmodels.panel import PanelOLS, RandomEffects
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.stattools import durbin_watson
from scipy import stats

# Load the dataset
data = pd.read_excel('main_data.xlsx')

# Data Preparation
data['Year'] = pd.to_datetime(data['Year'], format='%Y')
data.set_index(['Company', 'Year'], inplace=True)

# Ensure all data types are correct
data = data.astype({
    'RD': 'float',
    'NPR': 'float',
    'ROA': 'float',
    'ROE': 'float',
    'EPS': 'float',
    'Total Assets': 'float'
})

# Handle missing values
data = data.dropna()

# Create new variables
data['RD_Intensity'] = data['RD'] / data['Total Assets']
data['Log_RD'] = np.log(data['RD'] + 1)
data['Log_Total_Assets'] = np.log(data['Total Assets'] + 1)

# Update independent variables
# You can choose to use RD_Intensity or Log_RD and Log_Total_Assets
independent_vars = ['const', 'RD_Intensity']
# Alternatively, if you prefer log transformations:
# independent_vars = ['const', 'Log_RD', 'Log_Total_Assets', 'D/E ratio']

# Add constant term
data['const'] = 1

# Function to perform regression analysis for each dependent variable
def panel_regression(dependent_var):
    print(f"\nAnalyzing impact on {dependent_var}:")
    
    # Prepare exogenous variables
    exog_vars = data[independent_vars]
    
    # Fixed Effects Model
    model_fe = PanelOLS(data[dependent_var], exog_vars, entity_effects=True)
    results_fe = model_fe.fit(cov_type='robust')
    print("\nFixed Effects Model Results:")
    print(results_fe.summary)
    
    # Random Effects Model
    model_re = RandomEffects(data[dependent_var], exog_vars)
    results_re = model_re.fit()
    print("\nRandom Effects Model Results:")
    print(results_re.summary)
    
    # Hausman Test
    def hausman_test(fe, re):
        b = fe.params
        B = re.params
        v_b = fe.cov
        v_B = re.cov
        diff = b - B
        df = len(b)
        chi2 = np.dot(np.dot(diff.T, np.linalg.inv(v_b - v_B)), diff)
        pval = stats.chi2.sf(chi2, df)
        return chi2, pval
    
    chi2, pval = hausman_test(results_fe, results_re)
    print("\nHausman Test:")
    print(f"Chi-squared: {chi2:.2f}")
    print(f"P-value: {pval:.4f}")
    
    if pval < 0.05:
        print("Reject the null hypothesis. Use Fixed Effects model.")
        chosen_model = 'Fixed Effects'
    else:
        print("Fail to reject the null hypothesis. Use Random Effects model.")
        chosen_model = 'Random Effects'
    
    # Assumptions Checks
    residuals = results_fe.resids if chosen_model == 'Fixed Effects' else results_re.resids
    fitted = results_fe.fitted_values if chosen_model == 'Fixed Effects' else results_re.fitted_values
    
    # Durbin-Watson Test
    dw_stat = durbin_watson(residuals)
    print(f"\nDurbin-Watson statistic: {dw_stat:.2f}")
    
    # Multicollinearity Check
    # vif_df = pd.DataFrame()
    # exog_vars_vif = exog_vars.drop(columns=['const'])
    # vif_df['Variable'] = exog_vars_vif.columns
    # vif_df['VIF'] = [variance_inflation_factor(exog_vars_vif.values, i) for i in range(exog_vars_vif.shape[1])]
    # print("\nVariance Inflation Factor (VIF):")
    # print(vif_df)

# Dependent Variables
dependent_vars = ['NPR', 'ROA', 'ROE', 'EPS']

# Perform regression analysis for each dependent variable
for dep_var in dependent_vars:
    panel_regression(dep_var)
