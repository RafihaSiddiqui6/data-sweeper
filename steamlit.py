#imports
import streamlit as st 
import pandas as pd
import os 
from io import BytesIO

# Set up our App
st.set_page_config(page_title="💿 Data Sweeper", layout="wide")
st.title("💿 Data Sweeper")
st.markdown("""
    Transform your files between **CSV** and **Excel** formats with built-in data cleaning and visualization!
""")

# File uploader section
st.markdown("### 📤 Upload Your Files (CSV or Excel):")
uploaded_files = st.file_uploader("Choose your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Process the file based on its extension
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # Display file information
        st.markdown(f"### File Info: {file.name}")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**File Name**: {file.name}")
        with col2:
            st.write(f"**File Size**: {file.size / 1024:.2f} KB")

        # Display Dataframe preview
        st.markdown("### 🔍 Data Preview (First 5 Rows):")
        st.dataframe(df.head())

        # Data cleaning options section
        st.markdown("### 🛠️ Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates Removed!")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing Values Filled!")

        # Column selection section
        st.markdown("### 🎯 Select Columns to Include or Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns.tolist(), default=df.columns.tolist())
        df = df[columns]

        # Data visualization section
        st.markdown("### 📊 Data Visualization")
        if st.checkbox(f"Show Data Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Conversion options (CSV or Excel)
        st.markdown("### 🔄️ Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
            buffer.seek(0)

            # Download Button
            st.download_button(
                label=f"⬇️ Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

# Success message after processing all files
st.markdown("### 🎉 All Files Successfully Processed!")
