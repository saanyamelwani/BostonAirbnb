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
3. How prices vary based on room type in a neighborhood.
4. Interactive map of Airbnbs by price and room type.
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

# Query 3: How Does the Price Vary Based on Room Type?
st.header("3. How Does the Price Vary Based on Room Type?")
selected_neighborhood_3 = st.sidebar.selectbox("Select Neighborhood for Room Type Analysis", ["All"] + list(data["neighbourhood"].unique()), key="room_type_neighborhood")

if selected_neighborhood_3 == "All":
    price_by_room_type = data.groupby("room_type")["price"].mean().sort_values()
else:
    price_by_room_type = data[data["neighbourhood"] == selected_neighborhood_3].groupby("room_type")["price"].mean().sort_values()

st.subheader(f"Price Variation by Room Type in {selected_neighborhood_3}")
fig, ax = plt.subplots()
price_by_room_type.plot(kind="bar", ax=ax, color="green")
ax.set_title(f"Average Price by Room Type in {selected_neighborhood_3}")
ax.set_ylabel("Average Price ($)")
st.pyplot(fig)

# Query 4: Interactive Map with Price Data
st.header("4. Interactive Map of Airbnbs by Price")
price_filter = st.sidebar.slider("Set Price Range for Map", min_value=int(data["price"].min()), max_value=int(data["price"].max()), value=(50, 300), step=10)
room_type_filter = st.sidebar.multiselect("Select Room Types for Map", data["room_type"].unique(), default=data["room_type"].unique())

# Filter data
map_data = data[(data["price"] >= price_filter[0]) & (data["price"] <= price_filter[1]) & (data["room_type"].isin(room_type_filter))]

if not map_data.empty:
    # Use PyDeck for enhanced interactivity
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/streets-v11",
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
                get_color="[200, 30, 0, 160]",  # Red with some transparency
                get_radius=200,
                pickable=True,
                tooltip=True,
            )
        ],
        tooltip={"html": "<b>Price:</b> {price}<br><b>Room Type:</b> {room_type}<br><b>Neighborhood:</b> {neighbourhood}"}
    ))
else:
    st.error("No data available for the selected filters.")
