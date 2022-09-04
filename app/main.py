import os
import uvicorn

from app import config


def main(env: str, debug: bool):
    os.environ["ENV"] = env
    os.environ["DEBUG"] = str(debug)
    uvicorn.run(
        app="app.server:app",
        host=config.APP_HOST or 'localhost',
        port=config.APP_PORT or '8000',
        reload=True if config.ENV != "production" else False,
        workers=1,
    )


if __name__ == "__main__":
    main()
