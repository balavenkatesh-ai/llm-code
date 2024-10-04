import unittest
from unittest.mock import Mock, patch
import pandas as pd
from tip_controls_table import save_to_tipcontrol_table, TipControlRemediation

class TestTipControlTable(unittest.TestCase):
    def setUp(self):
        self.mock_engine = Mock()
        self.mock_session = Mock()
        self.mock_engine.return_value = self.mock_session

    @patch('tip_controls_table.Session')
    def test_save_to_tipcontrol_table_success(self, mock_session):
        mock_session.return_value = self.mock_session
        
        # Create a sample DataFrame
        data = {'column1': [1, 2, 3], 'column2': ['a', 'b', 'c']}
        df = pd.DataFrame(data)
        
        tip_gts_id = "test_id"
        
        # Call the function
        save_to_tipcontrol_table(df, tip_gts_id)
        
        # Assert that the session methods were called
        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_called_once()

    @patch('tip_controls_table.Session')
    def test_save_to_tipcontrol_table_exception(self, mock_session):
        mock_session.return_value = self.mock_session
        self.mock_session.commit.side_effect = Exception("Database error")
        
        # Create a sample DataFrame
        data = {'column1': [1, 2, 3], 'column2': ['a', 'b', 'c']}
        df = pd.DataFrame(data)
        
        tip_gts_id = "test_id"
        
        # Call the function and check if it handles the exception
        with self.assertRaises(Exception):
            save_to_tipcontrol_table(df, tip_gts_id)

    @patch('tip_controls_table.Session')
    def test_save_to_tipcontrol_table_correct_data(self, mock_session):
        mock_session.return_value = self.mock_session
        
        # Create a sample DataFrame
        data = {'column1': [1, 2, 3], 'column2': ['a', 'b', 'c']}
        df = pd.DataFrame(data)
        
        tip_gts_id = "test_id"
        
        # Call the function
        save_to_tipcontrol_table(df, tip_gts_id)
        
        # Assert that TipControlRemediation was called with correct data
        self.mock_session.add.assert_called_once()
        called_object = self.mock_session.add.call_args[0][0]
        self.assertIsInstance(called_object, TipControlRemediation)
        self.assertEqual(called_object.tip_gts_id, tip_gts_id)
        self.assertEqual(called_object.tip_version, 1)
        self.assertEqual(called_object.tip_remediation_data, df.to_dict(orient="records"))

if __name__ == '__main__':
    unittest.main()