# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_anulled = fields.Boolean(string="Is Anulled?")
    state = fields.Selection(selection_add=[("annul", "Annulled")])

    @api.multi
    def action_cancel(self):
        res = super(SaleOrder, self).action_cancel()
        anulled_sale_ids = self.filtered(lambda m: m.is_anulled)

        if anulled_sale_ids:
            anulled_sale_ids.write({"state": "annul"})

        return res
