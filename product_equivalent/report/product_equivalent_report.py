# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools
from psycopg2 import sql


class ProductEquivalentReport(models.Model):
    _name = "product.equivalent.report"
    _description = "Equivalent Products Report"
    _auto = False
    _order = "manufacturer_pref"

    brand_id = fields.Many2one(
        string="Brand", comodel_name="product.brand", readonly=True
    )
    manufacturer_id = fields.Many2one(
        string="Manufacturer", comodel_name="res.partner", readonly=True
    )
    manufacturer_pref = fields.Char(string="Manuf. Product Code", readonly=True)
    manufacturer_pname = fields.Char(string="Manuf. Product Name", readonly=True)
    product_id = fields.Many2one(
        string="Product", comodel_name="product.product", readonly=True
    )
    product_template_id = fields.Many2one(
        string="Product Template", comodel_name="product.template", readonly=True
    )
    parent_product_id = fields.Many2one(
        string="Parent Product", comodel_name="product.product", readonly=True
    )
    parent_product_template_id = fields.Many2one(
        string="Parent Product Template", comodel_name="product.template", readonly=True
    )

    def init(self):
        query = """
            SELECT
                pe.brand_id,
                pe.manufacturer_id,
                pe.manufacturer_pref,
                pe.manufacturer_pname,
                pe.product_id,
                pe.product_template_id,
                pp.id parent_product_id,
                pp.product_tmpl_id parent_product_template_id
            FROM
                product_equivalent pe
                INNER JOIN product_template_product_equivalent_rel ptper ON (pe.id = ptper.product_equivalent_id)
                INNER JOIN product_product pp ON (ptper.product_template_id = pp.product_tmpl_id)
        """
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            sql.SQL("""CREATE or REPLACE VIEW {} as ({})""").format(
                sql.Identifier(self._table), sql.SQL(query)
            )
        )
