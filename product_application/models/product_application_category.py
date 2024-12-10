# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import models, fields


class ProductApplicationsCategory(models.Model):
    _name = "product.application.category"
    _description = "Product Application Categories"
    _parent_store = True

    code = fields.Char(string="Code")
    name = fields.Char(string="Name", translate=True, required=True)
    parent_id = fields.Many2one(
        comodel_name="product.application.category",
        string="Parent Category",
        ondelete="restrict",
    )
    child_ids = fields.One2many(
        comodel_name="product.application.category",
        inverse_name="parent_id",
        string="Subcategories",
    )
    parent_path = fields.Char(index=True)
