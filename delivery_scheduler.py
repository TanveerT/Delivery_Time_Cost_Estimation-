"""
Service for scheduling package deliveries
"""
import heapq
from typing import List, Tuple
from models import Package, Vehicle


class DeliveryScheduler:
    """Schedules package deliveries across available vehicles"""

    def __init__(self, vehicles: List[Vehicle]):
        if not vehicles:
            raise ValueError("At least one vehicle is required")
        self.vehicles = vehicles

    def schedule_deliveries(self, packages: List[Package]) -> None:
        """Assign delivery times to all packages"""
        if not packages:
            return

        packages_to_deliver = list(packages)
        # Priority queue: (available_time, vehicle_index, vehicle)
        vehicle_queue = [(0.0, idx, vehicle) 
                        for idx, vehicle in enumerate(self.vehicles)]
        heapq.heapify(vehicle_queue)

        while packages_to_deliver:
            available_time, _, vehicle = heapq.heappop(vehicle_queue)

            # Select packages for this trip
            shipment, packages_to_deliver = self._select_shipment(
                packages_to_deliver, vehicle.max_load
            )

            if not shipment:
                # No packages fit, try again with next vehicle
                heapq.heappush(vehicle_queue, (available_time + 0.1, _, vehicle))
                continue

            # Assign delivery times
            for package in shipment:
                package.delivery_time = round(
                    available_time + (package.distance / vehicle.max_speed), 2
                )

            # Calculate when vehicle returns
            max_trip_time = max(pkg.distance / vehicle.max_speed 
                              for pkg in shipment)
            return_time = available_time + (max_trip_time * 2)

            heapq.heappush(vehicle_queue, (return_time, _, vehicle))

    def _select_shipment(self, packages: List[Package], 
                        max_load: float) -> Tuple[List[Package], List[Package]]:
        """
        Select packages for a single shipment.
        Strategy: Prioritize heavier packages first, then closer destinations.
        """
        # Sort by weight (descending), then distance (ascending)
        candidates = sorted(packages, key=lambda p: (-p.weight, p.distance))

        shipment = []
        current_load = 0.0

        for package in candidates:
            if current_load + package.weight <= max_load:
                shipment.append(package)
                current_load += package.weight

        remaining = [pkg for pkg in packages if pkg not in shipment]
        return shipment, remaining
