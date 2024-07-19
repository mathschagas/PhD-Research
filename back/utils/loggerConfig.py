import logging
import colorlog

def get_configured_logger():
    # Configure colorlog for colored logs
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s[%(levelname)s] [%(asctime)s] %(message)s',
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'white',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red,bg_white',
        },
        datefmt='%Y/%m/%d %H:%M:%S'  # Format of %(asctime)s
    ))
    logger = colorlog.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger