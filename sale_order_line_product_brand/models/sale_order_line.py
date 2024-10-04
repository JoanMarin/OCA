# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_brand_id = fields.Many2one(related="product_id.product_brand_id")
