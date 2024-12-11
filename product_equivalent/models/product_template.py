# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    sku = fields.Char(
        string="Reference EXA",
        compute="_compute_sku",
        inverse="_set_sku",
        store=True,
    )
    product_equivalent_ids = fields.Many2many(
        comodel_name="product.equivalent",
        relation="product_template_product_equivalent_rel",
        column1="product_template_id",
        column2="product_equivalent_id",
        string="Equivalent Products",
    )

    @api.depends("product_variant_ids", "product_variant_ids.sku")
    def _compute_sku(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in unique_variants:
            template.sku = template.product_variant_ids.sku
        for template in self - unique_variants:
            template.sku = False

    @api.one
    def _set_sku(self):
        if len(self.product_variant_ids) == 1:
            self.product_variant_ids.sku = self.sku

    @api.onchange("product_brand_id")
    def _onchange_product_brand_id(self):
        for record in self:
            if record.product_brand_id.partner_id:
                record.manufacturer = record.product_brand_id.partner_id
