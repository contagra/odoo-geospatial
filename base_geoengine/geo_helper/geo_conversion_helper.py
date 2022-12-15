# Copyright 2011-2012 Nicolas Bessi (Camptocamp SA)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

try:
    from shapely import wkt, wkb
    from shapely.geometry import shape
    from shapely.geometry.base import BaseGeometry
    import geojson
except ImportError:
    logger = logging.getLogger(__name__)
    logger.warning("Shapely or geojson are not available in the sys path")


def value_to_shape(value, use_wkb=False):
    """Transforms input into a Shapely object"""
    if not value:
        return wkt.loads("GEOMETRYCOLLECTION EMPTY")
    if isinstance(value, str):
        # We try to do this before parsing json
        # exceptions are resource costly
        if "{" in value:
            geo_dict = geojson.loads(value)
            sh = shape(geo_dict)
            return sh
        elif use_wkb:
            return wkb.loads(value, hex=True)
        else:
            return wkt.loads(value)
    elif hasattr(value, "wkt"):
        if isinstance(value, BaseGeometry):
            return value
        else:
            return wkt.loads(value.wkt)
    else:
        raise TypeError(
            "Write/create/search geo type must be wkt/geojson "
            "string or must respond to wkt"
        )
