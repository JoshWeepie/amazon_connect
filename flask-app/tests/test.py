import unittest
from cloudwatchlogs import Cloudwatchlogs

class TestCloudwatchlogs(unittest.TestCase):
    def test_get_all_data(self):
        self.assertRaises(TypeError, Cloudwatchlogs.get_all_data, True)
    
    def test_create_folder_list(self):
        self.assertRaises(TypeError, Cloudwatchlogs.create_folder_list, True)
    
    def test_query_logs(self):
        self.assertRaises(TypeError, Cloudwatchlogs.query_logs("2021/06/23/01/stream-KmpgRI1w3rV9R2A4W89yWg=="), True)
