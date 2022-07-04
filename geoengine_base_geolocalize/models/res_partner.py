##############################################################################
#
#   Author: Laurent Mignon
#   Copyright (c) 2015 Acsone SA/NV (http://www.acsone.eu)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging
import json

from odoo import api, exceptions, fields, models
from odoo.tools.translate import _
from shapely.geometry import Point

try:
    import requests
except ImportError:
    logger = logging.getLogger(__name__)
    logger.warning("requests is not available in the sys path")

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    """Add location to partner using a function field"""

    _inherit = "res.partner"

    def geocode_address(self):
        """Get the latitude and longitude by requesting the "Nominatim"
        search engine from "openstreetmap". See:
        https://nominatim.org/release-docs/latest/api/Overview/
        """
        url = "http://nominatim.openstreetmap.org/search"
        headers = {"User-Agent": "Odoobot/14.0.1.0.0 (OCA-geospatial)"}

        for partner in self:
            pay_load = {
                "limit":
                    1,
                "format":
                    "json",
                "street":
                    partner.street or "",
                "postalCode":
                    partner.zip or "",
                "city":
                    partner.city or "",
                "state":
                    partner.state_id and partner.state_id.name or "",
                "country":
                    partner.country_id and partner.country_id.name or "",
                "countryCodes":
                    partner.country_id and partner.country_id.code or "",
            }

            request_result = requests.get(url, params=pay_load, headers=headers)
            try:
                request_result.raise_for_status()
            except Exception as e:
                _logger.exception("Geocoding error")
                raise exceptions.UserError(_("Geocoding error. \n %s") % str(e))
            vals = request_result.json()
            vals = vals and vals[0] or {}
            geojson = {
                "type": "Point",
                "coordinates": [float(vals.get("lon")),
                                float(vals.get("lat"))]
            }
            geostr = json.dumps(geojson)
            partner.write({
                "partner_latitude": vals.get("lat"),
                "partner_longitude": vals.get("lon"),
                "date_localization": fields.Date.today(),
                "location": geostr,
            })

    def geo_localize(self):
        self.geocode_address()
        return True

    @api.onchange("partner_latitude", "partner_longitude")
    @api.depends("partner_latitude", "partner_longitude")
    def _compute_location(self):
        """
        Set the `location` of the partner depending on `partner_latitude`
        and `partner_longitude`
        """
        for partner in self:
            if partner.partner_latitude and partner.partner_longitude:
                geojson = {
                    "type":
                        "Point",
                    "coordinates": [
                        partner.partner_longitude, partner.partner_latitude
                    ]
                }
                geostr = json.dumps(geojson)
                partner.write({
                    "location": geostr,
                })

    @api.onchange("location")
    @api.depends("location")
    def _compute_lat_long(self):
        """
        Set the `partner_latitude` and `partner_longitude` of the partner
        depending on `location`
        """
        for partner in self:
            if partner.location:
                lat = partner.location.y
                long = partner.location.x
                partner.write({
                    "date_localization": fields.Date.today(),
                    "partner_latitude": lat,
                    "partner_longitude": long,
                })

    @api.model
    def create(self, vals):
        partner = super(ResPartner, self).create(vals)
        if not partner.location:
            partner._compute_location()
        return partner

    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        """
        if vals.get('partner_latitude') or vals.get('partner_longitude'):
            long = vals.get('partner_longitude', self.partner_longitude)
            lat = vals.get('partner_latitude', self.partner_latitude)
            geojson = {"type": "Point", "coordinates": [long, lat]}
            geostr = json.dumps(geojson)
            vals['location'] = geostr
        """
        return res
