# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ProductEquivalent(models.Model):
    _name = "product.equivalent"
    _description = "Equivalent Products"

    sku = fields.Char(string="Reference EXA")
    manufacturer_pref = fields.Char(string="Manuf. Product Code", required=True)
    print_to_pdf = fields.Boolean(string="Print to PDF?")
    brand_id = fields.Many2one(
        string="Brand",
        comodel_name="product.brand",
        required=False,
    )
    manufacturer_id = fields.Many2one(
        string="Manufacturer",
        comodel_name="res.partner",
        required=False,
        domain=[("is_manufacturer", "=", True)],
    )
    manufacturer_pname = fields.Char(string="Manuf. Product Name")
    classification_id = fields.Many2one(
        string="Classification of Equivalent Product",
        comodel_name="product.equivalent.classification",
    )
    product_id = fields.Many2one(string="Product", comodel_name="product.product")
    product_template_id = fields.Many2one(
        string="Product Template", comodel_name="product.template"
    )
    product_template_ids = fields.Many2many(
        comodel_name="product.template",
        relation="product_template_product_equivalent_rel",
        column1="product_equivalent_id",
        column2="product_template_id",
        string="Related Products",
    )

    def name_get(self):
        res = []

        for record in self:
            if record.manufacturer_id:
                name = "[%s] %s" % (
                    record.manufacturer_id.name or "",
                    record.manufacturer_pref or "",
                )
            else:
                name = "%s" % (record.manufacturer_pref or "")

            res.append((record.id, name))

        return res

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        args = args or []

        if name:
            args = [
                "|",
                ("sku", operator, name),
                ("manufacturer_pref", operator, name),
            ] + args

        return self.search(args, limit=limit).name_get()

    @api.onchange("product_id")
    def _onchange_product_id(self):
        for record in self:
            record.brand_id = record.product_id.product_tmpl_id.product_brand_id
            record.manufacturer_id = record.product_id.product_tmpl_id.manufacturer_id
            record.manufacturer_pref = (
                record.product_id.product_tmpl_id.manufacturer_pref
            )
            record.manufacturer_pname = (
                record.product_id.product_tmpl_id.manufacturer_pname
            )
            record.product_template_id = record.product_id.product_tmpl_id
