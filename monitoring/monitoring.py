import asyncio
import json
import os
import shutil
import sqlite3
import time


from datetime import datetime
from pathlib import Path
from typing import Iterator


from loguru import logger

version = "0.2"


def _adapt_datetime_iso(val):
    return val.isoformat()


def _convert_datetime(val):
    return datetime.fromisoformat(val)


sqlite3.register_adapter(datetime, _adapt_datetime_iso)
sqlite3.register_converter("datetime", _convert_datetime)

logger.add(
    "Logfile.log",
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="10 MB",
    compression="zip",
)

SETTINGS = {}


def load_settings():
    with open(
        file="C:\\Projects\\SPFS_BASE\\monitoring\\settings.json",
        mode="r",
        encoding="utf-8",
    ) as sett_file:
        SETTINGS.update(json.load(sett_file))


def _copy_file(path_file: Path, new_path: Path, log: bool = True) -> None:
    while True:
        try:
            shutil.copy(path_file, new_path)
            break
        except Exception as error:
            logger.error(error)
            time.sleep(5)
    if log:
        logger.info("Файл {} скопирован в {}".format(path_file, new_path))


def _move_file(path_file: Path, new_path: Path) -> None:
    _copy_file(path_file, new_path, log=False)
    while True:
        try:
            path_file.unlink()
            break
        except Exception as error:
            logger.error(error)
            time.sleep(5)
    logger.info("Файл {} перемещен в {}".format(path_file, new_path))


def _iter_dir(path: Path) -> Iterator[Path]:
    while True:
        try:
            paths = path.iterdir()
            result = filter(Path.is_file, paths)
            return result
        except OSError:
            logger.error(
                "Ошибка OSError, при нахождении пути к {}".format(path)
            )
        except Exception as error:
            logger.error("Ошибка при нахождении пути к {}".format(path))
            logger.error(error)
        time.sleep(5)


def start() -> None:
    pass


async def monitoring() -> None:
    while True:
        start()
        await asyncio.sleep(SETTINGS["tics"])


if __name__ == "__main__":
    logger.debug("Запуск скрипта версии: {}".format(version))
    load_settings()
    while True:
        try:
            asyncio.run(monitoring())
        except Exception as error:
            logger.error(error)
            time.sleep(10)
