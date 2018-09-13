import os

import pandas as pd

from chorogrid import Colorbin
from chorogrid import Chorogrid


DEFAULT_COLORS = [
    '#b35806', '#f1a340', '#fee0b6', '#d8daeb', '#998ec3', '#542788']
DEFAULT_COMPLEMENTS = ['#e0e0e0', '#101010']
SPEC_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "databases", "usa_states.csv")

STATE_ABBREVS = {
    "ALABAMA": "AL",
    "ALASKA": "AK",
    "ARIZONA": "AZ",
    "ARKANSAS": "AR",
    "CALIFORNIA": "CA",
    "COLORADO": "CO",
    "CONNECTICUT": "CT",
    "DELAWARE": "DE",
    "FLORIDA": "FL",
    "GEORGIA": "GA",
    "HAWAII": "HI",
    "IDAHO": "ID",
    "ILLINOIS": "IL",
    "INDIANA": "IN",
    "IOWA": "IA",
    "KANSAS": "KS",
    "KENTUCKY": "KY",
    "LOUISIANA": "LA",
    "MAINE": "ME",
    "MARYLAND": "MD",
    "MASSACHUSETTS": "MA",
    "MICHIGAN": "MI",
    "MINNESOTA": "MN",
    "MISSISSIPPI": "MS",
    "MISSOURI": "MO",
    "MONTANA": "MT",
    "NEBRASKA": "NE",
    "NEVADA": "NV",
    "NEW HAMPSHIRE": "NH",
    "NEW JERSEY": "NJ",
    "NEW MEXICO": "NM",
    "NEW YORK": "NY",
    "NORTH CAROLINA": "NC",
    "NORTH DAKOTA": "ND",
    "OHIO": "OH",
    "OKLAHOMA": "OK",
    "OREGON": "OR",
    "PENNSYLVANIA": "PA",
    "RHODE ISLAND": "RI",
    "SOUTH CAROLINA": "SC",
    "SOUTH DAKOTA": "SD",
    "TENNESSEE": "TN",
    "TEXAS": "TX",
    "UTAH": "UT",
    "VERMONT": "VT",
    "VIRGINIA": "VA",
    "WASHINGTON": "WA",
    "WEST VIRGINIA": "WV",
    "WISCONSIN": "WI",
    "WYOMING": "WY",
    "WASHINGTON DC": "DC"
}


def _get_state(state):
    state = state.replace(", ", "").replace(".", " ").upper().strip()
    return STATE_ABBREVS.get(state, state)


def plot(
        states, values, title="", legend="",
        colors=DEFAULT_COLORS, complements=DEFAULT_COMPLEMENTS,
        font={}, spacing={}, decimals=1, shape="hex"):
    states = [_get_state(state) for state in states]

    # Colors
    cbin = Colorbin(values, colors, proportional=True, decimals=None)
    cbin.set_decimals(decimals)
    cbin.recalc(fenceposts=True)
    cbin.calc_complements(0.5, *complements)

    # Choropleth
    cg = Chorogrid(SPEC_PATH, states, cbin.colors_out)
    cg.set_title(title, font_dict=font)
    cg.set_legend(cbin.colors_in, cbin.labels, title=legend)

    # Draw
    draw_fn = {
        "hex": cg.draw_hex,
        "square": cg.draw_squares,
        "multihex": cg.draw_multihex,
        "multisquare": cg.draw_multisquare,
        "map": cg.draw_map
    }[shape]
    draw_fn(spacing_dict=spacing)
    return cg.done(show=True)
