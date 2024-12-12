"""
Name: Saanya Melwani
CS230: Section 3
Data: Boston Airbnb Data
URL: https://github.com/saanyamelwani/BostonAirbnb.git
Description: 
This program analyzes Boston Airbnb data to assist people planning to visit Boston. 
It provides insights into rental trends, pricing, and availability, helping users find the best options for their stay. 
The program leverages Python's capabilities to create interactive visualizations and perform geographic and statistical analysis, 
making it a useful tool for travelers seeking the perfect Airbnb in Boston.
"""
import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
@st.cache_data
def load_data():
    try:
        listings = pd.read_csv("listings.csv")
        return listings
    except FileNotFoundError:
        st.error("The dataset file was not found. Please upload it and try again.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return pd.DataFrame()

data = load_data()

# Helper function: Plot bar chart
def plot_bar_chart(data, x_col, y_col, title, palette="Blues_d"):
    fig, ax = plt.subplots()
    sns.barplot(x=data[x_col], y=data[y_col], ax=ax, palette=palette)
    ax.set_title(title)
    ax.set_xticklabels(data[x_col], rotation=45, ha="right")
    st.pyplot(fig)

# Helper function: Compute summary statistics
def compute_summary(data, column):
    mean = data[column].mean()
    median = data[column].median()
    return mean, median

# Title and introduction
st.title("Boston Airbnb Data Explorer")
st.markdown("""
This application helps you explore Airbnb data in Boston. You can analyze:
1. Average listing prices by neighborhood.
2. Apartments under a specific price in a selected neighborhood.
3. How prices vary based on room type in a neighborhood.
4. Interactive map of Airbnbs by price and room type.
""")

# Sidebar for user inputs
st.sidebar.title("Filters")

# Query 1: Average Listing Price by Neighborhood
st.header("1. Average Listing Price by Neighborhood")
selected_neighborhood = st.sidebar.selectbox("Select Neighborhood", ["All"] + list(data["neighbourhood"].unique()))
if selected_neighborhood == "All":
    avg_prices = data.groupby("neighbourhood")["price"].mean().sort_values().reset_index()
    st.subheader("Bar Chart of Average Prices")
    plot_bar_chart(avg_prices, "neighbourhood", "price", "Average Prices by Neighborhood")
else:
    avg_price = data[data["neighbourhood"] == selected_neighborhood]["price"].mean()
    st.write(f"Average price in {selected_neighborhood}: ${avg_price:.2f}")

# Query 2: Airbnbs Under $300 a Night
st.header("2. Find Airbnbs Under $300 a Night")
selected_neighborhood_2 = st.sidebar.selectbox("Select Neighborhood for Price Filter", ["All"] + list(data["neighbourhood"].unique()), key="price_neighborhood")

if selected_neighborhood_2 == "All":
    filtered_data = data[data["price"] <= 300]
else:
    filtered_data = data[(data["price"] <= 300) & (data["neighbourhood"] == selected_neighborhood_2)]
st.subheader("Histogram of Prices Under $300")
fig, ax = plt.subplots()
sns.histplot(filtered_data["price"], bins=20, ax=ax, color="orange", kde=True, edgecolor="black")
ax.set_title("Price Distribution")
ax.set_xlabel("Price ($)")
ax.set_ylabel("Count")
st.pyplot(fig)

# Query 3: How Does the Price Vary Based on Room Type?
st.header("3. How Does the Price Vary Based on Room Type?")
selected_neighborhood_3 = st.sidebar.selectbox("Select Neighborhood for Room Type Analysis", ["All"] + list(data["neighbourhood"].unique()), key="room_type_neighborhood")

if selected_neighborhood_3 == "All":
    price_by_room_type = data.groupby("room_type")["price"].mean().sort_values().reset_index()
else:
    price_by_room_type = data[data["neighbourhood"] == selected_neighborhood_3].groupby("room_type")["price"].mean().sort_values().reset_index()

st.subheader(f"Price Variation by Room Type in {selected_neighborhood_3}")
plot_bar_chart(price_by_room_type, "room_type", "price", f"Average Price by Room Type in {selected_neighborhood_3}", palette="Greens_d")

# Query 4: Interactive Map with Price Data
st.header("4. Interactive Map of Airbnbs by Price")
price_filter = st.sidebar.slider("Set Price Range for Map", min_value=int(data["price"].min()), max_value=int(data["price"].max()), value=(50, 300), step=10)
room_type_filter = st.sidebar.multiselect("Select Room Types for Map", data["room_type"].unique(), default=data["room_type"].unique())

# Filter data
map_data = data[(data["price"] >= price_filter[0]) & (data["price"] <= price_filter[1]) & (data["room_type"].isin(room_type_filter))]

if not map_data.empty:
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.ViewState(
            latitude=map_data["latitude"].mean(),
            longitude=map_data["longitude"].mean(),
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=map_data,
                get_position=["longitude", "latitude"],
                get_color="[200, price * 2, 50, 160]",  # Dynamic color based on price
                get_radius=200,
                pickable=True,
            )
        ],
        tooltip={"html": "<b>Price:</b> ${price}<br><b>Room Type:</b> {room_type}"}
    ))
else:
    st.error("No data available for the selected filters.")

# Compute and display summary statistics for price
mean_price, median_price = compute_summary(data, "price")
st.write(f"Mean Price: ${mean_price:.2f}, Median Price: ${median_price:.2f}")
