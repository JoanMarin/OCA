# Copyright 2014-2016 Tecnativa - Pedro M. Baeza
# Copyright 2024 Tecnativa - Carolina Fernandez
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3
from odoo import api, fields, models


class ImportInvoiceLine(models.TransientModel):
    _name = "import.invoice.line.wizard"
    _description = "Import supplier invoice line"

    supplier = fields.Many2one(
        comodel_name="res.partner",
        required=True,
    )
    invoice = fields.Many2one(
        comodel_name="account.move",
        required=True,
        domain="[('partner_id', '=', supplier), ('state', '=', 'posted')]",
    )
    invoice_line = fields.Many2one(
        comodel_name="account.move.line",
        string="Invoice line",
        required=True,
        domain="[('move_id', '=', invoice)]",
    )
    expense_type = fields.Many2one(
        comodel_name="purchase.expense.type", string="Expense type", required=True
    )

    @api.multi
    def action_import_invoice_line(self):
        self.ensure_one()
        dist_id = self.env.context["active_id"]
        expense_amount = self.invoice_line.balance
        self.env["purchase.cost.distribution.expense"].create(
            {
                "distribution": dist_id,
                "invoice_line": self.invoice_line.id,
                "invoice_id": self.invoice_line.move_id.id,
                "ref": self.invoice_line.name,
                "expense_amount": expense_amount,
                "type": self.expense_type.id,
            }
        )
