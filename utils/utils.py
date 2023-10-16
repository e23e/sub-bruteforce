import logging
import sys



def eprint(content: str):
    print(content, file=sys.stderr)

def get_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
        )
    logger = logging.getLogger("bruteforce")
    return logger
