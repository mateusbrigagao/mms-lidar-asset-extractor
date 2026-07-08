# MMS & LiDAR Asset Extractor

An automated Python-based geospatial data fusion pipeline designed to filter and extract LiDAR point clouds using Mobile Mapping System (MMS) trajectories. This project targets infrastructure monitoring and HD mapping workflows, leveraging German standard Projected Coordinate Systems (such as ETRS89 / UTM Zone 32N - EPSG:25832).

# Project Overview

Processing massive 3D point clouds alongside vector trajectories is a computationally expensive bottleneck in autonomous driving and smart city infrastructure. This pipeline automates the spatial querying process by using 2D vector boundaries (MMS buffers) to spatially index, slice, and filter heavy 3D LiDAR data (`.las`/`.laz`), isolating only the relevant corridor assets (roads, traffic signs, overhead lines) and discarding regional noise.

# Key Features
* **High-Performance Spatial Querying:** Modular architecture built for handling dense point clouds without memory exhaustion.
* **MMS Trajectory Buffering:** Vector manipulation using `GeoPandas` and `Shapely` for dynamic corridor definition.
* **CRS-Aware Data Fusion:** Built-in validation for Coordinate Reference Systems, natively optimized for Germany's EPSG:25832.
* **Optimized I/O Ops:** Uses `laspy` with `lazrs` C-bindings for blazing-fast decompression of `.laz` files.

---

# Repository Structure

```text
mms-lidar-asset-extractor/
│
├── data/
│   ├── raw/          # Raw input data (LAZ and GeoJSON - Git ignored)
│   └── processed/    # Filtered outputs (Cleaned LAZ files)
│
├── src/
│   ├── __init__.py
│   ├── io_utils.py   # High-efficiency file I/O operations
│   ├── spatial.py    # Buffer generation and spatial filtering logic
│   └── pipeline.py   # Main orchestrator script
│
├── requirements.txt  # Python package dependencies
└── README.md         # Documentation