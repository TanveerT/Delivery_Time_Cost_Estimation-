"""
Service for calculating delivery costs
"""
from typing import List
from models import Package
from offer_service import OfferService


class CostCalculator:
    """Calculates delivery costs with offer discounts"""

    WEIGHT_COST_MULTIPLIER = 10
    DISTANCE_COST_MULTIPLIER = 5

    def __init__(self, base_delivery_cost: float, offer_service: OfferService):
        if base_delivery_cost < 0:
            raise ValueError("Base delivery cost cannot be negative")
        self.base_delivery_cost = base_delivery_cost
        self.offer_service = offer_service

    def calculate_cost(self, package: Package) -> None:
        """Calculate cost and discount for a single package"""
        delivery_cost = (self.base_delivery_cost + 
                        package.weight * self.WEIGHT_COST_MULTIPLIER + 
                        package.distance * self.DISTANCE_COST_MULTIPLIER)

        discount = 0
        if package.offer_code:
            offer = self.offer_service.get_offer(package.offer_code)
            if offer and offer.is_applicable(package.weight, package.distance):
                discount = delivery_cost * (offer.discount_percentage / 100)

        package.discount = round(discount)
        package.total_cost = round(delivery_cost - discount)

    def calculate_costs_batch(self, packages: List[Package]) -> None:
        """Calculate costs for multiple packages"""
        for package in packages:
            self.calculate_cost(package)
