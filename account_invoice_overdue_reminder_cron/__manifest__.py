# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

{
    "name": "Overdue Invoice Reminder Cron",
    "version": "12.0.1.0.0",
    "category": "Accounting",
    "author": "EXA Auto Parts Github@exaap, "
    "Joan Marín Github@JoanMarin, "
    "Odoo Community Association (OCA)",
    "maintainers": ["joanmarin"],
    "website": "https://github.com/OCA/credit-control",
    "depends": [
        "account_invoice_overdue_reminder",
        "sale",
        "stock",
    ],
    "data": [
        "data/ir_cron_data.xml",
        "views/res_partner_views.xml",
    ],
    "installable": True,
    "license": "AGPL-3",
}
