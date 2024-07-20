# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import fields, models
from odoo.addons import decimal_precision as dp


class AccountFiscalYear(models.Model):
    _inherit = "account.fiscal.year"

    fiscal_unit = fields.Float(
        string="Fiscal Unit",
        help="Value of the Fiscal Unit. Example: UVT Colombia.",
        digits=dp.get_precision("Fiscal Unit"),
    )
