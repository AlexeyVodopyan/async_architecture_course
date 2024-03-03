# stdlib
from typing import Dict, Optional

# thirdparty
from fastapi.exceptions import HTTPException as FastAPIHTTPException
from pydantic import BaseModel, RootModel
from typing_extensions import Annotated, Doc


class Error(BaseModel):
    error: str
    message: str


class ExceptionBody(RootModel):
    root: list[Error]


class HTTPException(FastAPIHTTPException):
    """Redefinition of fastapi exception to return in one format"""

    def __init__(
        self,
        status_code: Annotated[
            int,
            Doc(
                """
                    HTTP status code to send to the client.
                    """
            ),
        ],
        detail: Annotated[
            ExceptionBody,
            Doc(
                """
                    Any data to be sent to the client in the
                    `detail` key of the JSON
                    response.
                    """
            ),
        ] = None,
        headers: Annotated[
            Optional[Dict[str, str]],
            Doc(
                """
                    Any headers to send to the client in the response.
                    """
            ),
        ] = None,
    ) -> None:

        if not isinstance(detail, ExceptionBody):
            raise ValueError("detail must be an instance of ExceptionBody")

        detail = detail.model_dump()
        super().__init__(
            status_code=status_code, detail=detail, headers=headers
        )
