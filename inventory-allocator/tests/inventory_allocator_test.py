import pytest

from src.inventory_allocator import InventoryAllocator


@pytest.fixture(scope="module")
def inventory_allocator():
    """
    Return the same instance of InventoryAllocator (per module)
    """
    return InventoryAllocator()

def assert_allocation(order, inventory_distribution, expected_shipments, inventory_allocator):
    """
    Return true if the inventory allocation returns expected shipments
    """
    assert(
        inventory_allocator.allocate_shipments(order, inventory_distribution)
    ) == expected_shipments


@pytest.mark.parametrize(
    "order, inventory_distribution", 
    [
        (None, [{'name': 'X', 'inventory': {'apple': 5}}]),
        ({}, [{'name': 'X', 'inventory': {'apple': 5}}]),
        ([], [{'name': 'X', 'inventory': {'apple': 5}}]),
        ({'apple': 1}, None),
        ({'apple': 1}, {}),
        ({'apple': 1}, []),
        (None, None),
        ({}, []),
    ]
)
def test_allocate_shipments_empty_input(order, inventory_distribution, inventory_allocator):
    """
    Order should not be fullfilled if either order or inventory distribution is empty
    """
    assert_allocation(
        order=order,
        inventory_distribution=inventory_distribution,
        expected_shipments=[],
        inventory_allocator=inventory_allocator,
    )


def test_allocate_shipments_one_warehouse_one_shipment(inventory_allocator):
    """
    Order should be fullfilled when the one warehouse in the inventory distribution
    has all the items in the order  
    """
    assert_allocation(
        order={'apple': 1, 'banana': 1},
        inventory_distribution=[
            {'name': 'owd', 'inventory': {'apple': 1, 'banana': 2, 'orange': 3}}
        ],
        expected_shipments=[{'owd': {'apple': 1, 'banana': 1}}],
        inventory_allocator=inventory_allocator,
    )


def test_allocate_shipments_multiple_warehouses_one_shipment(inventory_allocator):
    """
    Order should be fullfilled by the first warehouse entirely since it has all the items
    """
    assert_allocation(
        order={'apple': 1, 'banana': 1},
        inventory_distribution=[
            {'name': 'owd', 'inventory': {'apple': 1, 'banana': 2}},
            {'name': 'dw', 'inventory': {'apple': 1}},
        ],
        expected_shipments=[{'owd': {'apple': 1, 'banana': 1}}],
        inventory_allocator=inventory_allocator,
    )


def test_allocate_shipments_multiple_warehouses_multiple_shipment(inventory_allocator):
    """
    Order should be fullfilled by multiple shipments when one warehouse doesn't have
    all the items in the order
    """
    assert_allocation(
        order={'apple': 2, 'banana': 1},
        inventory_distribution=[
            {'name': 'owd', 'inventory': {'apple': 1, 'banana': 2}},
            {'name': 'dw', 'inventory': {'apple': 1}},
        ],
        expected_shipments=[{'owd': {'apple': 1, 'banana': 1}}, {'dw':{'apple': 1}}],
        inventory_allocator=inventory_allocator,
    )


def test_allocate_shipments_one_warehouse_no_shipment(inventory_allocator):
    """
    If the inventory distribution (one warehouse) is does not have enough items
    to fullfill the order, no shipments/allocations should be made
    """
    assert_allocation(
        order={'apple': 100, 'banana': 2},
        inventory_distribution=[
            {'name': 'owd', 'inventory': {'apple': 1, 'banana': 2}},
        ],
        expected_shipments=[],
        inventory_allocator=inventory_allocator,
    )

    assert_allocation(
        order={'apple': 100, 'banana': 2},
        inventory_distribution=[
            {'name': 'owd', 'inventory': {'apple': 0, 'banana': 2}},
        ],
        expected_shipments=[],
        inventory_allocator=inventory_allocator,
    )

    assert_allocation(
        order={'apple': 100, 'banana': 2},
        inventory_distribution=[
            {'name': 'owd', 'inventory': {'apple': -123, 'banana': 2}},
        ],
        expected_shipments=[],
        inventory_allocator=inventory_allocator,
    )


def test_allocate_shipments_multiple_warehouses_no_shipment(inventory_allocator):
    """
    If the inventory distribution (multiple warehouses) is does not have enough items
    to fullfill the order, no shipments/allocations should be made
    """
    assert_allocation(
        order={'apple': 100, 'banana': 2},
        inventory_distribution=[
            {'name': 'owd', 'inventory': {'apple': 1, 'banana': 2}},
            {'name': 'dw', 'inventory': {'apple': 1, 'banana': 20}},
        ],
        expected_shipments=[],
        inventory_allocator=inventory_allocator,
    )
