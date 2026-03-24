# Basic Machine Learning Example for Beginners
# This script will help you understand the ML workflow step by step

# Step 1: Import libraries
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Step 2: Create a simple dataset
# Example: Predict salary based on years of experience

data = {
    "YearsExperience": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Salary": [30000, 35000, 40000, 50000, 55000, 65000, 70000, 80000, 85000, 95000]
}

df = pd.DataFrame(data)

print("Dataset:\n", df)

# Step 3: Split features (X) and target (y)
X = df[["YearsExperience"]]  # Input feature
y = df["Salary"]           # Output label

# Step 4: Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("\nTraining Data:\n", X_train)
print("\nTesting Data:\n", X_test)

# Step 5: Create and train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Step 6: Make predictions
predictions = model.predict(X_test)

print("\nPredictions:", predictions)

# Step 7: Evaluate the model
mse = mean_squared_error(y_test, predictions)
print("\nMean Squared Error:", mse)

# Step 8: Try your own prediction
years = float(input("\nEnter years of experience to predict salary: "))
predicted_salary = model.predict([[years]])
print(f"Predicted Salary for {years} years experience: {predicted_salary[0]}")

# -----------------------------
# What you learned:
# 1. Data creation
# 2. Feature & label separation
# 3. Train-test split
# 4. Model training
# 5. Prediction
# 6. Evaluation
# -----------------------------

# Next steps for you:
# - Try different models (DecisionTreeRegressor, RandomForest)
# - Use real datasets (CSV files)
# - Add visualization (matplotlib)
# - Learn classification problems (Logistic Regression)
