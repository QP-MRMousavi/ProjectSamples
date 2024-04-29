import socket
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from authlib.integrations.httpx_client import AsyncOAuth2Client
from tortoise import Tortoise
from tortoise.backends.base.client import BaseDBAsyncClient

from app.core.configs import settings
from app.core.log import logger


async def check_db(db: BaseDBAsyncClient) -> bool:
    """
    Checks if the database connection is successful.

    Args:
    db (BaseDBAsyncClient): The database connection object.

    Returns:
    bool: Returns True if the database connection is successful, False otherwise.

    Raises:
    RuntimeError: If the database connection fails.

    This function attempts to execute a simple SQL query ("SELECT 1") on the provided database connection.
    If the query is successful, the function returns True, indicating that the database connection is successful.
    If the query fails due to a socket.gaierror exception, the function logs the exception using the logger and returns False,
    indicating that the database connection failed.
    """
    try:
        await db.execute_script("SELECT 1")
        return True
    except socket.gaierror:
        logger.exception("Connection failure")
        return False


async def start_db() -> BaseDBAsyncClient:
    """
    Initializes the database connection and returns the connection object.

    Returns:
    BaseDBAsyncClient: The initialized database connection object.

    Raises:
    RuntimeError: If the database connection fails.

    This function initializes the database connection using Tortoise.init() with the provided TORTOISE_CONFIG.
    It then retrieves the default database connection using Tortoise.get_connection("default").
    If the database connection is successful, the function returns the connection object.
    If the database connection fails, the function raises a RuntimeError with the message "Database connection failure".
    """
    logger.debug(settings.TORTOISE_CONFIG)
    await Tortoise.init(config=settings.TORTOISE_CONFIG)

    db = Tortoise.get_connection("default")
    if not await check_db(db):
        raise RuntimeError("Database connection failure")
    return db


async def stop_db(db: BaseDBAsyncClient) -> None:
    """
    Closes all the database connections.

    Args:
    db (BaseDBAsyncClient): The database connection object.

    Returns:
    None: This function does not return any value.

    Raises:
    None: This function does not raise any exceptions.

    This function closes all the database connections using Tortoise.close_connections().
    It is called in the finally block of the context_db() asynchronous context manager to ensure that the database connections are closed even if an exception occurs during the execution of the code within the context.

    """
    await Tortoise.close_connections()


@asynccontextmanager
async def context_db() -> AsyncGenerator[BaseDBAsyncClient, None]:
    """
    Asynchronous context manager for database connections.

    Yields:
    BaseDBAsyncClient: The initialized database connection object.

    This function initializes the database connection using the `start_db` function and yields the connection object.
    It ensures that the database connections are closed even if an exception occurs during the execution of the code within the context by calling the `stop_db` function in the finally block.
    """
 
    db = await start_db()
    try:
        yield db
    finally:
        await stop_db(db)
