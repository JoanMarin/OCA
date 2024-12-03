# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

{
    "name": "Product Brand Unique",
    "version": "15.0.1.0.0",
    "category": "Product",
    "author": "EXA Auto Parts Github@exaap, "
    "Joan Marín Github@JoanMarin, "
    "Odoo Community Association (OCA)",
    "maintainers": ["joanmarin"],
    "website": "https://github.com/OCA/brand",
    "depends": [
        "product_brand",
        "product_manufacturer",
    ],
    "data": [
        "views/product_brand_views.xml",
        "views/res_partner_views.xml",
    ],
    "installable": True,
    "license": "AGPL-3",
}
