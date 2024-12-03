# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

{
    "name": "iFrames Dashboards",
    "version": "16.0.1.0.0",
    "category": "Extra Tools",
    "author": "EXA Auto Parts Github@exaap, "
    "Joan Marín Github@JoanMarin, "
    "Odoo Community Association (OCA)",
    "maintainers": ["joanmarin"],
    "website": "https://github.com/OCA/reporting-engine",
    "depends": [
        "board",
    ],
    "data": [
        "security/ir_module_category.xml",
        "security/res_groups.xml",
        "security/ir_rule.xml",
        "security/ir.model.access.csv",
        "views/iframe_dashboard_views.xml",
    ],
    "installable": True,
    "license": "AGPL-3",
}
