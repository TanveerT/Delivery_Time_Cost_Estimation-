
from typing import List, Tuple, Optional
from models import Package

class InputParser:
  """Parses and validates input data"""
   
  @staticmethod
  def parse_base_info(line: str) -> Tuple[float, int]:
      """Parse base delivery cost and number of packages"""
      try:
          parts = line.strip().split()
          if len(parts) != 2:
              raise ValueError("Base info must contain exactly 2 values")

          base_cost = float(parts[0])
          num_packages = int(parts[1])

          if base_cost < 0:
              raise ValueError("Base delivery cost cannot be negative")
          if num_packages <= 0:
              raise ValueError("Number of packages must be positive")

          return base_cost, num_packages
      except (ValueError, IndexError) as e:
          raise ValueError(f"Invalid base info format: {e}")

  @staticmethod
  def parse_package(line: str) -> Package:
      """Parse a single package line"""
      try:
          parts = line.strip().split()
          if len(parts) < 3:
              raise ValueError("Package must have at least 3 fields")

          pkg_id = parts[0]
          weight = float(parts[1])
          distance = float(parts[2])
          offer_code = parts[3] if len(parts) > 3 and parts[3] != 'NA' else None

          return Package(pkg_id, weight, distance, offer_code)
      except (ValueError, IndexError) as e:
          raise ValueError(f"Invalid package format: {e}")

  @staticmethod
  def parse_vehicle_info(line: str) -> Tuple[int, float, float]:
      """Parse vehicle configuration"""
      try:
          parts = line.strip().split()
          if len(parts) != 3:
              raise ValueError("Vehicle info must contain exactly 3 values")

          num_vehicles = int(parts[0])
          max_speed = float(parts[1])
          max_load = float(parts[2])

          if num_vehicles <= 0:
              raise ValueError("Number of vehicles must be positive")
          if max_speed <= 0:
              raise ValueError("Vehicle speed must be positive")
          if max_load <= 0:
              raise ValueError("Vehicle max load must be positive")

          return num_vehicles, max_speed, max_load
      except (ValueError, IndexError) as e:
          raise ValueError(f"Invalid vehicle info format: {e}")

  @staticmethod
  def read_input(lines: List[str]) -> Tuple[float, List[Package], Optional[Tuple[int, float, float]]]:
      """Read and parse all input data"""
      if len(lines) < 2:
          raise ValueError("Insufficient input: need at least 2 lines")

      # Parse base info
      base_cost, num_packages = InputParser.parse_base_info(lines[0])

      if len(lines) < num_packages + 1:
          raise ValueError(f"Expected {num_packages} package lines, got {len(lines) - 1}")

      # Parse packages
      packages = []
      for i in range(1, num_packages + 1):
          package = InputParser.parse_package(lines[i])
          packages.append(package)

      # Parse vehicle info if present
      vehicle_info = None
      if len(lines) > num_packages + 1:
          vehicle_info = InputParser.parse_vehicle_info(lines[num_packages + 1])

      return base_cost, packages, vehicle_info