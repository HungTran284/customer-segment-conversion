#%% IMPORT LIBRARIES
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import ttest_ind, chi2_contingency

#%% LOAD DATA
df = pd.read_csv('new_retail_data.csv')

#%% CONFIGS
plt.rcParams['font.size'] = 16
plt.rcParams['figure.dpi'] = 120

#%% DELETE COLUMN THAT IS NOT RELEVANT
df.drop(columns=['Transaction_ID','Name','Email',
                 'Phone','Address','City','State','Zipcode',
                 'products','Product_Brand',
                 'Product_Type','Feedback','Total_Purchases',
                 'Amount','Date'], inplace=True)
print(df.head())

#%% FILTER: KEEP ONLY 'REGULAR' AND 'PREMIUM' IN CUSTOMER_SEGMENT
print("\n--- Lọc dữ liệu để tập trung vào giá trị 'Regular' và 'Premium' (Loại bỏ giá trị 'New')---")
segments_to_keep = ['Regular', 'Premium']
df = df[df['Customer_Segment'].isin(segments_to_keep)].copy()
print(f"Đã lọc dữ liệu, số dòng còn lại: {len(df)}")
print("Các phân tích từ đây sẽ thực hiện trên 2 nhóm 'Regular' và 'Premium'.\n")

# PREPROCESSING
#%% VIEW DATA SHAPE
print('Shape of dataframe:', df.shape)

#%% CHECK DATA INFO
df.info()

#%% CHECK FOR DUPLICATES ROWS
num_duplicate_rows = df.duplicated().sum()
print('Number of duplicated rows in dataset:', num_duplicate_rows)

#%% REMOVE DUPLICATES ROW
df = df.drop_duplicates()

#%% CHECK FOR DUPLICATES VALUE
unique_counts = df.nunique()
print(unique_counts)

#%% CHECK FOR MISSING VALUES
missing_values = df.isnull().sum()
missing_percent = (missing_values / len(df)) * 100
missing_data = pd.DataFrame({
    'Missing Values': missing_values,
    'Percentage (%)': missing_percent
})
print(missing_data)
print(missing_values.sum())

#%% REMOVE ROWS WITH MISSING VALUES
df = df.dropna()
print(f"Số dòng sau khi xóa các giá trị thiếu: {len(df)}")

#%% CONVERT MONTH YEAR DATA
df['Month_Year'] = df['Month'].astype(str) + '-' + df['Year'].astype(str)
months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]
years = ['2023.0', '2024.0']

month_year_order = [f"{month}-{year}" for year in years for month in months]

df['Month_Year'] = pd.Categorical(df['Month_Year'],categories=month_year_order,
                                  ordered=True)
df.drop(columns=['Month', 'Year'], inplace=True)

# CONVERT TIME DATA
#%% CONVERT DATA STRUCTURE OF TIME VARIABLE
df["Time_dt"] = pd.to_datetime(df["Time"], format="%H:%M:%S")

#%% EXTRACT HOUR AND MINUTE DATA
df["Hour"] = df["Time_dt"].dt.hour
df["Minute"] = df["Time_dt"].dt.minute

#%% DIVIDE INTO 24 HOUR GROUPS
df["Hour_Group"] = df.apply(
    lambda row: (row["Hour"] if row["Minute"] < 30 else (row["Hour"] + 1) % 24),
    axis=1
)
df.drop(columns=['Time','Time_dt', 'Hour', 'Minute'], inplace=True)
df["Hour_Group"] = pd.Categorical(df["Hour_Group"], categories=range(24), ordered=True)

#%% ANALYZE CORRELATION USING T-TEST BETWEEN CONTINUOUS VARIABLES AND DEPENDENT VARIABLE (CUSTOMER_SEGMENT)
numerical_vars = ['Age', 'Total_Amount']

print("\n--- Phân tích tương quan T-test cho các biến số ---")
for var in numerical_vars:
    try:
        group1 = df[df['Customer_Segment'] == 'Regular'][var]
        group2 = df[df['Customer_Segment'] == 'Premium'][var]

        t_stat, p_val = ttest_ind(group1, group2, equal_var=False)

        print(f"{var}: t = {t_stat:.4f}, p = {p_val:.4f}")
        if p_val < 0.05:
            print(f"   → Biến '{var}' có khác biệt có ý nghĩa giữa 2 nhóm.")
        else:
            print(f"   → Biến '{var}' KHÔNG có khác biệt rõ rệt giữa 2 nhóm.")
    except Exception as e:
        print(f"{var}: lỗi khi tính T-test: {e}")

#%% ANALYZE CORRELATION USING CHI-SQUARE TEST BETWEEN CATEGORICAL VARIABLES AND DEPENDENT VARIABLE (CUSTOMER_SEGMENT)
categorical_vars = ['Gender','Income','Country','Product_Category',
                    'Shipping_Method','Payment_Method','Order_Status',
                    'Ratings','Hour_Group', 'Month_Year']

print("\n--- Phân tích Chi-square cho các biến phân loại ---")
for var in categorical_vars:
    try:
        ct = pd.crosstab(df[var], df['Customer_Segment'])

        if ct.shape[1] != 2:
            print(f"{var}: bỏ qua (không phải phân loại nhị phân)")
            continue

        chi2, p, dof, expected = chi2_contingency(ct)

        print(f"{var}: chi2 = {chi2:.4f}, p = {p:.4f}")
        if p < 0.05:
            print(f"   → Biến '{var}' có liên hệ với nhóm Customer_Segment.")
        else:
            print(f"   → Biến '{var}' KHÔNG có liên hệ rõ rệt.")
    except Exception as e:
        print(f"{var}: lỗi khi chạy Chi-square: {e}")

#%% ANALYZE PROPORTION DIFFERENCE BETWEEN 'REGULAR' AND 'PREMIUM' IN CATEGORICAL VARIABLES (DIFFERENCE >= 40%)

print("\n--- Phân tích tỷ lệ Regular vs Premium theo từng biến phân loại ---")

important_cats = ['Gender','Income','Country','Product_Category',
                    'Shipping_Method','Payment_Method','Order_Status','Ratings']

diff_threshold = 0.4

for var in important_cats:
    try:
        ct = pd.crosstab(df[var], df['Customer_Segment'], normalize='index')
        ct['Diff'] = abs(ct['Premium'] - ct['Regular'])

        sig_diff = ct[ct['Diff'] >= diff_threshold].sort_values('Diff', ascending=False)

        if not sig_diff.empty:
            print(f"\n>>> Biến '{var}' có giá trị chênh lệch lớn (>|{diff_threshold*100:.0f}%|):")
            print(sig_diff)

            sig_diff[['Premium', 'Regular']].plot(kind='barh', figsize=(8, 4), color=['#1f77b4', '#ff7f0e'])
            plt.title(f"Tỷ lệ Premium vs Regular theo '{var}' (chênh lệch > {diff_threshold*100:.0f}%)")
            plt.xlabel("Tỷ lệ (%)")
            plt.grid(axis='x', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.show()

    except Exception as e:
        print(f"{var}: lỗi khi phân tích tỷ lệ: {e}")

#%% PLOT AGE DISTRIBUTION BY CUSTOMER SEGMENT
plt.figure(figsize=(10, 10))

sns.histplot(data=df, x='Age', hue='Customer_Segment', multiple='stack',
             bins=50, palette={'Premium': '#ff9999', 'Regular': '#99ccff'})

plt.title("Phân bố độ tuổi theo nhóm khách hàng (Regular vs. Premium)", fontsize=14)
plt.xlabel("Độ tuổi", fontsize=12)
plt.ylabel("Số lượng khách hàng", fontsize=12)
plt.legend(title="Nhóm khách hàng")
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

#%% PLOT MONTH_YEAR DISTRIBUTION BY CUSTOMER SEGMENT
plt.figure(figsize=(10, 10))

sns.histplot(data=df, x='Month_Year', hue='Customer_Segment', multiple='stack',
             shrink=0.8, palette={'Premium': '#ff9999', 'Regular': '#99ccff'})

plt.title("Phân bố thời gian mua hàng theo nhóm khách hàng (Regular vs. Premium)", fontsize=14)
plt.xlabel("Thời gian (Month-Year)", fontsize=12)
plt.ylabel("Số lượng đơn hàng", fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.legend(title="Nhóm khách hàng")
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

#%%
df.to_csv('data/filtered_retail_data.csv', index=False)

#%%
df1 = pd.read_csv('data/filtered_retail_data.csv')
missing_values = df1.isnull().sum()
missing_percent = (missing_values / len(df1)) * 100
missing_data = pd.DataFrame({
    'Missing Values': missing_values,
    'Percentage (%)': missing_percent
})
print(missing_data)
print(missing_values.sum())