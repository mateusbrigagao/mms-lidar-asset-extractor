"""
MMS & LiDAR Asset Extractor - Test Data Generator
Generates realistic mock spatial data in EPSG:25832 for pipeline validation.

Author: m_b
"""

import os
import geopandas as gpd
import laspy
import numpy as np
from shapely.geometry import LineString


def generate_data():
    print("[m_b] Generating realistic test datasets...")
    os.makedirs("data/raw", exist_ok=True)

    # 1. Criar Trajetória MMS (Uma linha reta simulando uma rua de 100 metros)
    # Coordenadas UTM na Alemanha (Zona 32N) começam na casa dos 32X,XXX e 5,XXX,XXX
    x_coords = np.linspace(350000, 350100, 10)
    y_coords = np.linspace(5600000, 5600000, 10)  # Linha reta horizontal
    
    line = LineString(list(zip(x_coords, y_coords)))
    gdf = gpd.GeoDataFrame(geometry=[line], crs="EPSG:25832")
    gdf.to_file("data/raw/trajectory.geojson", driver="GeoJSON")
    print("[m_b] Success: Generated data/raw/trajectory.geojson")

    # 2. Criar Nuvem de Pontos LiDAR (LAS)
    # Vamos gerar 5.000 pontos aleatórios ao redor da rodovia
    num_points = 5000
    header = laspy.LasHeader(point_format=3, version="1.2")
    
    # Pontos espalhados: X entre 349990 e 350110, Y entre 5599980 e 5600020
    header.x_scale, header.y_scale, header.z_scale = 0.01, 0.01, 0.01
    
    las = laspy.LasData(header)
    las.x = np.random.uniform(349990, 350110, num_points)
    las.y = np.random.uniform(5599980, 5600020, num_points)
    las.z = np.random.uniform(50, 65, num_points)  # Altitude simulada (Z)

    las.write("data/raw/cloud_raw.las")
    print("[m_b] Success: Generated data/raw/cloud_raw.las")


if __name__ == "__main__":
    generate_data()