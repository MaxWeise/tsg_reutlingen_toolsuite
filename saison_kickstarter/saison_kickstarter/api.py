"""Create a fastapi api layer to call the workflows of the core logic.

Created: 06.08.2025
@author: Max Weise
"""

import io
from typing import Any

import fastapi
import starlette.responses
from fastapi.middleware.cors import CORSMiddleware

from saison_kickstarter import file_writer, tournament, view_builder

app = fastapi.FastAPI()

origins = [
    "http://localhost:5173",
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
def create_tournament_overview(items: list[tournament.Tournament]) -> Any:
    """Create an overview for all tournaments for the season.

    Args:
        items (list[tournaments]): A list of tournament items that form the
            data basis of the overviews.
    """
    io_buffer = io.BytesIO()

    # TODO: Make it possible to turn on optional tournaments
    builder = view_builder.TournamentViewBuilder(False)
    writer = file_writer.ExcelFileWriter(io_buffer)

    view = builder.build_view(items)

    # Buffer object gets modified
    writer.write_tournament_data(view)
    io_buffer.seek(0)

    # Return the file as a StreamingResponse
    media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    headers = {
        "Content-Disposition": 'attachment; filename="user_overview.xlsx"'
    }
    return starlette.responses.StreamingResponse(io_buffer, media_type=media_type, headers=headers)
