# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.multi
    def get_tax_group_dict(self):
        tax_group_dict = {}
        round_curr = self.currency_id.round

        for line in self.order_line:
            price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.taxes_id.compute_all(
                price_unit,
                self.currency_id,
                line.product_qty,
                line.product_id,
                self.partner_id,
            )["taxes"]

            for tax in taxes:
                tax_group_id = self.env["account.tax"].browse(tax["id"]).tax_group_id

                if tax_group_id not in tax_group_dict:
                    tax_group_dict[tax_group_id] = {
                        "amount": tax["amount"],
                        "base": round_curr(tax["base"]),
                    }
                else:
                    tax_group_dict[tax_group_id]["amount"] += tax["amount"]
                    tax_group_dict[tax_group_id]["base"] += round_curr(tax["base"])

        return tax_group_dict

    def get_remove_tax_group_ids(self):
        msg = _("There is no fiscal year corresponding to the date of your order.")
        date = self.date_order.strftime("%Y-%m-%d") or fields.Date.today()
        fiscal_year_id = self.env["account.fiscal.year"].search(
            [("date_from", "<=", date), ("date_to", ">=", date)]
        )

        if not fiscal_year_id:
            raise UserError(msg)

        tax_group_dict = self.get_tax_group_dict()
        remove_tax_group_ids = []
        currency_rate = self.currency_id._convert(
            1, self.company_id.currency_id, self.company_id, date
        )

        for tax_group_id in tax_group_dict.keys():
            if (
                self.partner_id not in tax_group_id.fiscal_unit_partner_ids
                and tax_group_id.fiscal_unit_factor * fiscal_year_id.fiscal_unit
                > tax_group_dict[tax_group_id]["base"] * currency_rate
            ):
                remove_tax_group_ids.append(tax_group_id)

        return remove_tax_group_ids

    @api.onchange("order_line")
    def _onchange_order_line(self):
        self.order_line._compute_tax_id()
