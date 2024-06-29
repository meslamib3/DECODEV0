import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, inspect

# Set the Streamlit page layout to wide
st.set_page_config(layout="wide")

# Define the SQLite database URL
database_url = 'sqlite:///decode_foundry_v0.db'

# Create a SQLAlchemy engine
engine = create_engine(database_url)

# Define the Streamlit app
st.title('DECODE FOUNDRY V0')

# Use CSS to adjust the font size and table layout
st.markdown(
    """
    <style>
    .big-font {
        font-size:24px !important;
    }
    .dataframe-table {
        font-size:20px !important; /* Increase the font size for table content */
        width:100% !important;
    }
    .stDataFrame th, .stDataFrame td {
        padding: 10px 10px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        font-size:20px !important; /* Increase the font size for table cells */
    }
    .stDataFrame table {
        width: 100%;
        table-layout: auto;  /* Adjust table-layout to auto for better column fit */
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Get the column names from the database
inspector = inspect(engine)
columns = [column['name'] for column in inspector.get_columns('papers')]

# Define a search input
search_term = st.text_input('Search for anything')

# Build the query based on the search term
query = 'SELECT * FROM papers'
if search_term:
    query += f" WHERE "
    query += " OR ".join(
        [f"`{col}` LIKE '%{search_term}%'" for col in columns]
    )

# Execute the query and display results
df = pd.read_sql(query, engine)

# Define a multiselect widget for columns, including the option to show all columns
options = ['Show all columns'] + columns
selected_columns = st.multiselect('Select columns to display', options, default=['Show all columns'])

# Filter the DataFrame based on selected columns
if 'Show all columns' in selected_columns:
    df_filtered = df
else:
    df_filtered = df[selected_columns]

st.write(f"Total results: {len(df_filtered)}")
st.dataframe(df_filtered)

# Allow users to download the filtered results
if not df_filtered.empty:
    csv = df_filtered.to_csv(index=False)
    st.download_button('Download CSV', csv, 'filtered_results.csv')
