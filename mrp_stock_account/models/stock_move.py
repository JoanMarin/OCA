# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class StockMove(models.Model):
    _inherit = "stock.move"

    def _create_account_move_line(
        self, credit_account_id, debit_account_id, journal_id
    ):
        self.ensure_one()
        AccountMove = self.env["account.move"]
        quantity = self.env.context.get("forced_quantity", self.product_qty)
        quantity = quantity if self._is_in() else -1 * quantity
        # Make an informative `ref` on the created account move to differentiate between classic
        # movements, vacuum and edition of past moves.
        ref = (
            self.picking_id
            and self.picking_id.name
            or "%s - %s" % (self.reference, self.product_id.default_code)
        )

        if self.env.context.get("force_valuation_amount"):
            if self.env.context.get("forced_quantity") == 0:
                ref = "Revaluation of %s (negative inventory)" % ref
            elif self.env.context.get("forced_quantity") is not None:
                ref = "Correction of %s (modification of past move)" % ref

        move_lines = self.with_context(forced_ref=ref)._prepare_account_move_line(
            quantity, abs(self.value), credit_account_id, debit_account_id
        )

        if move_lines:
            date = self._context.get(
                "force_period_date", fields.Date.context_today(self)
            )
            new_account_move = AccountMove.sudo().create(
                {
                    "journal_id": journal_id,
                    "line_ids": move_lines,
                    "date": date,
                    "ref": ref,
                    "stock_move_id": self.id,
                }
            )
            new_account_move.post()

    def _run_valuation(self, quantity=None):
        value_to_return = super(StockMove, self)._run_valuation(quantity)

        if self._is_out() and self.consume_unbuild_id:
            move_finished_ids = (
                self.consume_unbuild_id.mo_id.move_finished_ids
                if self.consume_unbuild_id.mo_id
                else []
            )

            for move_finished_id in move_finished_ids:
                if self.product_id == move_finished_id.product_id:
                    value_to_return = (
                        -move_finished_id.price_unit * move_finished_id.product_uom_qty
                    )
                    self.write(
                        {
                            "value": value_to_return,
                            "price_unit": -move_finished_id.price_unit,
                        }
                    )

                    if self.product_id.qty_available > 0:
                        self.product_id.standard_price = (
                            self.product_id.standard_price
                            * (self.product_id.qty_available + self.product_uom_qty)
                            + self.price_unit * self.product_uom_qty
                        ) / self.product_id.qty_available

        return value_to_return
