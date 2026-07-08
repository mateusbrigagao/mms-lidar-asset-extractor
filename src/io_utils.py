"""
MMS & LiDAR Asset Extractor - I/O Utilities
Handles high-efficiency reading and writing for vector and point cloud data.

Author: m_b
"""

import geopandas as gpd
import laspy
import numpy as np


def read_vector_trajectory(file_path: str) -> gpd.GeoDataFrame:
    """
    Carrega o arquivo vetorial que contém a trajetória ou eixo da pista (MMS).
    Suporta formatos comuns como GeoJSON, Shapefile ou GPKG.
    """
    try:
        gdf = gpd.read_file(file_path)
        if gdf.empty:
            raise ValueError(f"O arquivo {file_path} está vazio.")
        return gdf
    except Exception as e:
        raise IOError(f"Erro ao ler o arquivo vetorial: {e}")


def read_lidar_xyz(file_path: str) -> np.ndarray:
    """
    Abre uma nuvem de pontos LAS/LAZ de forma eficiente e extrai as 
    coordenadas X, Y, Z como um array do NumPy para processamento rápido.
    """
    try:
        with laspy.open(file_path) as fh:
            las = fh.read()
            # Agrupa as coordenadas X, Y, Z em uma matriz Nx3
            xyz = np.vstack((las.x, las.y, las.z)).T
            return xyz
    except Exception as e:
        raise IOError(f"Erro ao ler a nuvem de pontos LiDAR: {e}")


def write_filtered_lidar(output_path: str, original_file_path: str, mask: np.ndarray) -> None:
    """
    Salva uma nova nuvem de pontos contendo apenas os dados filtrados.
    Usa o arquivo original como referência para herdar rigorosamente todos os 
    metadados, cabeçalhos (headers) e o Sistema de Referência de Coordenadas (CRS).
    """
    try:
        # Reabre o arquivo original para extrair a estrutura de pontos correta
        with laspy.open(original_file_path) as fh:
            las = fh.read()
        
        # Cria um novo objeto LAS mantendo o mesmo cabeçalho
        filtered_las = laspy.LasData(las.header)
        # Aplica a máscara booleana para filtrar os pontos
        filtered_las.points = las.points[mask]
        
        # Grava o resultado final no disco (com compressão automática se for .laz)
        filtered_las.write(output_path)
    except Exception as e:
        raise IOError(f"Erro ao gravar a nuvem de pontos filtrada: {e}")