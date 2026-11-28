{
    "name": "Tipax Shipping",
    "version": "18.0.1.0.0",
    "category": "Inventory/Delivery",
    "depends": ["stock_delivery", "mail"],
    "external_dependencies": {"python": ["requests"]},
    "data": ["views/views.xml", "data/cron.xml", "report/label.xml"],
    "license": "LGPL-3",
    "installable": True,
}
