import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns

# Load flight data (Replace 'flights_data.csv' with the actual dataset)
df = pd.read_csv("/content/Sample_JFK_Flight_Data.csv")

# Inspect dataset structure
print(df.head())

# Ensure necessary columns are present (modify if needed)
required_columns = ["origin", "destination", "airline", "flight_number", "departure_time", "date", "domestic_international"]
assert all(col in df.columns for col in required_columns), "Missing necessary columns!"

# Filter data for JFK
jfk_flights = df[df["origin"] == "JFK"]

### 1. Mapping Direct Routes from JFK ###
def plot_route_map(df, airport):
    G = nx.DiGraph()
    for _, row in df.iterrows():
        G.add_edge(row["origin"], row["destination"])

    plt.figure(figsize=(12, 6))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10, font_weight="bold")
    plt.title(f"Direct Flight Routes from {airport}")
    plt.show()

plot_route_map(jfk_flights, "JFK")

### 2. Top 5 Destinations by Flight Volume ###
top_destinations = jfk_flights["destination"].value_counts().head(5)
print("Top 5 destinations from JFK:\n", top_destinations)

plt.figure(figsize=(8, 4))
sns.barplot(x=top_destinations.index, y=top_destinations.values, palette="Blues_r")
plt.title("Top 5 Destinations from JFK by Flight Volume")
plt.xlabel("Destination Airport")
plt.ylabel("Number of Flights")
plt.show()

### 3. Flight Volume by Time of Day ###
# Convert departure_time to datetime if not already
jfk_flights["departure_time"] = pd.to_datetime(jfk_flights["departure_time"])
jfk_flights["hour"] = jfk_flights["departure_time"].dt.hour

hourly_flight_count = jfk_flights["hour"].value_counts().sort_index()
plt.figure(figsize=(10, 5))
sns.lineplot(x=hourly_flight_count.index, y=hourly_flight_count.values, marker="o")
plt.title("Flight Volume by Time of Day (JFK)")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Flights")
plt.xticks(range(0, 24))
plt.grid()
plt.show()

### 4. Domestic vs International Flights ###
dom_int_counts = jfk_flights["domestic_international"].value_counts(normalize=True) * 100
print("Domestic vs. International flight distribution:\n", dom_int_counts)

plt.figure(figsize=(6, 6))
plt.pie(dom_int_counts, labels=dom_int_counts.index, autopct="%.1f%%", colors=["lightblue", "lightcoral"], startangle=140)
plt.title("Domestic vs International Flights from JFK")
plt.show()

### 5. Identifying Key Hub Airports ###
hub_airports = jfk_flights["destination"].value_counts().head(10)
print("Major hubs connected to JFK:\n", hub_airports)

plt.figure(figsize=(10, 5))
sns.barplot(x=hub_airports.index, y=hub_airports.values, palette="coolwarm")
plt.title("Top 10 Hub Airports Connected to JFK")
plt.xlabel("Airport")
plt.ylabel("Number of Flights")
plt.xticks(rotation=45)
plt.show()

### 6. Most Frequent Airlines from JFK ###
top_airlines = jfk_flights["airline"].value_counts().head(5)
print("Most frequent airlines operating from JFK:\n", top_airlines)

plt.figure(figsize=(8, 4))
sns.barplot(x=top_airlines.index, y=top_airlines.values, palette="magma")
plt.title("Top 5 Airlines Operating from JFK")
plt.xlabel("Airline")
plt.ylabel("Number of Flights")
plt.show()
