"""Test the correct manipulation of data.

Created: 05.11.2023
@author: Max Weise
"""

# pylint: disable=redefined-outer-name

import pytest
from ophardt_to_excel.functions import get_data_rows
from ophardt_to_excel.system_core import DataRow


@pytest.fixture()
def data_set():
    """Personal data extracted from a csv-file."""
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


def test_get_data_rows(data_set):
    """Test that the correct columns get extracted."""
    actual = get_data_rows(data_set)

    assert actual is not None

    under_test = actual[0]
    expected = DataRow(
        last_name="Mayer", first_name="Olaf", year_of_birth="1972"
    )

    assert under_test is not None
    assert under_test == expected
