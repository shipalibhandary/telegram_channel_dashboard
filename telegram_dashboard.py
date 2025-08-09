import pandas as pd
import streamlit as st

# Load CSV file
df = pd.read_csv("small_channel_metadata.csv")

# Convert timestamp to readable date (if needed)
df['creation_date'] = pd.to_datetime(df['creation_date'], unit='s')

# Add 'year' column once early (for chart)
df['year'] = df['creation_date'].dt.year

st.set_page_config(page_title="Telegram Dashboard", layout="wide")


# Page Title
st.title("📊Telegram Channel Explorer Dashboard")

st.markdown("""
    <style>
    /* Change background color */
    .stApp {
        background-color: #0e1117;
    }

    /* Style metric cards */
    div[data-testid="metric-container"] {
        background-color: #1e1e1e;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 0.5rem;
    }

    /* Improve text appearance */
    .main, .css-1v0mbdj {
        font-family: 'Segoe UI', sans-serif;
        color: #F5F5F5;
    }

    /* Style selectbox text */
    .css-1cpxqw2 {
        color: #ffffff;
    }

    /* Profile detail icons and spacing */
    .channel-profile {
        font-size: 18px;
        line-height: 1.6;
    }

    </style>
""", unsafe_allow_html=True)


# Sidebar filters
st.sidebar.header("🔎 Filter Channels")
search = st.sidebar.text_input("Search by Username or Title")
min_subs = st.sidebar.slider("Minimum Subscribers", 0, int(df['n_subscribers'].max()), 0)
verified_only = st.sidebar.checkbox("Show Only Verified Channels")
row_limit = st.sidebar.slider("Rows to display", 10, 500, 100)

# Apply filters
filtered = df.copy()
if search:
    filtered = filtered[
        filtered['username'].str.contains(search, case=False, na=False) |
        filtered['title'].str.contains(search, case=False, na=False)
    ]
filtered = filtered[filtered['n_subscribers'] >= min_subs]
if verified_only:
    filtered = filtered[filtered['verified'] == True]

# Show metrics
st.metric("Total Channels", len(filtered))
st.metric("Verified", filtered['verified'].sum())

# --- Pagination for Filtered Table ---
st.subheader("📋 Filtered Channel Results")

# Set number of rows per page
rows_per_page = st.selectbox("Rows per page:", [10, 25, 50, 100, 200], index=2)

# Total pages
total_rows = len(filtered)
total_pages = (total_rows - 1) // rows_per_page + 1

# Page selector
page = st.number_input("Page number", min_value=1, max_value=total_pages, value=1, step=1)

# Paginate the filtered data
start = (page - 1) * rows_per_page
end = start + rows_per_page
paginated_data = filtered.iloc[start:end]

# Display paginated table
st.write(f"Showing rows {start+1} to {min(end, total_rows)} of {total_rows}")
st.dataframe(paginated_data)


# Optional: Add safe chart
st.subheader("📈 Top 10 Channels by Subscribers")
top10 = filtered.sort_values("n_subscribers", ascending=False).head(10)
st.bar_chart(top10.set_index('username')['n_subscribers'])

st.subheader("📅 Channels Created Over Time")
year_counts = filtered['year'].value_counts().sort_index()
st.bar_chart(year_counts)

selected = st.selectbox("Select a channel", filtered['username'])
profile = filtered[filtered['username'] == selected].iloc[0]
st.markdown(f"""
💖 **Title** : &nbsp;{profile['title']}  
🔗 **Username** : &nbsp;`{profile['username']}`  
👥 **Subscribers** : &nbsp;{profile['n_subscribers']}  
📅 **Created** : &nbsp;{profile['creation_date'].date()}  
✅ **Verified** : &nbsp;{'✔️ Yes' if profile['verified'] else '❌ No'}
""", unsafe_allow_html=True)






