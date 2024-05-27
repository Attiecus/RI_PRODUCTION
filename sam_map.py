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
from io import BytesIO
from rapidfuzz import process, fuzz

def trim_name(name):
    if pd.isna(name):
        return name  
    
    if isinstance(name, str):
        
        if 'c/o' in name.lower():
            name = name.split(' c/o', 1)[0]
        
       
        name = name.replace('L L C','').replace(' LLC', '').replace(' llc', '').replace(' L.L.C', '').replace(' l.l.c', '')

    return name.strip() 


@st.cache
def load_data(file_buffer, sheet_name=0):
    
    data = pd.read_excel(file_buffer, usecols=['INSURED_RI', 'SAM_GROUP_NAME'], sheet_name=sheet_name)
    data['INSURED_RI'] = data['INSURED_RI'].apply(lambda x: trim_name(x))
    return data


@st.cache(allow_output_mutation=True)
def match_sam_groups(file_buffer, sam_names_df):
    chunk_size = 1000
    chunks = pd.read_csv(file_buffer, chunksize=chunk_size, usecols=['INSURED', 'cluster id'])
    processed_chunks = []

    sam_names_dict = {trim_name(str(row['INSURED_RI']).lower()): row['SAM_GROUP_NAME'] for _, row in sam_names_df.iterrows() if pd.notna(row['INSURED_RI'])}

    for chunk in chunks:
        
        chunk['INSURED'] = chunk['INSURED'].apply(lambda x: trim_name(str(x)).lower() if pd.notna(x) else x)

       
        chunk['Matched SAM Group'] = chunk.apply(lambda row: find_matching_sam_group(row, sam_names_dict), axis=1)

        processed_chunks.append(chunk)

    return pd.concat(processed_chunks)


def find_matching_sam_group(customer_name, sam_names_dict):
    
    insured_value = customer_name['INSURED']
    if isinstance(insured_value, str):
       
        matches = process.extractOne(insured_value, sam_names_dict.keys(), scorer=fuzz.token_sort_ratio)
        
       
        if matches is None or matches[1] < 77:
            return 'No SAM Match'
        
        
        best_match = matches[0]
        
        return sam_names_dict[best_match]
    else:
       
        return 'No SAM Match'

def main():
    st.title("SAM Group Mapping")

    deduped_data_file = st.file_uploader("Upload Deduplicated Data", type=["csv"])
    sam_names_file = st.file_uploader("Upload SAM Names File", type=["xlsx"])

    if deduped_data_file and sam_names_file:
        
        sam_names_df = load_data(sam_names_file)

        
        with st.spinner("Matching data..."):
            processed_df = match_sam_groups(deduped_data_file, sam_names_df)

        st.success("Data matching completed.")
        st.dataframe(processed_df)

        
        towrite = BytesIO()
        processed_df.to_csv(towrite, index=False, header=True)
        towrite.seek(0)
        st.download_button("Download Mapped Data", towrite, "mapped_data.csv", "text/csv")

if __name__ == "__main__":
    main()
