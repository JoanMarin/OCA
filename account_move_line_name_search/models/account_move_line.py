# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import api, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        args = args or []

        if name:
            args = [
                "|",
                "|",
                ("name", operator, name),
                ("ref", operator, name),
                ("move_id.name", operator, name),
            ] + args

        return self.search(args, limit=limit).name_get()
