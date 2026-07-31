import os
import random
import pandas as pd


# -------------------------------
# Create Folder if Not Exists
# -------------------------------

def create_folder(folder_name):
    """
    Creates a folder if it does not exist.
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


# -------------------------------
# Generate Random Color
# -------------------------------

def random_color():
    """
    Returns a random RGB color.
    """
    return (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )


# -------------------------------
# Vehicle Statistics
# -------------------------------

def vehicle_summary(results):

    summary = {
        "Car": results.get("Car", 0),
        "Motorcycle": results.get("Motorcycle", 0),
        "Bus": results.get("Bus", 0),
        "Truck": results.get("Truck", 0),
        "Total": results.get("Total", 0)
    }

    return summary


# -------------------------------
# Save Statistics as CSV
# -------------------------------

def save_csv(results, filename="vehicle_statistics.csv"):

    df = pd.DataFrame({
        "Vehicle": [
            "Car",
            "Motorcycle",
            "Bus",
            "Truck",
            "Total"
        ],
        "Count": [
            results.get("Car", 0),
            results.get("Motorcycle", 0),
            results.get("Bus", 0),
            results.get("Truck", 0),
            results.get("Total", 0)
        ]
    })

    df.to_csv(filename, index=False)

    return filename


# -------------------------------
# Print Summary
# -------------------------------

def print_summary(results):

    print("\n========= Vehicle Statistics =========")

    print(f"Cars         : {results.get('Car',0)}")
    print(f"Motorcycles  : {results.get('Motorcycle',0)}")
    print(f"Buses        : {results.get('Bus',0)}")
    print(f"Trucks       : {results.get('Truck',0)}")
    print("--------------------------------------")
    print(f"Total        : {results.get('Total',0)}")

    print("======================================")