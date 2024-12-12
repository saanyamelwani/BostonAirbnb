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
    ax.scatter(range(len(data)), data["price"], alpha=0.6, c="purple")
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
