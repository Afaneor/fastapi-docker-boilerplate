from pathlib import Path

ROOT_DIR = Path(__file__).parents[2]
APP_DIR = ROOT_DIR.joinpath('app')
ENV_FILE_PATH = ROOT_DIR.joinpath('.env')