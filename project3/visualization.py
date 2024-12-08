import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sqlite3
from sklearn.cluster import KMeans
from opencage.geocoder import OpenCageGeocode


def geocode_address(address):
    key = "b3782a4927064024a74ba53ed25ab676"
    geocoder = OpenCageGeocode(key)
    result = geocoder.geocode(address)
    if result:
        lat = result[0]['geometry']['lat']
        lng = result[0]['geometry']['lng']
        return lat, lng
    else:
        return None, None


def create_visualizations(db_path="resources/normanpd.db"):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM incidents", conn)
    conn.close()

    # Visualization 1: Bar Chart of Incident Nature Frequency
    plt.figure(figsize=(12, 6))  # Make the plot wider to accommodate labels
    incident_counts = df['nature'].value_counts()

    # Show the top 20 incident types
    top_incidents = incident_counts.head(20)
    
    top_incidents.plot(kind='bar', color='skyblue', width=0.8)
    plt.title('Top 20 Incident Nature Frequency', fontsize=18)
    plt.xlabel('Incident Nature', fontsize=14)
    plt.ylabel('Count', fontsize=14)
    plt.xticks(rotation=45, ha="right", fontsize=12)
    plt.tight_layout()
    plt.savefig('static/bar_chart.png')
    plt.close()

    df['latitude'], df['longitude'] = zip(*df['incident_location'].apply(geocode_address))
    df = df.dropna(subset=['latitude', 'longitude'])

    # Visualization 2: Apply KMeans clustering on latitude and longitude
    kmeans = KMeans(random_state=1)
    df['cluster'] = kmeans.fit_predict(df[['latitude', 'longitude']])

    # Plot the clustering result on a map
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x=df['longitude'], y=df['latitude'], hue=df['cluster'], palette='viridis', s=100)
    plt.title('Clustering of Incidents by Geographical Location', fontsize=18)
    plt.xlabel('Longitude', fontsize=14)
    plt.ylabel('Latitude', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(title='Cluster', fontsize=12)
    plt.tight_layout()
    plt.savefig('static/clustering.png')
    plt.close()

    # Visualization 3: Histogram of Incidents by ever hour
    df['hour'] = pd.to_datetime(df['incident_time']).dt.hour

    plt.figure(figsize=(12, 6))
    sns.histplot(df['hour'], bins=24, kde=True, color='skyblue')
    plt.title('Distribution of Incidents by Hour of Day', fontsize=18)
    plt.xlabel('Hour of Day', fontsize=14)
    plt.ylabel('Incident Count', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.savefig('static/histogram.png')
    plt.close()

