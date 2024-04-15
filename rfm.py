import pandas as pd
import numpy as np

# Assuming your data is stored in a DataFrame called 'df'
# Replace 'df' with the actual name of your DataFrame

# 1. Tenure
df['hire_date'] = pd.to_datetime(df['hire_date'])
df['latest_timestamp'] = pd.to_datetime(df['time_stamp'].max())
df['tenure'] = (df['latest_timestamp'] - df['hire_date']).dt.days

# 2. Change in Salary
df['salary_change'] = df.groupby('employee_code')['normalized_salary'].pct_change()

# 3. Promotion Rate
df['promotion'] = df.groupby('employee_code')['job_level'].diff().fillna(0)

# 4. Manager Tenure
manager_tenure = df.groupby('manager')['tenure'].mean().rename('manager_tenure')
df = df.merge(manager_tenure, left_on='manager', right_index=True, how='left')

manager_manager_tenure = df.groupby("manager's_manager")["tenure"].mean().rename("manager_manager_tenure")
df = df.merge(manager_manager_tenure, left_on="manager's_manager", right_index=True, how="left")

# 5. Job Stability
df['job_changes'] = df.groupby('employee_code')['job_title'].diff().fillna(0)

# 6. Performance Trends (assuming 'employee_rating' is the performance rating column)
df['rating_change'] = df.groupby('employee_code')['employee_rating'].diff().fillna(0)

# 7. Engagement Score (customize based on your criteria)
df['engagement_score'] = (df['employee_rating'] * df['normalized_salary']) / (df['job_changes'] + 1)

# 8. Distance from Manager (assuming 'distance_from_ceo' is a column indicating the organizational distance)
df['distance_from_manager'] = df.groupby('manager')['distance_from_ceo'].transform('mean')

# 9. Peer Attrition Rate
peer_attrition_rate = df.groupby(['job_family', 'work_city'])['attrition'].mean().rename('peer_attrition_rate')
df = df.merge(peer_attrition_rate, left_on=['job_family', 'work_city'], right_index=True, how='left')

# 10. RFM Features
# Recency
df['recency'] = (df['latest_timestamp'] - pd.to_datetime(df['time_stamp'])).dt.days

# Frequency
df['frequency'] = df.groupby('employee_code')['time_stamp'].transform('count')

# Monetary Value
df['monetary_value'] = df.groupby('employee_code')['normalized_salary'].transform('mean')

# Drop intermediate columns
df.drop(['hire_date', 'latest_timestamp'], axis=1, inplace=True)

# Check the updated DataFrame
print(df.head())
