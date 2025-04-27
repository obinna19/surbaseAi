import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Configure page settings
st.title("Cybersecurity Incident Analysis Dashboard")

# File upload
uploaded_file = st.file_uploader("Upload your security dataset (CSV)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Check for required columns
    required_cols = ['location', 'target_system', 'attack_severity', 'year']
    if not all(col in df.columns for col in required_cols):
        st.error(f"Dataset must contain these columns: {','.join(required_cols)}")
        st.stop()

    #Clean data
    df = df.dropna(subset=required_cols)

    # Metric Cards
    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", len(df))
    with col2:
        st.metric("Unique Locations", df['location'].nunique())
    with col3:
        st.metric("Avg Attack Severity", f"{df['attack_severity'].mean():.1f}")
    with col4:
        missing_values = df.isnull().sum().sum()
        st.metric("Missing Values", missing_values)
    
    # Visualization section
    st.subheader("Attack Analysis")

    # First row of charts
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Attacks by Location**")
        location_counts = df['location'].value_counts().head(10)
        fig, ax = plt.subplots()
        location_counts.plot(kind='bar', ax=ax, color='#FF4B4B')
        plt.xticks(rotation=45)
        st.pyplot(fig)

    with col2:
        st.write("**Target System Distribution**")
        system_counts = df['target_system'].value_counts()
        fig, ax = plt.subplots()
        system_counts.plot(kind='pie', ax=ax, autopct='%1.1f%%')
        st.pyplot(fig)

    
    # Second row of charts
    col3, col4 = st.columns(2)
    with col3:
        st.write("**Attack Severity Distribution**")
        severity_counts = df['attack_severity'].value_counts()
        fig, ax = plt.subplots()
        severity_counts.plot(kind='barh', ax=ax, color='#00FF00')
        plt.xlabel("Year")
        plt.ylabel("Number of Attacks")
        st.pyplot(fig)

    with col4:
        st.write("**Attack Over Years**")
        year_counts = df['year'].value_counts().sort_index()
        fig, ax = plt.subplots()
        year_counts.plot(kind='line', ax=ax, marker='o', color='#800080')
        plt.xlabel("Year")
        plt.ylabel("Number of Attacks")
        st.pyplot(fig)

    # Correlation matrix
    st.subheader("Feature Correlation")
    numeric_df = df.select_dtypes(include=['number'])
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)


    # Data quality section
    st.subheader("Data Quality Analysis")
    missing_data = df.isnull().sum()
    fig, ax = plt.subplots()
    missing_data[missing_data > 0].plot(kind='bar', ax=ax, color='#FFA500')
    plt.title("Missing Values per Column")
    st.pyplot(fig)

else:
    st.info("Please upload a CSV file to begin analysis")

# Add some Styling
st.markdown("""
<style>
    .stMetric {background-color: #0E1117; border-radius: 5px; padding:15px}
    .st-bq {border-color: #FF4B4B}
</style>
""")

