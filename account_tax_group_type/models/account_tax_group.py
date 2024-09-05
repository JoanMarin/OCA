# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import fields, models


class AccountTaxGroup(models.Model):
    _inherit = "account.tax.group"

    tax_group_type_id = fields.Many2one(
        comodel_name="account.tax.group.type", string="Tax Group Type"
    )
