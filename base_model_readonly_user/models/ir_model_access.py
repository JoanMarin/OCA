# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import api, models


class IrModelAccess(models.Model):
    _inherit = "ir.model.access"

    @api.model
    def check(self, model, mode="read", raise_exception=True):
        if self.check_groups("base_model_readonly_user.group_readonly_user"):
            if mode != "read":
                return False

        return super(IrModelAccess, self).check(model, mode, raise_exception)
