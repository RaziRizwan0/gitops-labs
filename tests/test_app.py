import unittest
from app import app
class AppTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING']=True
        self.client=app.test_client()
    def test_health(self):
        r=self.client.get('/healthz'); self.assertEqual(r.status_code,200); self.assertEqual(r.json['status'],'ok')
    def test_home(self):
        r=self.client.get('/'); self.assertEqual(r.status_code,200); self.assertIn(b'GitOps Labs',r.data)
if __name__=='__main__': unittest.main()
