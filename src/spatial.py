"""
MMS & LiDAR Asset Extractor - Spatial Processing
Handles computational geometry, buffer zones, and spatial querying.

Author: m_b
"""

import geopandas as gpd
import numpy as np
from shapely.geometry import Point


def create_road_buffer(gdf_trajectory: gpd.GeoDataFrame, buffer_distance_meters: float) -> gpd.GeoDataFrame:
    """
    Garante que os dados estejam no sistema projetado oficial da Alemanha (EPSG:25832)
    e gera a área de amortecimento (buffer) em metros ao redor do eixo viário.
    """
    # Se o CRS original for geográfico (latitude/longitude), converte para UTM Zona 32N (Métrico)
    if gdf_trajectory.crs and gdf_trajectory.crs.is_geographic:
        gdf_trajectory = gdf_trajectory.to_crs(epsg=25832)
    elif gdf_trajectory.crs is None:
        # Se não houver CRS definido, força o padrão do projeto
        gdf_trajectory.set_crs(epsg=25832, inplace=True)
        
    gdf_trajectory['geometry'] = gdf_trajectory.geometry.buffer(buffer_distance_meters)
    return gdf_trajectory


def filter_lidar_by_buffer(points_xyz: np.ndarray, buffer_geometry) -> np.ndarray:
    """
    Varre a nuvem de pontos 3D e gera uma máscara booleana indexada.
    Retorna True para os pontos que estão dentro da geometria 2D do buffer viário.
    """
    # Converte as coordenadas X, Y do NumPy para objetos de ponto da Shapely
    # Otimizado para checagem espacial contida
    spatial_points = [Point(x, y) for x, y in zip(points_xyz[:, 0], points_xyz[:, 1])]
    
    # Executa a validação se o polígono do buffer contém o ponto
    mask = [buffer_geometry.contains(pt) for pt in spatial_points]
    return np.array(mask)