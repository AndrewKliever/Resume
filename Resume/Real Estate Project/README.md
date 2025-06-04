# Project-3-Group-6-DataV
Andrew Kliever
Ken Priest
Jesus Mata
Yvette Saul


Real Estate Trends Visualization Project
Overview
This project focuses on monitoring real estate trends across the United States by leveraging web scraping, data visualization, and geospatial mapping. It is designed to analyze monthly real estate data, providing insights through interactive visualizations such as heat maps, choropleth maps, and a bubble map. The project serves as a dynamic tool to assist users in understanding market trends at both state and national levels.

Features:
Web Scraping: Real estate data is collected from online sources.

SQL Database Integration: Data is stored and managed in a SQL database for efficiency and scalability.

Visualizations:
Choropleth Map: Displays state-by-state trends using color gradients.
Heat Map: Highlights specific regions with higher activity or values.
Bubble Map: Displays state-by-state average trends using a bubble reference for average price lists, average price per square foot, and average dayas on market.

Geocoding: Coordinates are processed during data collection to streamline mapping workflows.

Tools and Technologies:
Programming Languages: Python, JavaScript
Libraries and Frameworks:
Python: BeautifulSoup (web scraping), Pandas, Folium, Geopy
Note: please be sure to 'pip install folium' and 'pip install geopy' prior to running map
JavaScript: Leaflet, D3.js
Database: SQL for data storage and management

Purpose
The project aims to provide real-time insights into real estate market trends, making it a valuable tool for analysts, realtors, and stakeholders in the housing market.

Data Acquisition Challenges
Our initial plan involved sourcing real estate data from Zillow.com, given its comprehensive listings and detailed metrics. However, Zillow employs advanced anti-scraping measures that restrict the volume of data that can be retrieved in a single session. This presented a significant challenge to our project.

To continue using Zillow as our data source, we explored several options:

1. Circumventing Anti-Scraping Measures – While technically feasible, this approach posed potential legal and ethical concerns.
2. Incremental Scraping – Conducting multiple scraping sessions to accumulate sufficient data, though time-intensive and logistically impractical.
3. Purchasing the Zillow API – A straightforward solution, but the associated cost was beyond the scope of our project’s budget.

After careful consideration, we determined that none of these options were viable. Consequently, we pivoted to alternative data sources and adjusted the focus of our project. This shift allowed us to continue without compromising the project’s integrity while staying within our resource constraints.
