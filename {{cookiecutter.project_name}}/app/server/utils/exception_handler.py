from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
import os

from pydantic_i18n import PydanticI18n, BabelLoader

from config.constants import APP_DIR

class CustomBabelLoader(BabelLoader):  # FIXME move to separate file

    def __init__(self, translations_directory: str, domain: str = "messages"):
        try:
            from babel import Locale
            from babel.support import Translations
        except ImportError as e:  # pragma: no cover
            raise ImportError(
                "babel not installed, you cannot use this loader.\n"
                "To install, run: pip install babel"
            ) from e

        self.translations = {}

        for dir_name in [d for d in os.listdir(translations_directory)
                         if os.path.isdir(
                os.path.join(translations_directory, d)
            )
                         ]:
            locale = Locale.parse(dir_name)
            self.translations[str(locale)] = Translations.load(
                translations_directory,
                [locale],
                domain=domain,
            )

loader = CustomBabelLoader(os.path.join(APP_DIR, 'locales'))
tr = PydanticI18n(
    loader,
    default_locale='en',
)

async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    try:
        locale = request.state.babel.locale  # will work with BabelMiddleware
    except AttributeError:
        locale = "en"
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": tr.translate(exc.errors(), locale)},
    )
