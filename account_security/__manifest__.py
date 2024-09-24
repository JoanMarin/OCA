# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

{
    "name": "Account Security",
    "version": "16.0.1.0.0",
    "category": "Accounting",
    "author": "EXA Auto Parts Github@exaap, "
    "Joan Marín Github@JoanMarin, "
    "Odoo Community Association (OCA)",
    "maintainers": ["joanmarin"],
    "website": "https://github.com/OCA/account-financial-tools",
    "depends": [
        "account",
    ],
    "data": [
        "security/res_groups.xml",
        "views/account_account_views.xml",
        "views/account_move_views.xml",
    ],
    "installable": True,
    "license": "AGPL-3",
}
