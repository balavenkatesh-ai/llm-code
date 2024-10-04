import unittest
from unittest.mock import MagicMock
from your_module import get_tip_inventory_by_ci_id, TipInventory  # adjust imports accordingly

class TestTipInventoryMethods(unittest.TestCase):
    def setUp(self):
        # Mock database session
        self.mock_db_session = MagicMock()

    def test_get_tip_inventory_by_ci_id_success(self):
        # Mock data to be returned by the query
        mock_inventory = [TipInventory(id=1, ci_id=1001, status='active'), 
                          TipInventory(id=2, ci_id=1001, status='active')]
        
        # Simulate the query result
        self.mock_db_session.query().filter().order_by().all.return_value = mock_inventory
        
        # Call the function
        result = get_tip_inventory_by_ci_id(ci_id=1001, status='active', db_session=self.mock_db_session)
        
        # Assert that the result matches the mocked data
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].ci_id, 1001)

    def test_get_tip_inventory_by_ci_id_no_results(self):
        # Simulate no results
        self.mock_db_session.query().filter().order_by().all.return_value = []
        
        # Call the function
        result = get_tip_inventory_by_ci_id(ci_id=1002, status='inactive', db_session=self.mock_db_session)
        
        # Assert that the result is an empty list
        self.assertEqual(result, [])

    def test_get_tip_inventory_by_ci_id_exception(self):
        # Simulate an exception being raised
        self.mock_db_session.query.side_effect = Exception("Database Error")
        
        # Call the function and handle the exception
        result = get_tip_inventory_by_ci_id(ci_id=1003, status='active', db_session=self.mock_db_session)
        
        # Assert that the result is an empty list in case of exception
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()