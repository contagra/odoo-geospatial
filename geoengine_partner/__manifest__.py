# Copyright 2011-2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    "name": "Geospatial support of partners",
    "version": "14.0.1.0.0",
    "category": "GeoBI",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/geospatial",
    "depends": [
        "base",
        "base_geoengine",
        "contacts"
    ],
    "data": [
        "views/res_partner_views.xml",
        "views/assets.xml",
    ],
    "installable": True,
    "application": True,
}
