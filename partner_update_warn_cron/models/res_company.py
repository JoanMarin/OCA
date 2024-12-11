# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    overdue_days = fields.Integer(default=30)
