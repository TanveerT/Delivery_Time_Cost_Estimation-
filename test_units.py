"""
Unit tests for courier service components
"""
import unittest
from models import Offer, Package, Vehicle
from offer_service import OfferService
from cost_calculator import CostCalculator
from delivery_scheduler import DeliveryScheduler
from input_parser import InputParser


class TestModels(unittest.TestCase):
    """Test data models"""

    def test_offer_is_applicable(self):
        offer = Offer('TEST', 10, 50, 100, 10, 50)
        self.assertTrue(offer.is_applicable(75, 30))
        self.assertFalse(offer.is_applicable(40, 30))
        self.assertFalse(offer.is_applicable(75, 60))

    def test_package_validation(self):
        with self.assertRaises(ValueError):
            Package("", 10, 5)  # Empty ID
        with self.assertRaises(ValueError):
            Package("PKG1", -10, 5)  # Negative weight
        with self.assertRaises(ValueError):
            Package("PKG1", 10, -5)  # Negative distance

    def test_package_equality(self):
        pkg1 = Package("PKG1", 10, 5)
        pkg2 = Package("PKG1", 20, 10)
        pkg3 = Package("PKG2", 10, 5)
        self.assertEqual(pkg1, pkg2)
        self.assertNotEqual(pkg1, pkg3)

    def test_vehicle_validation(self):
        with self.assertRaises(ValueError):
            Vehicle(1, -50, 100)  # Negative speed
        with self.assertRaises(ValueError):
            Vehicle(1, 50, -100)  # Negative load


class TestOfferService(unittest.TestCase):
    """Test offer service"""

    def test_add_and_get_offer(self):
        service = OfferService()
        offer = Offer('TEST', 15, 100, 200, 50, 100)
        service.add_offer(offer)
        retrieved = service.get_offer('TEST')
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.code, 'TEST')

    def test_remove_offer(self):
        service = OfferService()
        service.remove_offer('OFR001')
        self.assertIsNone(service.get_offer('OFR001'))

    def test_default_offers_loaded(self):
        service = OfferService()
        self.assertIsNotNone(service.get_offer('OFR001'))
        self.assertIsNotNone(service.get_offer('OFR002'))
        self.assertIsNotNone(service.get_offer('OFR003'))


class TestCostCalculator(unittest.TestCase):
    """Test cost calculator"""

    def setUp(self):
        self.offer_service = OfferService()
        self.calculator = CostCalculator(100, self.offer_service)

    def test_calculate_cost_no_discount(self):
        pkg = Package('PKG1', 10, 50)
        self.calculator.calculate_cost(pkg)
        # 100 + 10*10 + 50*5 = 450
        self.assertEqual(pkg.total_cost, 450)
        self.assertEqual(pkg.discount, 0)

    def test_calculate_cost_with_valid_offer(self):
        pkg = Package('PKG1', 100, 100, 'OFR001')
        self.calculator.calculate_cost(pkg)
        # 100 + 100*10 + 100*5 = 1600
        # 10% discount = 160
        self.assertEqual(pkg.discount, 160)
        self.assertEqual(pkg.total_cost, 1440)

    def test_calculate_cost_with_invalid_offer(self):
        pkg = Package('PKG1', 10, 50, 'INVALID')
        self.calculator.calculate_cost(pkg)
        self.assertEqual(pkg.discount, 0)

    def test_calculate_cost_offer_not_applicable(self):
        pkg = Package('PKG1', 10, 50, 'OFR001')  # Too light for OFR001
        self.calculator.calculate_cost(pkg)
        self.assertEqual(pkg.discount, 0)


class TestDeliveryScheduler(unittest.TestCase):
    """Test delivery scheduler"""

    def test_schedule_with_single_vehicle(self):
        vehicles = [Vehicle(1, 70, 200)]
        scheduler = DeliveryScheduler(vehicles)
        packages = [
            Package('PKG1', 50, 30),
            Package('PKG2', 75, 125),
            Package('PKG3', 175, 100),
        ]
        scheduler.schedule_deliveries(packages)

        for pkg in packages:
            self.assertIsNotNone(pkg.delivery_time)
            self.assertGreaterEqual(pkg.delivery_time, 0)

    def test_schedule_with_multiple_vehicles(self):
        vehicles = [Vehicle(1, 70, 200), Vehicle(2, 70, 200)]
        scheduler = DeliveryScheduler(vehicles)
        packages = [
            Package('PKG1', 50, 30),
            Package('PKG2', 75, 125),
        ]
        scheduler.schedule_deliveries(packages)

        for pkg in packages:
            self.assertIsNotNone(pkg.delivery_time)

    def test_select_shipment_respects_max_load(self):
        vehicles = [Vehicle(1, 70, 100)]
        scheduler = DeliveryScheduler(vehicles)
        packages = [
            Package('PKG1', 60, 10),
            Package('PKG2', 50, 20),
            Package('PKG3', 40, 5),
        ]
        shipment, remaining = scheduler._select_shipment(packages, 100)

        total_weight = sum(pkg.weight for pkg in shipment)
        self.assertLessEqual(total_weight, 100)
        self.assertGreater(len(remaining), 0)


class TestInputParser(unittest.TestCase):
    """Test input parser"""

    def test_parse_base_info_valid(self):
        base_cost, num_packages = InputParser.parse_base_info("100 3")
        self.assertEqual(base_cost, 100)
        self.assertEqual(num_packages, 3)

    def test_parse_base_info_invalid(self):
        with self.assertRaises(ValueError):
            InputParser.parse_base_info("100")
        with self.assertRaises(ValueError):
            InputParser.parse_base_info("-100 3")
        with self.assertRaises(ValueError):
            InputParser.parse_base_info("100 -3")

    def test_parse_package_valid(self):
        pkg = InputParser.parse_package("PKG1 50 30 OFR001")
        self.assertEqual(pkg.pkg_id, "PKG1")
        self.assertEqual(pkg.weight, 50)
        self.assertEqual(pkg.distance, 30)
        self.assertEqual(pkg.offer_code, "OFR001")

    def test_parse_package_without_offer(self):
        pkg = InputParser.parse_package("PKG1 50 30 NA")
        self.assertIsNone(pkg.offer_code)

    def test_parse_package_invalid(self):
        with self.assertRaises(ValueError):
            InputParser.parse_package("PKG1 50")

    def test_parse_vehicle_info_valid(self):
        num, speed, load = InputParser.parse_vehicle_info("2 70 200")
        self.assertEqual(num, 2)
        self.assertEqual(speed, 70)
        self.assertEqual(load, 200)

    def test_parse_vehicle_info_invalid(self):
        with self.assertRaises(ValueError):
            InputParser.parse_vehicle_info("2 70")
        with self.assertRaises(ValueError):
            InputParser.parse_vehicle_info("-2 70 200")

    def test_read_input_complete(self):
        lines = [
            "100 2",
            "PKG1 50 30 OFR001",
            "PKG2 75 125 NA",
            "2 70 200"
        ]
        base_cost, packages, vehicle_info = InputParser.read_input(lines)

        self.assertEqual(base_cost, 100)
        self.assertEqual(len(packages), 2)
        self.assertIsNotNone(vehicle_info)
        self.assertEqual(vehicle_info[0], 2)

    def test_read_input_without_vehicle(self):
        lines = [
            "100 2",
            "PKG1 50 30 OFR001",
            "PKG2 75 125 NA"
        ]
        base_cost, packages, vehicle_info = InputParser.read_input(lines)

        self.assertEqual(base_cost, 100)
        self.assertEqual(len(packages), 2)
        self.assertIsNone(vehicle_info)

    def test_read_input_insufficient_lines(self):
        with self.assertRaises(ValueError):
            InputParser.read_input(["100 2"])


if __name__ == '__main__':
    unittest.main()
