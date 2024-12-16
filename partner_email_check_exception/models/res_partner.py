# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import models, api, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.constrains("email")
    def _check_email_unique(self):
        if self._should_filter_duplicates():
            for rec in self.filtered("email"):
                email_exception_obj = self.env["res.partner.email.exception"]
                email_exceptions = email_exception_obj.search([]).mapped("name")

                if self.search_count(
                    [
                        ("email", "=", rec.email),
                        ("id", "!=", rec.id),
                        ("email", "!=", False),
                        ("email", "not in", email_exceptions),
                    ]
                ):
                    raise UserError(
                        _("Email '%s' is already in use.") % rec.email.strip()
                    )
