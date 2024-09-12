# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class AccountMoveLineSetServiceOrder(models.TransientModel):
    _name = "account.move.line.set.service.order"
    _description = "Set Service Order"

    service_order_id = fields.Many2one(
        comodel_name="account.service.order",
        string="Service Order",
        domain="[('state', '=', 'open')]",
    )

    def set_service_order_id(self):
        account_move_obj = self.env["account.move"]

        for wizard_id in self:
            move_id = account_move_obj.browse(self.env.context.get("active_id", False))

            for line_id in move_id.line_ids.filtered(
                lambda r: r.is_service_order_account
            ):
                if (
                    line_id.has_service_order != "no"
                    and not line_id.service_order_id
                    and line_id.partner_id == wizard_id.service_order_id.partner_id
                ):
                    line_id.write(
                        {
                            "service_order_id": wizard_id.service_order_id.id,
                            "has_service_order": "yes",
                        }
                    )

        return {"type": "ir.actions.act_window_close"}
