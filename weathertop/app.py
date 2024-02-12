from os import environ
import logging
from weathertop import imageProcessor


# Logging
_loglevel = environ.get('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
	level=_loglevel,
	format='[%(asctime)s] [%(levelname)s]: %(message)s'
)
logging.getLogger(name=__name__)


def main(config):
	logging.debug(config)
	logging.info(f"Weathertop (c) Brian Shef 2024")
	processor = imageProcessor.Processor(
		f"{config.source}/map3.jpg",
		logging.getLogger("imageProcessor")
	)
	processor.showImg(title=f"Original {processor.src}")
	processor.getShapes()
	logging.info("Done")