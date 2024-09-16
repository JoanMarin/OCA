# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Account Service Order",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/l10n-el-salvador",
    "author": "EXA Auto Parts Github@exaap, "
    "Joan Marín Github@JoanMarin, "
    "Odoo Community Association (OCA)",
    "maintainers": ["joanmarin"],
    "category": "Account",
    "depends": [
        "account",
    ],
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "wizards/account_move_line_set_service_order_views.xml",
        "views/account_account_views.xml",
        "views/account_move_line_views.xml",
        "views/account_move_views.xml",
        "views/account_service_order_views.xml",
    ],
    "installable": True,
}
