"""
***********************************************************************
This code was created by Atharva Godkar on the 21st of May 2024
for ADNIC information technology team.
The below code consists of various ML,fuzzy and data sorting techniques
to smoothen the process of data grouping and transformation

DATA MAY DISAPPOINT BUT IT NEVER LIES
ENJOY THE CODE!!
***********************************************************************
"""
import streamlit as st
import pandas as pd
import os
import re
import numpy as np


st.set_page_config(layout="wide")
os.environ['PANDASAI_API_KEY'] = 'your_secure_api_key_here'


def trim_name(name):
    if pd.isna(name):
        return name
    
    if isinstance(name, str):
        
        name = re.split(r'\s+c\s*\/\s*o\s+', name, flags=re.IGNORECASE)[0]

       
        name = name.replace('L L C','').replace('LlC', '').replace('LLC', '').replace(' llc', '').replace(' L.L.C', '').replace(' l.l.c', '').replace('L.L.C.', '').replace(' L.L.C.', '')

    return name.strip()  


def load_data(file_path):
    with st.spinner("Loading and filtering data..."):
       
        df = pd.read_excel(file_path)

        
        st.write("Data Types:", df.dtypes)

        
        df['OF_PARTY_NUMBER'] = pd.to_numeric(df['OF_PARTY_NUMBER'], errors='coerce')

       
        df.loc[df['OF_PARTY_NUMBER'].notna(), 'OF_PARTY_NUMBER'] = df['OF_PARTY_NUMBER'].dropna().astype(int)

        
        excluded_lobs = ['INDIVIDUAL TPL', 'INDIVIDUAL COMPREHENSIVE', 'INDIVIDUAL SHIFA', 'INDIVIDUAL EBP', 'INDIVIDUAL LIFE-UNIT LINKED']
        df = df[~df['MINOR_LOB'].isin(excluded_lobs)]

        
        excluded_party_numbers = [19186, 21246, 2625, 2607]
        df = df[~df['OF_PARTY_NUMBER'].isin(excluded_party_numbers) | df['OF_PARTY_NUMBER'].isna()]

        
        df['INSURED'] = df['INSURED'].apply(trim_name)
        df = df.applymap(lambda x: trim_name(x) if isinstance(x, str) else x)

        st.text("Data loaded and filtered successfully.")
        return df





def download_file(default_filename):
    
    base, ext = os.path.splitext(default_filename)
    if ext.lower() != '.csv':
        default_filename = base + '.csv'  
    
    i = 1
    new_filename = default_filename
    while os.path.exists(new_filename):
        new_filename = f"{base}_{i}.csv"
        i += 1
    
    return new_filename


def main():
    st.title("Data Filtering and Trimming 1")
    file_path = st.file_uploader("Upload Excel file", type=['xlsx'])
    if file_path is not None:
        df = load_data(file_path)
        st.dataframe(df)

       
        if st.button("Download Filtered Data as CSV"):
            csv_file_path = download_file("filtered_data.csv")
            df.to_csv(csv_file_path, index=False)
            st.success(f"Filtered data downloaded successfully as '{os.path.basename(csv_file_path)}'.")


if __name__ == "__main__":
    main()
