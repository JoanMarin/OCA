# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

{
    "name": "Partner Email Check Exception",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/partner-contact",
    "author": "EXA Auto Parts Github@exaap, "
    "Joan Marín Github@JoanMarin, "
    "Odoo Community Association (OCA)",
    "maintainers": ["joanmarin"],
    "category": "Partner Management",
    "depends": [
        "contacts",
        "partner_email_check",
    ],
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "views/res_partner_email_exception_views.xml",
    ],
    "installable": True,
}
