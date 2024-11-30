# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import models, fields


class PartnerEmailException(models.Model):
    _name = "res.partner.email.exception"
    _description = "Email Exceptions"

    name = fields.Char(string="Email", required=True)
