# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import fields, models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    is_split_pdf = fields.Boolean("Split By PDF?")
