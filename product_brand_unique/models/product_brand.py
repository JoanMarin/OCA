# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, _


class ProductBrand(models.Model):
    _inherit = "product.brand"

    _sql_constraints = [
        ("name_unique", "UNIQUE(name)", _("Brand name must be unique!")),
    ]
