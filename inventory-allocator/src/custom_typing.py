from typing import Dict
from typing import List
from typing import Union

ItemQuantities = Dict[str, int]  # {'apple': 10, 'banana': 20, 'orange': 30}
Warehouse = Dict[str, Union[str, ItemQuantities]] # {'name': 'LAX', 'inventory': {'apple': 10, 'banana': 20}}
Shipment = Dict[str, ItemQuantities] # {'LAX': {'apple': 1, 'banana': 1}}