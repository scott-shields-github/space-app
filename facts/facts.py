from re import sub
from ruamel.yaml import YAML
from typing import List
from pathlib import Path
import random
import json
DATA_DIR = "./facts/data"

SUBJECT_FILES = {
    "jwst": f"{DATA_DIR}/jwst.facts.yaml"
}

def _load_yaml_file(file_path: str):
    """Loads a YAML file

    Args:
        file_path: The file path to read.

    Returns:
        The content of the loaded file.
    """
    try:
        yaml = YAML(typ="safe")
        yaml.preserve_quotes = True  # type: ignore
        return yaml.load(Path(file_path))

    except Exception as e:
        raise

def load_subject_data(subject: str):
    data_file = SUBJECT_FILES.get(subject, "jwst")
    return _load_yaml_file(data_file)

def random_fact(subject: str):
    subject_data = load_subject_data(subject)
    return random.choice(subject_data["facts"])

def fact_block(subject:str, title: str, details: str):
    blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{title}",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": f"{details}",
                    "emoji": True
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "plain_text",
                        "text": f":book: Fact from subject: {subject}",
                        "emoji": True
                    }
                ]
            }
        ]
    return json.dumps(blocks)