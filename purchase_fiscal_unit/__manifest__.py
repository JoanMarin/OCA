# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

{
    "name": "Purchase Fiscal Unit",
    "summary": "This module allows to evaluate a tax at purchase order level, "
    "using parameters such as total base and others.",
    "version": "12.0.1.0.0",
    "category": "Purchase",
    "author": "EXA Auto Parts Github@exaap, "
    "Joan Marín Github@JoanMarin, "
    "Odoo Community Association (OCA)",
    "maintainers": ["joanmarin"],
    "website": "https://github.com/OCA/purchase-workflow",
    "depends": [
        "purchase_discount",
        "account_fiscal_unit",
    ],
    "installable": True,
    "license": "AGPL-3",
    "auto_install": True,
}
