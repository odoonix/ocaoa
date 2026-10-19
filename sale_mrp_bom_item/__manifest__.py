# pylint: disable=W0104
{
    "name": "Sale MRP BoM Item",
    "category": "Sale",
    "license": "AGPL-3",
    "author": "MoonSun PTY LTD",
    "version": "19.0.1.0.0",
    "website": "https://moonsun.au",
    "summary": "Rename BoM column to Item in sale order lines",
    "depends": [
        "sale_mrp_bom",
    ],
    "data": [
        "views/sale_order_views.xml",
    ],
    "installable": True,
}
