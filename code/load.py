%config Completer.use_jedi = False

import numpy as np
import pandas as pd
import geopandas as gp
import holoviews as hv
import geoviews as gv
from geoviews import opts

import utils
import importlib
importlib.reload(utils)

gv.extension('bokeh')
opts.defaults(
    opts.Polygons( tools=['hover'], width=600, height=500),
    opts.Points( tools=['hover'], width=600, height=500),
    opts.Overlay(width=600, height=500)
    )