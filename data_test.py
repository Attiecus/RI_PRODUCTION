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
import pandas_dedupe
from io import BytesIO
from datetime import time 
import datetime

def process_file(df):
    with st.spinner("Deduplicating data..."):
        deduped_df = pandas_dedupe.dedupe_dataframe(df, ['LOB','POLNO','INSURED','OF_PARTY_NUMBER'], sample_size=0.3)
    st.success("Data deduplicated successfully.")
    return deduped_df.sort_values(by="cluster id", ascending=True)

def main():
    st.title("Data Deduplication")
    uploaded_file = st.file_uploader("Upload filtered data (Excel file)", type=['xlsx'])
    if uploaded_file is not None:
        
        with st.spinner("Loading data..."):
            df = pd.read_excel(uploaded_file)

        if not df.empty:
           
            st.write("Number of records:", len(df))

            start_time = datetime.datetime.now()
            
            deduped_df = process_file(df)
            
               

            end_time = datetime.datetime.now()

            st.dataframe(deduped_df, width=5000)
            
            towrite = BytesIO()
            deduped_df.to_csv(towrite, index=False, header=True)
            towrite.seek(0)
            st.download_button("Download Deduped Data", towrite, "deduped_data.csv", "text/csv")
            
            st.write(f"Process started at: {start_time}")
            st.write(f"Process ended at: {end_time}")
        else:
            st.warning("The DataFrame is empty.")

if __name__ == "__main__":
    main()
