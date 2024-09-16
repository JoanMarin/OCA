# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    is_service_order_account = fields.Boolean(
        related="account_id.is_service_order_account",
        string="Is a Service Order Account?",
    )
    has_service_order = fields.Selection(
        selection=[("no", "No"), ("yes", "Yes")],
        string="Has Service Order?",
        default=False,
    )
    service_order_id = fields.Many2one(
        comodel_name="account.service.order",
        string="Service Order",
        domain="[('state', '=', 'open'), ('partner_id', '=', partner_id)]",
    )
