import sys
import logging
import colorlog

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.setLevel(logging.INFO)

stdout = logging.StreamHandler(stream=sys.stdout)
logging.basicConfig(
  "%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(process)d >>> %(message)s")
logging.warning("Something bad is going to happen")


fmt = logging.Formatter(
    "%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(process)d >>> %(message)s"
)
stdout.setFormatter(fmt)
logger.addHandler(stdout)

logger.setLevel(logging.INFO)

logger.info("An info")
logger.warning("A warning")

stdout = logging.StreamHandler(stream=sys.stdout)
stdout.setLevel(logging.INFO)

logger.addHandler(stdout)