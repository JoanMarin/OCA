# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

{
    "name": "Account Fiscal Unit",
    "version": "12.0.1.0.0",
    "category": "Accounting",
    "author": "EXA Auto Parts Github@exaap, "
    "Joan Marín Github@JoanMarin, "
    "Odoo Community Association (OCA)",
    "maintainers": ["joanmarin"],
    "website": "https://github.com/OCA/account-financial-tools",
    "depends": [
        "account_group_menu",
        "account_fiscal_year",
    ],
    "data": [
        "data/decimal_precision_data.xml",
        "views/account_fiscal_year_views.xml",
        "views/account_invoice_views.xml",
        "views/account_tax_group_views.xml",
    ],
    "installable": True,
    "license": "AGPL-3",
}
