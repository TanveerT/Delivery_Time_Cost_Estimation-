



class Package:
    """Represents a delivery package"""

    def __init__(self, pkg_id: str, weight: float, distance: float, offer_code: str = None):
        if not pkg_id or not isinstance(pkg_id, str):
            raise ValueError("Package ID must be a non-empty string")
        if weight <= 0:
            raise ValueError("Package weight must be positive")
        if distance < 0:
            raise ValueError("Package distance cannot be negative")

        self.pkg_id = pkg_id
        self.weight = weight
        self.distance = distance
        self.offer_code = offer_code
        self.discount = 0
        self.total_cost = 0
        self.delivery_time = None

    def __eq__(self, other):
        if isinstance(other, Package):
            return self.pkg_id == other.pkg_id
        return False

    def __hash__(self):
        return hash(self.pkg_id)

    def __repr__(self):
        return f"Package(id={self.pkg_id}, weight={self.weight}, distance={self.distance})"



class Offer:
    """Represents a discount offer with specific criteria"""

    def __init__(self, code: str, discount_percentage: float, 
                 min_weight: float, max_weight: float, 
                 min_distance: float, max_distance: float):
        self.code = code
        self.discount_percentage = discount_percentage
        self.min_weight = min_weight
        self.max_weight = max_weight
        self.min_distance = min_distance
        self.max_distance = max_distance

    def is_applicable(self, weight: float, distance: float) -> bool:
        """Check if offer is applicable for given weight and distance"""
        return (self.min_weight <= weight <= self.max_weight and
                self.min_distance <= distance <= self.max_distance)
        

class Vehicle:
    """Represents a delivery vehicle"""

    def __init__(self, vehicle_id: int, max_speed: float, max_load: float):
        if max_speed <= 0:
            raise ValueError("Vehicle speed must be positive")
        if max_load <= 0:
            raise ValueError("Vehicle max load must be positive")

        self.vehicle_id = vehicle_id
        self.max_speed = max_speed
        self.max_load = max_load
        self.available_at = 0.0

    def __repr__(self):
        return f"Vehicle(id={self.vehicle_id}, speed={self.max_speed}, load={self.max_load})"