from django.test import TestCase

from .models import RainRadarImage
from .tasks import import_rain_radar_image


class RainRadarTestCase(TestCase):
    def setUp(self):
        pass

    def test_import_rain_radar_image(self):
        import_rain_radar_image()
        image = RainRadarImage.objects.all()[0]
        self.assertTrue(image.created)
        self.assertTrue(image.image.url)
