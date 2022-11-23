import logging

import structlog

# Only shows INFO+ messages
structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
)

logger = structlog.get_logger("spaghetti")
