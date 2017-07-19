import logging

logger = logging.getLogger(__name__)
_root_handler = None


def setup_logging(enabled=True, level=logging.DEBUG):
    global _root_handler
    if _root_handler is not None and _root_handler in logging.root.handler:
        logging.root.removeHandler(_root_handler)
    logging.root.setLevel(logging.NOTSET)
    _root_handler = logging.StreamHandler() if enabled else logging.NullHandler()
    _root_handler.addFilter(logging.Filter("pget"))
    _root_handler.setLevel(level)

    logging.root.addHandler(_root_handler)
