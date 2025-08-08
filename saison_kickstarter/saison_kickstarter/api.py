"""Create a fastapi api layer to call the workflows of the core logic.

Created: 06.08.2025
@author: Max Weise
"""

import fastapi

app = fastapi.FastAPI()


@app.get("/")
def root():
    """Use this endpoint as a healthcheck."""
    return {"message": "The api is live"}


@app.get("/overview/tournament")
def create_tournament_overview():
    """Create an overview for all tournaments for the season."""
    return ...



