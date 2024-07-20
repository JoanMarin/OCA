# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import fields, models
from odoo.addons import decimal_precision as dp


class AccountTaxGroup(models.Model):
    _inherit = "account.tax.group"

    fiscal_unit_factor = fields.Float(
        string="Fiscal Unit Factor",
        help="Number of Fiscal Units from which the tax is calculated",
        digits=dp.get_precision("Fiscal Unit"),
    )
    fiscal_unit_partner_ids = fields.Many2many(
        comodel_name="res.partner",
        relation="account_tax_group_res_partner_fiscal_unit_rel",
        column1="account_tax_group_id",
        column2="partner_id",
        string="Partners that do not apply Fiscal Unit Factor",
    )
