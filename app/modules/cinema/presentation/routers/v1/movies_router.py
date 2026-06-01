from typing import Annotated

from fastapi import APIRouter, Query

router = APIRouter(prefix="/v1/movies")


# ==================


@router.get("/")
async def get_movies(genre: Annotated[str, Query()], search: Annotated[str, Query()]):
    pass
