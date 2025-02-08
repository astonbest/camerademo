import unittest
from src.camera.camera_manager import CameraManager

class TestCameraManager(unittest.TestCase):

    def setUp(self):
        self.camera_manager = CameraManager()

    def test_initialize_camera(self):
        self.assertTrue(self.camera_manager.initialize_camera())

    def test_start_preview(self):
        self.camera_manager.initialize_camera()
        self.assertTrue(self.camera_manager.start_preview())

    def test_take_photo(self):
        self.camera_manager.initialize_camera()
        self.camera_manager.start_preview()
        photo = self.camera_manager.take_photo()
        self.assertIsNotNone(photo)

    def tearDown(self):
        self.camera_manager.release_camera()

if __name__ == '__main__':
    unittest.main()