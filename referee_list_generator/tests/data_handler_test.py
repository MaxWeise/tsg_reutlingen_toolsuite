"""Test the correct manipulation of data.

Created: 05.11.2023
@author: Max Weise
"""

import pytest
from referee_list_generator.main import prepare_data  # type: ignore


@pytest.fixture()
def data_set():
    return [
        (
            "id",
            "lastname",
            "firstname",
            "dateofbirth",
            "nation",
            "nationality1",
            "nationality2",
            "club_id",
            "clubname",
            "gender",
            "addressStreet",
            "addressPostcode",
            "addressCi ty",
            "addressCountry",
        ),
        (
            "201156",
            "Mayer",
            "Olaf",
            "01.01.1972",
            "GER",
            "GER",
            "",
            "350",
            "TS G Hauptverein",
            "M",
            "Feldweg 13/5",
            "72795",
            "Hauptstadt",
            "Deutschland",
        ),
        (
            "197177",
            "Müller ",
            "Frank",
            "01.11.2002",
            "GER",
            "GER",
            "FRA",
            "350",
            "TSG Hauptverein",
            "M",
            "Boschweg 21",
            "72795",
            "Hauptstadt",
            "Deutschland",
        ),
        (
            "192733",
            "Schmidt",
            "Nadia",
            "16.05.1990",
            "GER",
            "GER ",
            "",
            "350",
            "TSG Hauptverein",
            "F",
            "Hauptstraße 7",
            "72718",
            "Hauptstadt",
            "Deutschland",
        ),
        (
            "3364",
            "Scholz",
            "Sabine",
            "01.01.2001",
            "GER",
            "GER",
            "",
            "350",
            "TSG Hauptverein",
            "F",
            "Siebenerweg 5",
            "72795",
            "Hauptstadt",
            "Deutschland",
        ),
        (
            "198929",
            "Henrikson",
            "Henry",
            "01.01.1901",
            "GER",
            "GER",
            "",
            "350",
            "TSG Hauptverein",
            "M",
            "Nebengasse 27/1",
            "72797",
            "Kleindorf ",
            "Deutschland",
        ),
        (
            "201386",
            "Forger",
            "Yor",
            "01.01.1992",
            "GER",
            "GER",
            "",
            "350",
            "TSG Hauptverein",
            "F",
            "Westalisweg 3",
            "72795",
            "Berlint",
            "Deutschland",
        ),
        (
            "201099",
            "Forger",
            "Loid",
            "17.05.1982",
            "GER",
            "GER",
            "",
            "350",
            "TSG Hauptverein",
            "M",
            "Westalisweg 3",
            "72795",
            "Berlint",
            "Deutschland",
        ),
    ]


def test_clean_data(data_set):
    """Test that the correct columns get extracted."""
    actual = prepare_data(data_set)

    assert actual is not None

    header = actual.get("header", None)
    print(header)
    assert header is not None
    assert len(header) == 3

    content = actual.get("content", None)
    print(content)
    assert content is not None
    assert len(content) == (len(data_set) - 1)

    for row in content:
        assert all(row)
