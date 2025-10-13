{
    "name": "Connector",
    "version": "19.0.1.0.0",
    "author": "Camptocamp,Odoo Community Association (OCA)",
    "website": "https://www.moonsun.au/apps/integeration-toolbox",
    "license": "LGPL-3",
    "category": "Generic Modules",
    "depends": ["mail", "queue_job", "component", "component_event"],
    "data": [
        "security/connector_security.xml",
        "views/connector_menu.xml",
        "views/res_partner_views.xml",
    ],
    "installable": True,
}
