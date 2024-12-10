# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_application_id = fields.Many2one(
        comodel_name="product.application", string="Application"
    )
    application_category_id = fields.Many2one(
        comodel_name="product.application.category",
        string="Category",
        domain=[("parent_id", "=", False)],
    )
    application_subcategory_id = fields.Many2one(
        comodel_name="product.application.category", string="Subcategory"
    )
    application_segment_id = fields.Many2one(
        comodel_name="product.application.category", string="Segment"
    )

    @api.onchange("application_category_id")
    def _onchange_application_category_id(self):
        self.application_subcategory_id = False
        self.application_segment_id = False

    @api.onchange("application_subcategory_id")
    def _onchange_application_subcategory_id(self):
        self.application_segment_id = False

    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)

        if (
            vals.get("product_application_id")
            or vals.get("application_category_id")
            or vals.get("application_subcategory_id")
            or vals.get("application_segment_id")
        ):
            if not self.env.user.has_group(
                "product_application.group_product_application_user"
            ):
                raise UserError(
                    _("You can not modify applications or product categories.")
                )

        return res
