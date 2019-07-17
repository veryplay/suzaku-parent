#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging.config
from signal import pause

import suzaku_driver.engine
import suzaku_driver.cfg.loader
from suzaku_driver.log import configure_logging

LOG_CONFIG = configure_logging()
logger = logging.getLogger(__name__)

ascii_snake = """\
=============================================================================================

    --..,_                     _,.--.
       `'.'.                .'`__ o  `;__. 
          '.'.            .'.'`  '---'`  `  Suzaku Driver Service
            '.`'--....--'`.'
              `'--....--'`

=============================================================================================
"""


def run():
    print ascii_snake
    logger.info(LOG_CONFIG)

    config_loader = suzaku_driver.cfg.loader.ConfigLoader()
    cfg = config_loader.load_config()
    logger.info(cfg)

    engine = suzaku_driver.engine.Engine(cfg)
    engine.start()
    try:
      signal.pause()
    except KeyboardInterrupt:
      # ignore
      pass
    logger.info("engine is ready to stop")


if __name__ == '__main__':
    run()
