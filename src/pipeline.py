"""
MMS & LiDAR Asset Extractor - Main Pipeline Orchestrator
Fuses vector trajectories and 3D point clouds to extract highway corridor assets.

Author: m_b
"""

import os
import sys
from io_utils import read_vector_trajectory, read_lidar_xyz, write_filtered_lidar
from spatial import create_road_buffer, filter_lidar_by_buffer


def run_pipeline(trajectory_path: str, lidar_path: str, output_path: str, buffer_size: float = 5.0) -> None:
    """
    Executa o fluxo de ponta a ponta: Ingestão -> Bufferização -> Filtragem -> Exportação.
    """
    print("[m_b] Starting MMS-LiDAR Asset Extractor Pipeline...")
    
    # 1. Ingestão do vetor de trajetória
    print(f"[m_b] Loading MMS trajectory from: {os.path.basename(trajectory_path)}")
    gdf_trajectory = read_vector_trajectory(trajectory_path)
    
    # 2. Geração da área de busca (Corredor da rodovia)
    print(f"[m_b] Generating {buffer_size}m road corridor buffer (EPSG:25832)...")
    gdf_buffer = create_road_buffer(gdf_trajectory, buffer_distance_meters=buffer_size)
    # Extrai a geometria do polígono unificado (dissolvido) para a busca espacial
    buffer_geometry = gdf_buffer.unary_union
    
    # 3. Ingestão da nuvem de pontos LiDAR
    print(f"[m_b] Loading LiDAR point cloud from: {os.path.basename(lidar_path)}")
    points_xyz = read_lidar_xyz(lidar_path)
    print(f"[m_b] Total points loaded: {len(points_xyz):,}")
    
    # 4. Processamento e Filtragem Espacial
    print("[m_b] Spatial querying in progress... Filtering points outside corridor.")
    spatial_mask = filter_lidar_by_buffer(points_xyz, buffer_geometry)
    
    # 5. Exportação dos dados filtrados
    print(f"[m_b] Exporting filtered point cloud to: {output_path}")
    write_filtered_lidar(output_path, lidar_path, spatial_mask)
    
    print("[m_b] Pipeline execution completed successfully!")


if __name__ == "__main__":
    # Exemplo de execução via terminal passando os argumentos necessários
    # Formato: python pipeline.py <trajetoria> <nuvem_bruta> <nuvem_saida>
    if len(sys.argv) < 4:
        print("\n[m_b] Usage error. Expected format:")
        print("python pipeline.py <trajectory_path> <lidar_raw_path> <output_processed_path> [buffer_size_meters]")
        sys.exit(1)
        
    input_vector = sys.argv[1]
    input_lidar = sys.argv[2]
    output_lidar = sys.argv[3]
    
    # Se o usuário não passar o tamanho do buffer, o padrão será 5.0 metros
    size = float(sys.argv[4]) if len(sys.argv) > 4 else 5.0
    
    run_pipeline(input_vector, input_lidar, output_lidar, buffer_size=size)