# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountAccount(models.Model):
    _inherit = "account.account"

    is_service_order_account = fields.Boolean(
        string="Is a Service Order Account?", default=False
    )
