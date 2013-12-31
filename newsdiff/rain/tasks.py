import logging

from datetime import datetime
from newsdiff.celery import app
from newsdiff.core.utils import get_file_from_url

from .models import RainRadarImage

RAIN_RADAR_IMAGE_URL = 'http://www.ims.gov.il/Ims/Pages/RadarImage.aspx'


@app.task()
def import_rain_radar_image():
    _name, image = get_file_from_url(RAIN_RADAR_IMAGE_URL)
    name = datetime.now().strftime('%H%M.gif')
    image_obj = RainRadarImage()
    image_obj.image.save(name, image)
    image_obj.save()
