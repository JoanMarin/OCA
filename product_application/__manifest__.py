# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

{
    "name": "Product Application",
    "version": "12.0.1.0.0",
    "category": "Product",
    "author": "EXA Auto Parts Github@exaap, "
    "Joan Marín Github@JoanMarin, "
    "Odoo Community Association (OCA)",
    "maintainers": ["joanmarin"],
    "website": "https://github.com/OCA/product-attribute",
    "depends": [
        "sale_management",
    ],
    "data": [
        "security/ir_module_category.xml",
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "views/product_application_category_views.xml",
        "views/product_application_views.xml",
        "views/product_product_views.xml",
        "views/product_template_views.xml",
    ],
    "installable": True,
    "license": "AGPL-3",
}
