# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).
from odoo import models, api, _


class ResCompany(models.Model):
    _inherit = "res.company"

    @api.model
    def _overdue_reminder_interface_selection(self):
        selection = super(ResCompany, self)._overdue_reminder_interface_selection()
        selection.append(("validate_all", _("Validate All")))

        return selection
