# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class MrpUnbuild(models.Model):
    _inherit = "mrp.unbuild"

    def _generate_move_from_raw_moves(self, raw_move, factor):
        move_id = super(MrpUnbuild, self)._generate_move_from_raw_moves(
            raw_move, factor
        )
        move_id.write({"price_unit": -raw_move.price_unit})

        return move_id
