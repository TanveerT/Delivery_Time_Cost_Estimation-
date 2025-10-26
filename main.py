import sys
from typing import List
from input_parser import InputParser
from offer_service import OfferService
from cost_calculator import CostCalculator
from delivery_scheduler import DeliveryScheduler
from models import Vehicle

def read_input_from_file(filename: str) -> List[str]:
  """Read input from a file"""
  try:
      with open(filename, 'r') as f:
          lines = [line.strip() for line in f if line.strip()]
      return lines
  except FileNotFoundError:
      raise FileNotFoundError(f"Input file not found: {filename}")
  except IOError as e:
      raise IOError(f"Error reading file: {e}")
    
def print_results(packages: List, include_delivery_time: bool = False):
    """Print formatted results"""
    for pkg in packages:
        if include_delivery_time and pkg.delivery_time is not None:
            print(f"{pkg.pkg_id} {pkg.discount} {pkg.total_cost} {pkg.delivery_time}")
        else:
            print(f"{pkg.pkg_id} {pkg.discount} {pkg.total_cost}") 
def main():
  """ Main application logic"""
  

  try:
    if len(sys.argv) > 1:
      filename = sys.argv[1]
      lines = read_input_from_file(filename)
    else:
      raise FileNotFoundError(f"Input file not specified")
    
    
    # Parse base info
    # Parse input
    base_cost, packages, vehicle_info = InputParser.read_input(lines)
    # Initialize services
    offer_service = OfferService()
    cost_calculator = CostCalculator(base_cost, offer_service)
     # Calculate costs
    cost_calculator.calculate_costs_batch(packages)
    
    # Calculate delivery times if vehicle info provided
    include_delivery_time = False
    if vehicle_info:
        num_vehicles, max_speed, max_load = vehicle_info
        vehicles = [Vehicle(i + 1, max_speed, max_load) 
                    for i in range(num_vehicles)]
        scheduler = DeliveryScheduler(vehicles)
        scheduler.schedule_deliveries(packages)
        include_delivery_time = True
    
    # Print results
    print_results(packages, include_delivery_time)
    
  except ValueError as e:
        print(f"Input validation error: {e}", file=sys.stderr)
        sys.exit(1)
  except FileNotFoundError as e:
        print(f"File error: {e}", file=sys.stderr)
        sys.exit(1)
  except Exception as e:
    print(f"Unexpected error: {e}", file=sys.stderr)
    sys.exit(1)
    
    pass
  
if __name__ == "__main__":
    main()