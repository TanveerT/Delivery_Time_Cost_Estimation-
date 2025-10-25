import sys
from typing import List

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
    
def main():
  """ Main application logic"""
  
  print(sys.argv)
  try:
    if len(sys.argv) > 1:
      filename = sys.argv[1]
      lines = read_input_from_file(filename)
    else:
      raise FileNotFoundError(f"Input file not specified")
    
    
    
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