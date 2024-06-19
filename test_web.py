import unittest
from flask import Flask
from web import app
import os
import tempfile


class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        """Test that the home page loads correctly."""
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Upload a File', result.data)

    def test_upload_file(self):
        """Test uploading a file and getting the most common word."""
        data = {
            'file': (tempfile.NamedTemporaryFile(delete=False, mode='wb+'), 'test.txt')
        }
        data['file'][0].write(b'word word test test test')
        data['file'][0].seek(0)

        result = self.app.post('/', data={
            'file': (data['file'][0], 'test.txt')
        }, content_type='multipart/form-data')

        self.assertEqual(result.status_code, 200)
        self.assertIn(b"The most common word is 'test' with 3 occurrences.", result.data)

        data['file'][0].close()
        os.remove(data['file'][0].name)

    def test_no_file_part(self):
        """Test when no file part is in the request."""
        result = self.app.post('/', data={})
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'No file part', result.data)

    def test_no_selected_file(self):
        """Test when no file is selected."""
        data = {'file': (None, '')}
        result = self.app.post('/', data=data, content_type='multipart/form-data')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'No selected file', result.data)


if __name__ == '__main__':
    unittest.main()