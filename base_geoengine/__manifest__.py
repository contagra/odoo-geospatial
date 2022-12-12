# Copyright 2011-2015 Nicolas Bessi (Camptocamp SA)
# Copyright 2016 Yannick Vaucher (Camptocamp SA)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Geospatial support for Odoo",
    "version": "15.0.1.0.2",
    "category": "GeoBI",
    "author": "Camptocamp,ACSONE SA/NV,Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/geospatial",
    "depends": ["base", "web"],
    "data": [
        "security/data.xml",
        "views/base_geoengine_view.xml",
        "geo_ir/ir_model_view.xml",
        "geo_view/ir_view_view.xml",
        "geo_view/geo_raster_layer_view.xml",
        "geo_view/geo_vector_layer_view.xml",
        "security/ir.model.access.csv",
    ],
    "external_dependencies": {"python": ["shapely", "geojson", "simplejson"]},
    # "qweb": ["static/src/xml/geoengine.xml"],

    'assets': {
        'web.assets_backend': [
            'base_geoengine/static/src/js/geoengine_common.js',
            'base_geoengine/static/src/js/widgets/geoengine_record.js',
            'base_geoengine/static/src/js/widgets/geoengine_template_widgets.js',
            'base_geoengine/static/src/js/widgets/geoengine_widgets.js',
            'base_geoengine/static/src/js/views/geoengine/geoengine_renderer.js',
            'base_geoengine/static/src/js/views/geoengine/geoengine_controller.js',
            'base_geoengine/static/src/js/views/geoengine/geoengine_view.js',
            'base_geoengine/static/src/js/views/view_registry.js',
            'base_geoengine/static/src/js/views/form_renderer.js',
            'base_geoengine/static/src/css/style.css',
            '/base_geoengine/static/lib/ol-5.3.3/ol.css',
            '/base_geoengine/static/lib/ol3-layerswitcher.css',
            '/base_geoengine/static/lib/geostats-2.0.0/geostats.css',
            '/base_geoengine/static/lib/ol-5.3.3/ol.js',
            '/base_geoengine/static/lib/ol3-layerswitcher.js',
            '/base_geoengine/static/lib/chromajs-0.8.0/chroma.js',
            '/base_geoengine/static/lib/geostats-2.0.0/geostats.js',
        ],
        'web.assets_qweb': [
            'base_geoengine/static/src/**/*.xml',
        ],
    },

    "installable": True,
    "pre_init_hook": "init_postgis",
}
