# Semarang Geospatial Network Analysis (Self Project)

This repository contains my self-initiated project exploring **geospatial analysis using Python** that focused on **road network analysis and public facility accessibility** in Semarang City, Indonesia.

The project utilizes **OpenStreetMap (OSM)** data, **GeoPandas**, **NetworkX**, and other Python tools to analyze:
- Road network structure
- Accessibility of settlements to public facilities (nearest schools, hospital)
- Spatial patterns and metrics (e.g., shortest paths, centrality)
- Hospitals distribution through a heatmap
---

## Project Structure
├── File .shp and .geosjon/ # Raw and cleaned geospatial data (GeoJSON, SHP)
├── File CSV/ #  Final results (CSV files)
├── File OSM/ #  OSM files that utilized on this project
├── Script Python/ # Python scripts used for processing and analysis
├── Peta HTML/ # Final results (interactive HTML maps)
├── README.md # This file

---

## Tools & Libraries Used

- QGIS
- Python 3.10+
- OSMium Tool
- GeoPandas
- Pandas
- NetworkX
- Branca
- Folium
- SciPy
- Numpy
- Matplotlib
- tqdm

---

## Key Features

- Build and analyze a graph-based road network from OSM data
- Compute **shortest paths** between settlements and POI (schools, hospitals)
- Identifying the nearest facilities from multiple origin points and calculating the shortest routes from those origin points
  to a single public facility, including information on walking distance and travel time
- Mapping the distribution of hospital facilities in Semarang City using a heatmap visualization
- Export results as:
  - CSV (access distances & times)
  - Interactive web maps (Folium)

---

## Notes

- This project was conducted independently as part of my learning journey in geospatial data science.
- The data and results are specific to Semarang City, and can be adapted to other locations with different datasets.

---

## Contact

Feel free to reach out if you want to collaborate or have questions!

> **Author**: Hilmy Azkal Adzkiya  
> **Email**: azkalhilmy.gmail.com  
> **GitHub**:(https://github.com/azkalhilmy)


