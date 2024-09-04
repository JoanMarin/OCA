# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PurchaseCostDistributionExpense(models.Model):
    _inherit = "purchase.cost.distribution.expense"

    state = fields.Selection(string='Status', related="distribution.state")

    @api.onchange("invoice_line")
    def onchange_invoice_line(self):
        msg = _(
            "You cannot change the value of the expense amount if the status is 'Done' "
            "or 'Accounted'."
        )
        old_expense_amount = self.expense_amount
        super(PurchaseCostDistributionExpense, self).onchange_invoice_line()

        if (
            self.state in ("done", "accounted")
            and old_expense_amount != self.expense_amount
        ):
            raise UserError(msg)
