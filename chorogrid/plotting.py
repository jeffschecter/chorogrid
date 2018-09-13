import os

import pandas as pd

from chorogrid import Colorbin
from chorogrid import Chorogrid


DEFAULT_COLORS = [
    '#b35806', '#f1a340', '#fee0b6', '#d8daeb', '#998ec3', '#542788']
DEFAULT_COMPLEMENTS = ['#e0e0e0', '#101010']
STATE_FILEPATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "databases", "usa_states.csv")
COUNTY_FILEPATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "databases", "usa_counties.csv")
COUNTY_IDS = set(pd.read_csv(COUNTY_FILEPATH).fips_integer.unique())


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

HEXILE_LABELS = ["- - -", "- -", "-", "+", "++", "+++"]


def _get_state(state):
    state = state.replace(", ", "").replace(".", " ").upper().strip()
    return STATE_ABBREVS.get(state, state)


def plot(
        states, values, title="", legend="",
        colors=DEFAULT_COLORS, complements=DEFAULT_COMPLEMENTS,
        font={}, spacing={}, decimals=1, shape="hex", quantile=False):
    states = [_get_state(state) for state in states]
    states, values = zip(*[
        (state, value) for state, value in zip(states, values)
        if state in STATE_ABBREVS.values()])
    if quantile:
        values = pd.qcut(values, 6, [-20, -10, -1, 1, 10, 20])

    # Colors
    cbin = Colorbin(values, colors, proportional=True, decimals=None)
    cbin.set_decimals(decimals)
    cbin.recalc(fenceposts=True)
    cbin.calc_complements(0.0, *complements)

    # Choropleth
    cg = Chorogrid(STATE_FILEPATH, states, cbin.colors_out)
    cg.set_title(title, font_dict=font)
    if quantile:
        labels = HEXILE_LABELS
    else:
        labels = cbin.labels
    cg.set_legend(cbin.colors_in, labels, title=legend)

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


def plot_counties(
        fips, values, title="", legend="",
        colors=DEFAULT_COLORS, complements=DEFAULT_COMPLEMENTS,
        font={}, spacing={}, decimals=1, quantile=False):
    fips, values = zip(*[
        (fip, value) for fip, value in zip(fips, values)
        if fip in COUNTY_IDS])
    if quantile:
        values = pd.qcut(values, 6, [-20, -10, -1, 1, 10, 20])

    # Colors
    cbin = Colorbin(values, colors, proportional=True, decimals=None)
    cbin.set_decimals(decimals)
    cbin.recalc(fenceposts=True)
    cbin.calc_complements(0.0, *complements)

    # Choropleth
    cg = Chorogrid(
        COUNTY_FILEPATH, fips, cbin.colors_out,
        id_column="fips_integer")
    cg.set_title(title, font_dict=font)
    if quantile:
        labels = HEXILE_LABELS
    else:
        labels = cbin.labels
    cg.set_legend(cbin.colors_in, labels, title=legend)

    # Draw
    cg.draw_map(spacing_dict=spacing)
    return cg.done(show=True)
