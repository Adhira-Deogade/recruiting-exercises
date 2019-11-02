from typing import List
from typing import Dict

from src.custom_typing import ItemQuantities
from src.custom_typing import Shipment
from src.custom_typing import Warehouse

class InventoryAllocator:
    def allocate_shipments(self, order: ItemQuantities={},  inventory_distribution: List[Warehouse]=[]) -> List[Shipment]:
        """Compute the best way an order can be shipped with an inventory distribution.

        Keyword Args:
            order -- A dict of items, with the key being the item's name and 
                the value being it's quantity. For example: {'apple': 1, 'banana': 2}
            inventory_distribution -- A list of warehouses, pre-sorted based on cost.
                A warehouse is a dict with the key being the name of an attribute and the value 
                being the attribute's value. For example: [{'name': 'owd', 'inventory': {'apple': 1}}]
        
        Returns:
            A list of shipments that need to be made in order to fullfill the order, with the least cost.
            An item's shipment will be split accross warehouses only if that's the only way to fullfill the item.
            
            No shipments will be allocated if any item's quantity is larger than the total available inventory
            for the item.
        """
        # Base case: empty order or inventory distribution
        if any(input == empty for empty in [None, {}, []] for input in [order, inventory_distribution]):
            return []

        # Use a copy of the order, since we don't want to modify the original order
        remaining_order = order.copy()

        # Start with an empty list of shipments; return a built list at the end
        shipments: List[Shipment] = []

        # total_remaining_quantity will be used to verify that the order has been completely fullfilled
        # (if we don't have enough items in our inventory, the order must not be fullfilled)
        total_remaining_quantity = sum(remaining_order.values())

        # Go through each warehouse inventory sequentially, and try to 
        # fullfill each item in the order as fully as possible
        for warehouse in inventory_distribution: 

            # If the order is fullfilled, stop iterating through inventory_distribution
            if total_remaining_quantity < 1: 
                break

            # warehouse_item_quantities represents which items and what quantities of them 
            # will be allocated from the warehouse to fullfil the order
            warehouse_item_quantities: ItemQuantities = {}

            warehouse_name: str = warehouse['name']
            inventory: ItemQuantities = warehouse['inventory']

            # If the warehouse has an item requested in the order, allocate it
            for item_name in inventory:
                inventory_quantity: int = inventory[item_name]
                if inventory_quantity <= 0:
                    continue
                if item_name in remaining_order and remaining_order[item_name] > 0:
                    allocated_quantity = min(remaining_order[item_name], inventory_quantity)
                    warehouse_item_quantities[item_name] = allocated_quantity
                    remaining_order[item_name] -= allocated_quantity
                    total_remaining_quantity -= allocated_quantity

            shipments.append({warehouse_name: warehouse_item_quantities})

        # Fullfill the order only if all items in the order have been fullfilled
        return shipments if total_remaining_quantity == 0 else []

