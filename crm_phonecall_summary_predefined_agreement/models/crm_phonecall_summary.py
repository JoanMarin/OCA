# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import models, fields


class CRMPhonecallSummary(models.Model):
    _inherit = "crm.phonecall.summary"

    is_agreement = fields.Boolean(string="Is Agreement?")
