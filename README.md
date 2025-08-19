# Customer Conversion Analysis: Regular → Premium

This project analyzes customer behavior to identify key differences between **Regular** and **Premium** customers, with the goal of improving conversion rates.

## Objectives
- Focus on Regular and Premium segments
- Identify factors influencing customer upgrade
- Support campaign strategy with data-driven insights

## Methods
- Data cleaning & preprocessing
- T-test (numerical variables)
- Chi-square test (categorical variables)
- Distribution analysis & visualization

## Tools
- Python: `pandas`, `seaborn`, `scipy`, `matplotlib`
- PowerBI

## Process:
1. **Data Preparation and EDA**  
   - Import dataset, handle missing values, encode categorical variables
   - Perform basic EDA (describe infomation, check unique values, spot data issues)
   - Standardize time columns (convert all dates to the same format and divide into groups)

2. **Statistical Testing**  
   - **T-test**: Validate numerical differences (Age, Total_Amount)  
   - **Chi-square**: Test categorical variables (Gender, Income, Country, Product_Category, Shipping_Method, Ratings, Month_Year, Payment Method, Order Status) 

4. **Segment Significant Difference**  
   - Highlight key features where Premium significantly differs from Regular  
   - Visualize the differs using barplot

5. **Dashboard Visualization**  
   - Visualize customer demographics and behaviors in Power BI dashboard
   - Highlight patterns in age, gender, income, product categories, ratings, and monthly transactions

6. **Campaign Design**  
   - Define customer personas for targeted promotions  
   - Build a data-driven campaign plan aiming at 10% conversion growth  

## Key Insights
- Variables like **Income**, **Order Status**, and **Product Category** show significant differences between segments.
- Visual patterns help shape targeted marketing strategies.

## Summary Campaign Strategy

Based on data insights, a multi-channel campaign strategy is proposed to increase Premium customer conversion by at least 10% within 12 months. The focus is on medium-to-high income customers in key product categories: **Electronics**, **Home Decor**, **Books**, and **Clothing**.

The campaign highlights:
- Personalized benefits of Premium membership (e.g. early access, exclusive recommendations)
- Targeting customers aged 21–27, especially in high-income regions (e.g. US, UK)
- Using behavioral traits (e.g. low product ratings, payment/shipping preferences) to tailor promotions
- Deployed in peak buying months (Jan, Apr, Jul) via email, ads, chatbot, and gamified interactions
