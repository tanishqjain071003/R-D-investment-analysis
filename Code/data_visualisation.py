import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go


data = pd.read_excel('/Users/tanishqjain/Desktop/4-1/SOP/Code/main_data.xlsx')


data['Year'] = pd.to_datetime(data['Year'], format='%Y')


numeric_data = data.select_dtypes(include='number')


correlation_matrix = numeric_data.corr()

# Correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap of Financial Metrics')
plt.show()

# Time Series of RD expenditure over years
plt.figure(figsize=(12, 6))
for company in data['Company'].unique():
    company_data = data[data['Company'] == company]
    plt.plot(company_data['Year'], company_data['RD'], label=company)
plt.title('R&D Expenditure Over Time by Company')
plt.xlabel('Year')
plt.ylabel('R&D Expenditure')
plt.legend(title='Company')
plt.show()

# Time Series for Profitability Metric - ROE over time
plt.figure(figsize=(12, 6))
for company in data['Company'].unique():
    company_data = data[data['Company'] == company]
    plt.plot(company_data['Year'], company_data['ROE'], label=company)
plt.title('Return on Equity (ROE) Over Time by Company')
plt.xlabel('Year')
plt.ylabel('ROE')
plt.legend(title='Company')
plt.show()


plt.figure(figsize=(10, 6))
sns.scatterplot(data=data, x='RD', y='ROA', hue='Company', palette='viridis', s=100)
plt.title('R&D Expenditure vs. Return on Assets (ROA)')
plt.xlabel('R&D Expenditure')
plt.ylabel('ROA')
plt.legend(title='Company')
plt.show()


# Aggregate RD by company
total_rd = data.groupby('Company')['RD'].sum().reset_index()

plt.figure(figsize=(12, 6))
sns.barplot(data=total_rd, x='Company', y='RD', palette='Blues_d')
plt.title('Total RD Expenditure by Company')
plt.xlabel('Company')
plt.ylabel('Total RD Expenditure')
plt.xticks(rotation=45)
plt.show()

# Trend Comparison of Key Profitability Ratios Across Companies
fig, ax = plt.subplots(3, 1, figsize=(12, 12), sharex=True)
profitability_metrics = ['ROA', 'ROE', 'EPS']
titles = ['Return on Assets (ROA)', 'Return on Equity (ROE)', 'Earnings Per Share (EPS)']

for i, metric in enumerate(profitability_metrics):
    for company in data['Company'].unique():
        company_data = data[data['Company'] == company]
        ax[i].plot(company_data['Year'], company_data[metric], label=company)
    ax[i].set_title(titles[i])
    ax[i].set_ylabel(metric)
    ax[i].legend(title='Company')

plt.xlabel('Year')
plt.suptitle('Profitability Metrics Over Time by Company')
plt.show()



# Time Series Analysis of Net Profit Ratio (NPR) Over Time by Company
plt.figure(figsize=(12, 6))
for company in data['Company'].unique():
    company_data = data[data['Company'] == company]
    plt.plot(company_data['Year'], company_data['NPR'], label=company)

plt.title('Net Profit Ratio (NPR) Over Time by Company')
plt.xlabel('Year')
plt.ylabel('Net Profit Ratio (NPR)')
plt.legend(title='Company')
plt.show()


# Scatter Plot of R&D Expenditure vs. Net Profit Ratio (NPR)
plt.figure(figsize=(10, 6))
sns.scatterplot(data=data, x='RD', y='NPR', hue='Company', palette='viridis', s=100)
plt.title('R&D Expenditure vs. Net Profit Ratio (NPR)')
plt.xlabel('R&D Expenditure')
plt.ylabel('Net Profit Ratio (NPR)')
plt.legend(title='Company')
plt.show()

