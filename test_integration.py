"""
Integration tests for courier service
"""
import unittest
from models import Package, Vehicle
from offer_service import OfferService
from cost_calculator import CostCalculator
from delivery_scheduler import DeliveryScheduler
from input_parser import InputParser


class TestEndToEndIntegration(unittest.TestCase):
    """End-to-end integration tests"""

    def test_cost_calculation_flow(self):
        """Test complete cost calculation flow"""
        lines = [
            "100 3",
            "PKG1 5 5 OFR001",
            "PKG2 15 5 OFR002",
            "PKG3 10 100 OFR003"
        ]

        base_cost, packages, _ = InputParser.read_input(lines)
        offer_service = OfferService()
        calculator = CostCalculator(base_cost, offer_service)
        calculator.calculate_costs_batch(packages)

        # PKG1: 100 + 5*10 + 5*5 = 175 (no discount - doesn't meet weight criteria)
        self.assertEqual(packages[0].discount, 0)
        self.assertEqual(packages[0].total_cost, 175)

        # PKG2: 100 + 15*10 + 5*5 = 275 (no discount)
        self.assertEqual(packages[1].discount, 0)
        self.assertEqual(packages[1].total_cost, 275)

        # PKG3: 100 + 10*10 + 100*5 = 700, 5% discount = 35
        self.assertEqual(packages[2].discount, 35)
        self.assertEqual(packages[2].total_cost, 665)

    def test_delivery_time_calculation_flow(self):
        """Test complete delivery time calculation flow"""
        lines = [
            "100 5",
            "PKG1 50 30 OFR001",
            "PKG2 75 125 OFFR0008",
            "PKG3 175 100 OFR003",
            "PKG4 110 60 OFR002",
            "PKG5 155 95 NA",
            "2 70 200"
        ]

        base_cost, packages, vehicle_info = InputParser.read_input(lines)

        # Calculate costs
        offer_service = OfferService()
        calculator = CostCalculator(base_cost, offer_service)
        calculator.calculate_costs_batch(packages)

        # Calculate delivery times
        num_vehicles, max_speed, max_load = vehicle_info
        vehicles = [Vehicle(i + 1, max_speed, max_load) for i in range(num_vehicles)]
        scheduler = DeliveryScheduler(vehicles)
        scheduler.schedule_deliveries(packages)

        # Verify all packages have delivery times
        for pkg in packages:
            self.assertIsNotNone(pkg.delivery_time)
            self.assertGreater(pkg.delivery_time, 0)

        # Verify costs are calculated
        for pkg in packages:
            self.assertGreaterEqual(pkg.total_cost, 0)

    def test_empty_package_list(self):
        """Test handling of empty package list"""
        vehicles = [Vehicle(1, 70, 200)]
        scheduler = DeliveryScheduler(vehicles)
        scheduler.schedule_deliveries([])  # Should not crash

    def test_single_package_single_vehicle(self):
        """Test simplest case"""
        lines = [
            "100 1",
            "PKG1 50 30 NA",
            "1 70 200"
        ]

        base_cost, packages, vehicle_info = InputParser.read_input(lines)
        offer_service = OfferService()
        calculator = CostCalculator(base_cost, offer_service)
        calculator.calculate_costs_batch(packages)

        num_vehicles, max_speed, max_load = vehicle_info
        vehicles = [Vehicle(i + 1, max_speed, max_load) for i in range(num_vehicles)]
        scheduler = DeliveryScheduler(vehicles)
        scheduler.schedule_deliveries(packages)

        self.assertIsNotNone(packages[0].delivery_time)
        expected_time = round(30 / 70, 2)
        self.assertEqual(packages[0].delivery_time, expected_time)


if __name__ == '__main__':
    unittest.main()
