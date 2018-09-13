import pandas as pd

from chorogrid import Colorbin
from chorogrid import Chorogrid


DEFAULT_COLORS = [
    '#b35806', '#f1a340', '#fee0b6', '#d8daeb', '#998ec3', '#542788']
DEFAULT_COMPLEMENTS = ['#e0e0e0', '#101010']


def plot(
        states, values, title, legend,
        colors=DEFAULT_COLORS, complements=DEFAULT_COMPLEMENTS,
        font={}, spacing={}, decimals=1, shape="hex"):
    df = pd.DataFrame({"state": states, "val": values})

    # Colors
    cbin = Colorbin(values, colors, proportional=True, decimals=None)
    cbin.set_decimals(decimals)
    cbin.recalc(fenceposts=True)
    cbin.calc_complements(0.5, *complements)

    # Choropleth
    cg = Chorogrid(df, states, cbin.colors_out)
    cg.set_title(title, font_dict=font)
    cg.set_legend(cbin.colors_in, cbin.labels, title=legend)

    # Draw
    if shape == "square":
        cg.draw_squares(spacing_dict=spacing)
    elif shape == "hex":
        cg.draw_hex(spacing_dict=spacing)
    return cg.done(show=True)
