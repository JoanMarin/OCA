# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _run_valuation(self, quantity=None):
        value_to_return = super(StockMove, self)._run_valuation(quantity)
        move_id = self.origin_returned_move_id

        if (
            self._is_out()
            and move_id
            and move_id._is_in()
            and move_id.product_id == self.product_id
        ):
            value_to_return = -move_id.price_unit * self.product_uom_qty
            self.write(
                {
                    "value": value_to_return,
                    "price_unit": -move_id.price_unit,
                }
            )

            if self.product_id.qty_available > 0:
                self.product_id.standard_price = (
                    self.product_id.standard_price
                    * (self.product_id.qty_available + self.product_uom_qty)
                    + self.price_unit * self.product_uom_qty
                ) / self.product_id.qty_available

        return value_to_return
