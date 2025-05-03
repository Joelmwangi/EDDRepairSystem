import csv
from models.supplier import Supplier

class SupplierService:
    def __init__(self):
        self.suppliers = []

    def add_supplier(self, supplier):
        self.suppliers.append(supplier)

    def save_suppliers_to_csv(self, filename="suppliers.csv"):
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Location"])
            for s in self.suppliers:
                writer.writerow([s.name, s.location])

    def load_suppliers_from_csv(self, filename="suppliers.csv"):
        try:
            with open(filename, mode="r") as file:
                reader = csv.DictReader(file)
                return [row for row in reader]
        except FileNotFoundError:
            return []

