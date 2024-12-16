# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_non_territorial = fields.Boolean(string="Is Non-territorial?", default=False)
