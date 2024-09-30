import json
import logging
import os
from typing import Any

logger = logging.getLogger()


class Resource:
    @staticmethod
    def load_json(path: str) -> Any:
        base_path = os.path.join(os.getcwd(), "src", "resources")
        absolute_path = os.path.join(base_path, path)
        if not os.path.isfile(absolute_path):
            raise FileNotFoundError(
                f"The file {absolute_path} does not exist."
            )

        with open(absolute_path, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError as error:
                logger.error(f"Error: {error}")
                raise ValueError(
                    f"Error decoding JSON from file {absolute_path}: {error}"
                )
            except Exception as error:
                logger.error(f"Error: {error}")
