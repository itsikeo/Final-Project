# FinalProjectInventory.py
Ike Okafor
2032177
import csv
from datetime import datetime

class InventoryItem:
    def __init__(self, item_id, manufacturer, item_type, price, service_date, damaged):
        self.item_id = item_id
        self.manufacturer = manufacturer
        self.item_type = item_type
        self.price = price
        self.service_date = service_date
        self.damaged = damaged

class InventoryManager:
    def __init__(self):
        self.items = {}

    def load_data(self, manufacturer_file, price_file, service_date_file):
        with open(manufacturer_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                item_id, manufacturer, item_type, *damaged = row
                damaged = damaged[0] if damaged else ""
                self.items[item_id] = InventoryItem(item_id, manufacturer, item_type, None, None, damaged)

        with open(price_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                item_id, price = row
                if item_id in self.items:
                    self.items[item_id].price = float(price)

        with open(service_date_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                item_id, service_date = row
                if item_id in self.items:
                    self.items[item_id].service_date = datetime.strptime(service_date, '%m/%d/%Y')

        # Debugging: Print loaded data
        for item_id, item in self.items.items():
            print(f"Loaded item: {item_id}, {item.manufacturer}, {item.item_type}, {item.price}, {item.service_date}, {item.damaged}")

    def generate_full_inventory(self, output_file):
        sorted_items = sorted(self.items.values(), key=lambda x: x.manufacturer)
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            for item in sorted_items:
                writer.writerow([item.item_id, item.manufacturer, item.item_type, item.price, item.service_date.strftime('%m/%d/%Y'), item.damaged])

    def generate_item_type_inventory(self):
        item_types = {}
        for item in self.items.values():
            if item.item_type not in item_types:
                item_types[item.item_type] = []
            item_types[item.item_type].append(item)

        for item_type, items in item_types.items():
            sorted_items = sorted(items, key=lambda x: x.item_id)
            with open(f'{item_type}Inventory.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                for item in sorted_items:
                    writer.writerow([item.item_id, item.manufacturer, item.price, item.service_date.strftime('%m/%d/%Y'), item.damaged])

    def generate_past_service_date_inventory(self, output_file):
        today = datetime.today()
        past_service_items = [item for item in self.items.values() if item.service_date < today]
        sorted_items = sorted(past_service_items, key=lambda x: x.service_date)
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            for item in sorted_items:
                writer.writerow([item.item_id, item.manufacturer, item.item_type, item.price, item.service_date.strftime('%m/%d/%Y'), item.damaged])

    def generate_damaged_inventory(self, output_file):
        damaged_items = [item for item in self.items.values() if item.damaged]
        sorted_items = sorted(damaged_items, key=lambda x: x.price, reverse=True)
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            for item in sorted_items:
                writer.writerow([item.item_id, item.manufacturer, item.item_type, item.price, item.service_date.strftime('%m/%d/%Y')])

# Usage
inventory_manager = InventoryManager()
inventory_manager.load_data("C://Users//cedri//Downloads//order-6867889//ManufacturerList.csv", "C://Users//cedri//Downloads//order-6867889//PriceList.csv", "C://Users//cedri//Downloads//order-6867889//ServiceDatesList.csv")
inventory_manager.generate_full_inventory("C://Users//cedri//Downloads//order-6867889//FullInventory.csv")
inventory_manager.generate_item_type_inventory()
inventory_manager.generate_past_service_date_inventory("C://Users//cedri//Downloads//order-6867889//PastServiceDateInventory.csv")
inventory_manager.generate_damaged_inventory("C://Users//cedri//Downloads//order-6867889//DamagedInventory.csv")