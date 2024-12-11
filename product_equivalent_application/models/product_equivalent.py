# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ProductEquivalent(models.Model):
    _inherit = "product.equivalent"

    application_category_id = fields.Many2one(
        comodel_name="product.application.category",
        string="Category",
        domain=[("parent_id", "=", False)],
    )
    application_subcategory_id = fields.Many2one(
        comodel_name="product.application.category", string="Subcategory"
    )

    @api.onchange("product_id")
    def _onchange_product_id(self):
        super(ProductEquivalent, self)._onchange_product_id()

        for record in self:
            record.application_category_id = (
                record.product_id.product_tmpl_id.application_category_id
            )
            record.application_subcategory_id = (
                record.product_id.product_tmpl_id.application_subcategory_id
            )
