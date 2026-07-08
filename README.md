# LiDAR & MMS Spatial Filter

An automated Python-based geospatial data fusion pipeline designed to filter and extract LiDAR point clouds using Mobile Mapping System (MMS) trajectories. This project targets infrastructure monitoring and HD mapping workflows, leveraging German standard Projected Coordinate Systems (ETRS89 / UTM Zone 32N - EPSG:25832).

The core processing engine operates under a strict **"Solve et Coagula"** paradigm: dissolving massive, unstructured raw point clouds into standalone spatial matrices, and coagulating them back into refined, noise-free geospatial assets.

## Project Overview

Processing massive 3D point clouds alongside vector trajectories is a computationally expensive bottleneck. This pipeline automates the spatial querying process by using 2D vector boundaries (MMS buffers) to spatially index, slice, and filter heavy 3D LiDAR data (`.las`/`.laz`), isolating only the relevant corridor assets and discarding regional environmental noise.

Built with a **Left-Hand Path design philosophy**, the architecture deliberately bypasses bloated desktop GIS software wrappers, interacting directly with low-level geometry and raw binary point streams for absolute execution control.

## Key Features

* **High-Performance Spatial Querying:** Modular architecture built for handling dense point clouds without memory exhaustion.
* **MMS Trajectory Buffering:** Vector manipulation using `GeoPandas` and `Shapely` for dynamic, metric-accurate corridor definition.
* **CRS-Aware Data Fusion:** Built-in validation for Coordinate Reference Systems, natively optimized for Germany's EPSG:25832.
* **Optimized I/O Ops:** Uses `laspy` with `lazrs` C-bindings for fast decompression of spatial data.

---

## Repository Structure

```text
mms-lidar-asset-extractor/
│
├── data/
│   ├── raw/          # Raw input data (LAZ and GeoJSON - Git ignored)
│   └── processed/    # Filtered outputs (Cleaned LAS/LAZ files)
│
├── notebooks/
│   └── validation_analysis.ipynb  # Interactive visual validation
│
├── src/
│   ├── __init__.py
│   ├── io_utils.py   # High-efficiency file I/O operations
│   ├── spatial.py    # Buffer generation and spatial filtering logic
│   ├── pipeline.py   # Main orchestrator script
│   └── generate_test_data.py # Local mock data generator
│
├── requirements.txt  # Python package dependencies
└── README.md         # Documentation


Visual Validation

The repository includes a local mock data generator to verify the containment logic without downloading heavy external datasets.

Execution metrics from the validation test:

Raw Point Cloud: 5,000 points

Filtered Output: 2,428 points

Discarded Noise: 2,572 points (51.44%)

The spatial slicing results can be inspected via the interactive notebook located in notebooks/validation_analysis.ipynb.


Quickstart

1. Setup Environment
DOS
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

2. Run Pipeline Test
DOS
python src/generate_test_data.py
python src/pipeline.py data/raw/trajectory.geojson data/raw/cloud_raw.las data/processed/cloud_filtered.las 10.0

Developed by m_b 