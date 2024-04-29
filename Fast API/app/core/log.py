import logging

from typing import TextIO

import structlog
from rich.console import Console
from rich.traceback import Traceback
from structlog.processors import CallsiteParameter

from app.core.configs import settings

time_stamper = structlog.processors.TimeStamper(fmt="iso", key="time")


structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        time_stamper,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
        structlog.processors.CallsiteParameterAdder(
            parameters=[
                CallsiteParameter.FILENAME,
                # CallsiteParameter.FUNC_NAME,
                CallsiteParameter.LINENO,
            ],
        ),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)


def extract_from_record(
    _: structlog.types.WrappedLogger, __: str, event_dict: structlog.types.EventDict
) -> structlog.types.EventDict:
    """
    Extract thread and process names and add them to the event dict.

    Parameters
    ----------
    _ : structlog.types.WrappedLogger
        The first parameter is a structlog WrappedLogger object.
    __ : str
        The second parameter is a string. It is not used in this function.
    event_dict : structlog.types.EventDict
        The third parameter is a structlog EventDict object. It contains the event data.

    Returns
    -------
    structlog.types.EventDict
        The function returns the modified EventDict object with added thread and process names.

    Notes
    -----
    This function is used to extract thread and process names from the event record and add them to the event dict.
    """
    record = event_dict["_record"]
    event_dict["logger"] = record.name
    event_dict["filename"] = record.filename
    event_dict["lineno"] = record.lineno
    event_dict["thread_name"] = record.threadName
    event_dict["process_name"] = record.processName
    return event_dict


def custom_exception_formatter(sio: TextIO, exc_info: structlog.types.ExcInfo) -> None:
    sio.write("\n")
    Console(
        file=sio,
        color_system="truecolor" if settings.COLORIZE_LOGS else None,
    ).print(Traceback.from_exception(*exc_info, show_locals=True))


pre_chain: list[structlog.types.Processor] = [
    structlog.stdlib.add_log_level,
    structlog.stdlib.ExtraAdder(),
    time_stamper,
]
formatter_processors: list[structlog.types.Processor] = [
    extract_from_record,
    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
]
if settings.LOG_JSON:
    formatter_processors.extend(
        [
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ]
    )
else:
    formatter_processors.append(
        structlog.dev.ConsoleRenderer(
            colors=settings.COLORIZE_LOGS,
            exception_formatter=custom_exception_formatter,
        )
    )
formatter = structlog.stdlib.ProcessorFormatter(
    # These run ONLY on `logging` entries that do NOT originate within structlog.
    foreign_pre_chain=pre_chain,
    # These run on ALL entries after the pre_chain is done.
    processors=formatter_processors,
)

handler = logging.StreamHandler()
# Use OUR `ProcessorFormatter` to format all `logging` entries.
handler.setFormatter(formatter)
logging.basicConfig(handlers=[handler], level=settings.LOG_LEVEL)
for name in logging.root.manager.loggerDict.keys():
    logging.getLogger(name).handlers.clear()
logging.getLogger("uvicorn").propagate = True
logger = structlog.get_logger()
logger.debug("Logger created")
