# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Manufacturing Stock Account",
    "version": "12.0.1.0.0",
    "category": "Manufacturing",
    "author": "EXA Auto Parts Github@exaap, "
    "Joan Marín Github@JoanMarin, "
    "Odoo Community Association (OCA)",
    "maintainers": ["joanmarin"],
    "website": "https://github.com/OCA/manufacture",
    "depends": [
        "mrp",
        "stock_account",
    ],
    "data": [
        "views/mrp_production.xml",
    ],
    "installable": True,
    "license": "AGPL-3",
}
