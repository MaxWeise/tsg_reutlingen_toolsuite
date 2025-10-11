"""Create a fastapi api layer to call the workflows of the core logic.

Created: 06.08.2025
@author: Max Weise
"""

import io
from typing import Any

import fastapi
import starlette.responses
from fastapi.middleware.cors import CORSMiddleware

import saison_kickstarter.exceptions
from saison_kickstarter import file_writer, tournament, view_builder

app = fastapi.FastAPI()

origins = [
    "http://localhost:5173",  # Allow requests from dev server
    "http://127.0.0.1:5173",  # Allow requests from dev server
    "http://localhost:8080",  # Allow requests from prod server
    "http://127.0.0.1:8080",  # Allow requests from prod server
    "http://localhost:9000",  # Allow requests from docker container
    "http://127.0.0.1:9000",  # Allow requests from docker container
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Use this endpoint as a healthcheck."""
    return {"message": "The api is live"}


@app.post("/overview/tournament")
def create_tournament_overview(
    items: list[tournament.Tournament],
    include_optional: bool | None = None,
    file_name: str | None = None,
) -> Any:
    """## Create an overview for all tournaments for the season.

    ### Args:
    - **items** _(list[tournament.Tournament])_: A list of tournament items that
        form the data basis of the overviews.
    - **include_optional** _(bool, Optional)_: Include optional tournaments for
        each age group. Defaults to _False_.
    - **file_name** _(str, Optional)_: The name of the created excel file.
        Defaults to _user_overview.xlsx_.

    ### Returns:
    A StreamingResponse containing the Excel file.

    ### Raises:
    **saison_kickstarter.exceptions.WorkbookError**: Something went wrong while
        trying to write the excel file. Please refer to the error message
        for further information.
    """
    io_buffer = io.BytesIO()

    builder = view_builder.TournamentViewBuilder(
        include_optional if include_optional else False
    )
    writer = file_writer.ExcelFileWriter(io_buffer)

    view = builder.build_view(items)

    # Buffer object gets modified
    try:
        writer.write_tournament_data(view)
        io_buffer.seek(0)
    except saison_kickstarter.exceptions.WorkbookError as e:
        raise fastapi.HTTPException(status_code=500, detail=e)

    # Return the file as a StreamingResponse
    media_type = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    fn = file_name if file_name else "user_overview.xlsx"
    headers = {
        "Content-Disposition": f"attachment; filename={fn}",
    }
    return starlette.responses.StreamingResponse(
        io_buffer, media_type=media_type, headers=headers
    )


@app.post("/overview/referee")
def create_referee_overview(
    items: list[tournament.Tournament], file_name: str | None = None
) -> Any:
    """## Create an overview over all tournaments that need referee coverage.

    ### Args:
    - **items** _(list[tournament.Tournament])_: A list of tournament items that
        form the data basis of the overviews.
    - **file_name** _(str, Optional)_: The name of the created excel file.
        Defaults to _user_overview.xlsx_.

    ### Returns:
    A StreamingResponse containing the Excel file.

    ### Raises:
    **saison_kickstarter.exceptions.WorkbookError**: Something went wrong while
        trying to write the excel file. Please refer to the error message
        for further information.
    """
    io_buffer = io.BytesIO()

    builder = view_builder.RefereeViewBuilder()
    writer = file_writer.ExcelFileWriter(io_buffer)

    view = builder.build_view(items)

    try:
        writer.write_referee_data(view)
        io_buffer.seek(0)
    except saison_kickstarter.exceptions.WorkbookError as e:
        raise fastapi.HTTPException(status_code=500, detail=e)

    # Return the file as a StreamingResponse
    media_type = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    fn = file_name if file_name else "user_overview.xlsx"
    headers = {
        "Content-Disposition": f"attachment; filename={fn}",
    }
    return starlette.responses.StreamingResponse(
        io_buffer, media_type=media_type, headers=headers
    )
