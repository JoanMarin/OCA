# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Equivalent Products with Manufacturer and Brand",
    "version": "15.0.1.0.0",
    "category": "Product",
    "author": "EXA Auto Parts Github@exaap, "
    "Joan Marín Github@JoanMarin, "
    "Odoo Community Association (OCA)",
    "maintainers": ["joanmarin"],
    "website": "https://github.com/OCA/product-attribute",
    "depends": [
        "product_brand_unique",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_equivalent_classification_views.xml",
        "views/product_equivalent_views.xml",
        "views/product_product_views.xml",
        "views/product_template_views.xml",
    ],
    "installable": True,
    "license": "AGPL-3",
}
