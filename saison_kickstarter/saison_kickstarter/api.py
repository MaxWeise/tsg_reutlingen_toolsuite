"""Create a fastapi api layer to call the workflows of the core logic.

Created: 06.08.2025
@author: Max Weise
"""

import fastapi
from fastapi.middleware.cors import CORSMiddleware

from saison_kickstarter import tournament

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
def create_tournament_overview(items: list[tournament.Tournament]) -> None:
    """Create an overview for all tournaments for the season.

    Args:
        items (list[tournaments]): A list of tournament items that form the
            data basis of the overviews.
    """
    # NOTE: Refer to the obsidian entry for more specific info
    # The Overview needs to be created as a dataframe, which then can be
    # written to an excel file via the pandas library.
    print(f"{items = }")


