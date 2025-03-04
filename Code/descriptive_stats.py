import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew, kurtosis

# Load dataset
data = pd.read_excel('/Users/tanishqjain/Desktop/4-1/SOP/Code/main_data.xlsx')

data = data.select_dtypes(include='number')
metrics = ['RD','NPR', 'ROA', 'ROE', 'EPS']

# Descriptive Statistics Summary
desc_stats = data.describe().T  # Transpose for better readability
desc_stats['median'] = data.median()  # Adding the median column
desc_stats['iqr'] = data.quantile(0.75) - data.quantile(0.25)  # Interquartile range (IQR)



# Display the descriptive statistics summary
print("Descriptive Statistics Summary:")
print(desc_stats)

skewness = data[metrics].apply(skew)
kurt = data[metrics].apply(kurtosis)

# Print skewness and kurtosis
print("Skewness of Key Financial Metrics:\n", skewness)
print("\nKurtosis of Key Financial Metrics:\n", kurt)
