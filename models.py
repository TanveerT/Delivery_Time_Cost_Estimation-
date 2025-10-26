



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