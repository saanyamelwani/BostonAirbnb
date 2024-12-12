import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt

# Load the dataset
@st.cache_data
def load_data():
    # Ensure your CSV files are correctly named and uploaded to the repository
    listings = pd.read_csv("listings.csv")
    return listings

data = load_data()

# Title and introduction
st.title("Boston Airbnb Data Explorer")
st.markdown("""
This application helps you explore Airbnb data in Boston. You can analyze:
1. Average listing prices by neighborhood.
2. Apartments under a specific price in a selected neighborhood.
3. Highly rated Airbnbs in different neighborhoods.
4. Interactive map of affordable or highly rated Airbnbs.
""")

# Sidebar for user inputs
st.sidebar.title("Filters")

# Query 1: Average Listing Price by Neighborhood
st.header("1. Average Listing Price by Neighborhood")
selected_neighborhood = st.sidebar.selectbox("Select Neighborhood", ["All"] + list(data["neighbourhood"].unique()))
if selected_neighborhood == "All":
    avg_prices = data.groupby("neighbourhood")["price"].mean().sort_values()
    st.subheader("Bar Chart of Average Prices")
    fig, ax = plt.subplots()
    avg_prices.plot(kind="bar", ax=ax, color="skyblue")
    ax.set_title("Average Prices by Neighborhood")
    ax.set_ylabel("Average Price ($)")
    st.pyplot(fig)
else:
    avg_price = data[data["neighbourhood"] == selected_neighborhood]["price"].mean()
    st.write(f"Average price in {selected_neighborhood}: ${avg_price:.2f}")

# Query 2: Apartments Under a Specific Price
st.header("2. Find Apartments Under a Specific Price")
price_limit = st.sidebar.slider("Set Maximum Price", min_value=int(data["price"].min()), max_value=int(data["price"].max()), value=100)
selected_neighborhood_2 = st.sidebar.selectbox("Select Neighborhood for Price Filter", ["All"] + list(data["neighbourhood"].unique()), key="price_neighborhood")

if selected_neighborhood_2 == "All":
    filtered_data = data[data["price"] <= price_limit]
else:
    filtered_data = data[(data["price"] <= price_limit) & (data["neighbourhood"] == selected_neighborhood_2)]
st.subheader(f"Histogram of Prices Under ${price_limit}")
fig, ax = plt.subplots()
filtered_data["price"].plot(kind="hist", bins=20, ax=ax, color="orange", edgecolor="black")
ax.set_title("Price Distribution")
ax.set_xlabel("Price ($)")
ax.set_ylabel("Count")
st.pyplot(fig)

# Query 3: Highly Rated Airbnbs
st.header("3. Highly Rated Airbnbs")
min_rating = st.sidebar.slider("Set Minimum Rating", min_value=0, max_value=5, value=4, step=1)
selected_neighborhood_3 = st.sidebar.selectbox("Select Neighborhood for Ratings", ["All"] + list(data["neighbourhood"].unique()), key="rating_neighborhood")

if "review_scores_rating" in data.columns:
    if selected_neighborhood_3 == "All":
        rated_data = data[data["review_scores_rating"] >= min_rating]
    else:
        rated_data = data[(data["review_scores_rating"] >= min_rating) & (data["neighbourhood"] == selected_neighborhood_3)]
    
    st.subheader("Scatter Plot of Ratings")
    fig, ax = plt.subplots()
    ax.scatter(rated_data["price"], rated_data["review_scores_rating"], alpha=0.6, c="purple")
    ax.set_title("Ratings vs Price")
    ax.set_xlabel("Price ($)")
    ax.set_ylabel("Rating")
    st.pyplot(fig)
else:
    st.error("The dataset does not contain a 'review_scores_rating' column. Displaying price data instead.")
    
    # Fallback: Display price data in a scatter plot
    st.subheader("Scatter Plot of Prices")
    fig, ax = plt.subplots()
    ax.scatter(data["price"], alpha=0.6, c="purple")
    ax.set_title("Prices")
    ax.set_xlabel("Index")
    ax.set_ylabel("Price ($)")
    st.pyplot(fig)

# Query 4: Interactive Map
st.header("4. Interactive Map of Airbnbs")
price_filter = st.sidebar.slider("Set Price Range for Map", min_value=int(data["price"].min()), max_value=int(data["price"].max()), value=(50, 300), step=10)
rating_filter = st.sidebar.slider("Set Rating Range for Map", min_value=0, max_value=5, value=(3, 5), step=1)

if "review_scores_rating" in data.columns:
    map_data = data[(data["price"] >= price_filter[0]) & (data["price"] <= price_filter[1]) &
                    (data["review_scores_rating"] >= rating_filter[0]) & (data["review_scores_rating"] <= rating_filter[1])]
    st.map(map_data)
else:
    st.error("The dataset does not contain a 'review_scores_rating' column. Displaying price data instead.")
    
    # Fallback: Display price data on the map
    map_data = data[(data["price"] >= price_filter[0]) & (data["price"] <= price_filter[1])]
    st.map(map_data)
