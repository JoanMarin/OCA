# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

{
    "name": "Purchase landed costs - Alternative option - Account",
    "version": "12.0.1.0.0",
    "category": "Purchase Management",
    "author": "EXA Auto Parts Github@exaap, "
    "Joan Marín Github@JoanMarin, "
    "Odoo Community Association (OCA)",
    "maintainers": ["joanmarin"],
    "website": "https://github.com/OCA/purchase-workflow",
    "depends": [
        "purchase_landed_cost",
        "account_move_line_stock_info",
    ],
    "data": [
        "views/stock_picking_views.xml",
        "views/purchase_cost_distribution_views.xml",
        "views/account_move_line_views.xml",
    ],
    "installable": True,
    "license": "AGPL-3",
}
