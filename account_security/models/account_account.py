# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import models, fields, _
from odoo.exceptions import UserError


class AccountAccount(models.Model):
    _inherit = "account.account"

    active = fields.Boolean(default=True)

    def toggle_active(self):
        if not self.env.user.has_group("account.group_account_manager"):
            raise UserError(_("You can't archive accounts"))

        return super(AccountAccount, self).toggle_active()
