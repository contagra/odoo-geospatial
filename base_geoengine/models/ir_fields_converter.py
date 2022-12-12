# -*- coding: utf-8 -*-

import json
from odoo import models, api, _
from shapely import wkt, geometry

class IrFieldsConverter(models.AbstractModel):
    _inherit = 'ir.fields.converter'

    @api.model
    def _str_to_geo_multi_polygon(self, model, field, value):
        try:
            g1 = wkt.loads(value)
            g2 = geometry.mapping(g1)
            js = json.dumps(g2)
            return js, []
        except ValueError:
            raise self._format_import_error(
                ValueError,
                _(u"'%s' does not seem to be an geometry for field '%%(field)s'"),
                value
            )
