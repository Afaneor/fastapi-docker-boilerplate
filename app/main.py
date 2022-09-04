import uvicorn

import config


def main():
    uvicorn.run(
        app="server.server:app",
        host=config.APP_HOST or '0.0.0.0',
        port=config.APP_PORT or '8000',
        reload=True if config.ENV != "production" else False,
        workers=1,
    )


if __name__ == "__main__":
    main()
