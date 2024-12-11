# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = "product.product"

    sku = fields.Char(string="Reference EXA", index="True")

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        res = super(ProductProduct, self).name_search(name, args, operator, limit)

        if name:
            args = [
                "|",
                "|",
                "|",
                ("manufacturer_pref", operator, name),
                ("sku", operator, name),
                ("product_equivalent_ids", operator, name),
                ('id', 'in', [x[0] for x in res])
            ]

            return self.search(args, limit=limit).name_get()

        return res
