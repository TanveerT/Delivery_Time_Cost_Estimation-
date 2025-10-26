# Courier Service Coding Challenge Solution

This repository contains a Python command-line solution for the Everest Engineering Courier Service assignment. The solution estimates delivery costs and times based on input packages, offers, and vehicle information.

## Cloning git repository

1. git clone https://github.com/TanveerT/Delivery_Time_Cost_Estimation-.git
2. use branch main

## How to Run

1. Ensure Python 3 and unittest is installed.
2. Run the solution via command line: python3 main.py input.txt
3. Give the input through input.txt file

The program prints the output lines directly to the console.

To run the test case run the follwoing : python3 main.py input.txt

## How to Run Test Cases

1. To run unit test cases : python -m unittest test_units.py
2. To run integration test : python -m unittest test_integration.py

## Input Format

-   First line: `base_delivery_cost no_of_packages`
-   Next `no_of_packages` lines: `package_id weight distance offer_code`
-   Last line: `no_of_vehicles max_speed max_carriable_weight`

Examples:

## Test Cases

**Input:**

```
100 5
PKG1 50 30 OFR001
PKG2 75 125 OFFR0008
PKG3 175 100 OFR003
PKG4 110 60 OFR002
PKG5 155 95 NA
2 70 200
```

**Expected Output:**

```
PKG1 0 750 3.98
PKG2 0 1475 1.78
PKG3 0 2350 1.42
PKG4 105 1550 0.86
PKG5 0 2125 0.68
```

---
