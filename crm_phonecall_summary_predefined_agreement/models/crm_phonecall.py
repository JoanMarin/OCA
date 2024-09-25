# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import models, fields


class CRMPhonecall(models.Model):
    _inherit = "crm.phonecall"

    is_agreement = fields.Boolean(related="summary_id.is_agreement")
    agreement_date = fields.Date()
    agreement_amount = fields.Float()
