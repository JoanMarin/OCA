# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = "account.move"

    service_order_line_ids = fields.One2many(
        compute="_compute_service_order_ids",
        comodel_name="account.move.line",
        string="Journal Items",
    )
    duca = fields.Char(string="No. DUCA", compute="_compute_service_order_ids")
    dmti = fields.Char(string="No. DMTI", compute="_compute_service_order_ids")
    dm = fields.Char(string="No. DM", compute="_compute_service_order_ids")
    sv = fields.Char(string="No. SV", compute="_compute_service_order_ids")
    bl = fields.Char(string="No. BL", compute="_compute_service_order_ids")
    awb = fields.Char(string="No. AWB", compute="_compute_service_order_ids")
    cp = fields.Char(string="No. CP", compute="_compute_service_order_ids")

    def _compute_service_order_ids(self):
        for move_id in self:
            service_order_ids = move_id.line_ids.mapped("service_order_id")
            move_id.duca = ", ".join(service_order_ids.mapped("duca"))
            move_id.dmti = ", ".join(service_order_ids.mapped("dmti"))
            move_id.dm = ", ".join(service_order_ids.mapped("dm"))
            move_id.sv = ", ".join(service_order_ids.mapped("sv"))
            move_id.bl = ", ".join(service_order_ids.mapped("bl"))
            move_id.awb = ", ".join(service_order_ids.mapped("awb"))
            move_id.cp = ", ".join(service_order_ids.mapped("cp"))
            move_line_ids = service_order_ids.mapped("move_line_ids")
            move_id.service_order_line_ids = move_line_ids
