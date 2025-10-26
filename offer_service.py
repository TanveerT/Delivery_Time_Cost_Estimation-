"""
Service for managing discount offers
"""
from typing import Dict, Optional
from models import Offer


class OfferService:
    """Manages discount offers in an extensible way"""

    def __init__(self):
        self._offers: Dict[str, Offer] = {}
        self._load_default_offers()

    def _load_default_offers(self):
        """Load default offers"""
        default_offers = [
            Offer('OFR001', 10, 70, 200, 0, 199),
            Offer('OFR002', 7, 100, 250, 50, 150),
            Offer('OFR003', 5, 10, 150, 50, 250),
        ]
        for offer in default_offers:
            self.add_offer(offer)

    def add_offer(self, offer: Offer):
        """Add a new offer to the system"""
        if not isinstance(offer, Offer):
            raise ValueError("Invalid offer object")
        self._offers[offer.code] = offer

    def get_offer(self, code: str) -> Optional[Offer]:
        """Retrieve an offer by code"""
        return self._offers.get(code)

    def remove_offer(self, code: str):
        """Remove an offer from the system"""
        if code in self._offers:
            del self._offers[code]

    def get_all_offers(self) -> Dict[str, Offer]:
        """Get all available offers"""
        return self._offers.copy()
