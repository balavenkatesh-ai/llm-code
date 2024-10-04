import unittest
from unittest.mock import MagicMock
from your_module import get_tip_controls_by_gts_id, get_all_tip_controls, TipControlRemediation  # Adjust imports accordingly

class TestTipControlRemediationMethods(unittest.TestCase):
    
    def setUp(self):
        # Mock database session
        self.mock_db_session = MagicMock()

    def test_get_tip_controls_by_gts_id_success(self):
        # Mock data to be returned by the query
        mock_tip_controls = [TipControlRemediation(id=1, tip_gts_id=1001), 
                             TipControlRemediation(id=2, tip_gts_id=1001)]
        
        # Simulate the query result
        self.mock_db_session.query().filter().all.return_value = mock_tip_controls
        
        # Call the function
        result = get_tip_controls_by_gts_id(gts_id=1001, db_session=self.mock_db_session)
        
        # Assert that the result matches the mocked data
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].tip_gts_id, 1001)

    def test_get_tip_controls_by_gts_id_no_results(self):
        # Simulate no results
        self.mock_db_session.query().filter().all.return_value = []
        
        # Call the function
        result = get_tip_controls_by_gts_id(gts_id=1002, db_session=self.mock_db_session)
        
        # Assert that the result is an empty list
        self.assertEqual(result, [])

    def test_get_tip_controls_by_gts_id_exception(self):
        # Simulate an exception being raised
        self.mock_db_session.query.side_effect = Exception("Database Error")
        
        # Call the function and handle the exception
        result = get_tip_controls_by_gts_id(gts_id=1003, db_session=self.mock_db_session)
        
        # Assert that the result is an empty list in case of exception
        self.assertEqual(result, [])

    def test_get_all_tip_controls_success(self):
        # Mock data to be returned by the query
        mock_all_tip_controls = [TipControlRemediation(id=1), 
                                 TipControlRemediation(id=2)]
        
        # Simulate the query result
        self.mock_db_session.query().all.return_value = mock_all_tip_controls
        
        # Call the function
        result = get_all_tip_controls(db_session=self.mock_db_session)
        
        # Assert that the result matches the mocked data
        self.assertEqual(len(result), 2)

    def test_get_all_tip_controls_no_results(self):
        # Simulate no results
        self.mock_db_session.query().all.return_value = []
        
        # Call the function
        result = get_all_tip_controls(db_session=self.mock_db_session)
        
        # Assert that the result is an empty list
        self.assertEqual(result, [])

    def test_get_all_tip_controls_exception(self):
        # Simulate an exception being raised
        self.mock_db_session.query.side_effect = Exception("Database Error")
        
        # Call the function and handle the exception
        result = get_all_tip_controls(db_session=self.mock_db_session)
        
        # Assert that the result is an empty list in case of exception
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()