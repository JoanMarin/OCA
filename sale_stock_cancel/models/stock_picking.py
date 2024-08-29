# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import models, api, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    def action_cancel(self):
        done_move_ids = self.mapped("move_lines").filtered(lambda m: m.state == "done")
        sale_ids = self.mapped("move_lines").mapped("picking_id").mapped("sale_id")

        if not done_move_ids or not sale_ids:
            return super(StockPicking, self).action_cancel()

        msg = _(
            "You cannot cancel a sale order that has a stock move that has been set to "
            "'Done' and does not have its respective return."
        )
        product_dict = {}

        for done_move_id in done_move_ids.sorted(key=lambda m: m.date):
            product_id = done_move_id.product_id
            location_id = done_move_id.location_id
            location_dest_id = done_move_id.location_dest_id
            product_qty = done_move_id.product_qty

            if product_id not in product_dict:
                product_dict[product_id] = {}

            if location_id not in product_dict[product_id]:
                product_dict[product_id][location_id] = -product_qty
            else:
                product_dict[product_id][location_id] -= product_qty

            if location_dest_id not in product_dict[product_id]:
                product_dict[product_id][location_dest_id] = product_qty
            else:
                product_dict[product_id][location_dest_id] += product_qty

        for product_id in product_dict.keys():
            for location_id in product_dict[product_id].keys():
                if product_dict[product_id][location_id] != 0:
                    raise UserError(msg)

        other_move_ids = self.mapped("move_lines").filtered(lambda m: m.state != "done")

        if other_move_ids:
            other_move_ids._action_cancel()
            other_move_ids.write({"is_locked": True})

        return sale_ids.write({"is_anulled": True})
