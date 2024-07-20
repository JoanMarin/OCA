# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import fields, models, _


class AccountTaxGroupType(models.Model):
    _name = "account.tax.group.type"
    _description = "Tax Group Type"

    code = fields.Char(string="Code", required=True)
    name = fields.Char(string="Name", required=True)
    type = fields.Selection(
        selection=[("tax", "Tax"), ("withholding_tax", "Withholding Tax")],
        string="Type",
        required=True,
        default=False,
    )
    description = fields.Char(string="Description")

    _sql_constraints = [
        ("code_unique", "UNIQUE(code)", _("The code of Tax Group Type must be unique!"))
    ]
