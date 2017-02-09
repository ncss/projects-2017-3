import back_end.Imaging as img
import unittest

class TestImageMethods(unittest.TestCase):
    def test_image1(self):
        x = img.open_image(open('correct1.jpg', 'rb').read())
        self.assertFalse(isinstance(x, type(None)))
        self.assertEqual(x[1], 'jpeg')

    def test_image2(self):
        x = img.open_image(open('correct1.jpg', 'rb').read())[0]
        x.save("out1.jpg")
        x = img.to_icon(x)
        x.save("out2.jpg")
        self.assertFalse(False)


if __name__ == "__main__":
    unittest.main()