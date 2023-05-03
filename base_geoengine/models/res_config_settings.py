# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    mapbox_token = fields.Char(config_parameter='base_geoengine.token_mapbox', string='Mapbox Token',
                               help='Required for adding Mapbox styles as layers', copy=True, default='',
                               store=True)
