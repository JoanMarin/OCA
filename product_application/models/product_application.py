# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import models, fields


class ProductApplications(models.Model):
    _name = "product.application"
    _description = "Product Applications"

    code = fields.Char(string="Code")
    name = fields.Char(string="Name", translate=True, required=True)
