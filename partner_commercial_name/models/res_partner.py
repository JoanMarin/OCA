# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).


from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    commercial_name = fields.Char(
        string="Commercial Name", placeholder="Commercial Name"
    )

    def name_get(self):
        res = []

        for record in super(ResPartner, self).name_get():
            partner_id = self.env["res.partner"].browse(record[0])
            name = record[1]

            if partner_id.commercial_name:
                name = "[%s] %s" % (partner_id.commercial_name, name)

            res.append((partner_id.id, name))

        return res

    @api.depends(
        "is_company",
        "name",
        "parent_id.name",
        "type",
        "company_name",
        "commercial_name",
    )
    def _compute_display_name(self):
        return super(ResPartner, self)._compute_display_name()
