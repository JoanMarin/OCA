# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

{
    "name": "Account Tax Group Type",
    "version": "12.0.1.0.0",
    "category": "Accounting",
    "author": "EXA Auto Parts Github@exaap, "
    "Joan Marín Github@JoanMarin, "
    "Odoo Community Association (OCA)",
    "maintainers": ["joanmarin"],
    "website": "https://github.com/OCA/account-financial-tools",
    "depends": [
        "account_group_menu",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/account_tax_group_views.xml",
    ],
    "installable": True,
    "license": "AGPL-3",
}
