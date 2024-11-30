# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import fields, models, api


class ResPartnerEmail(models.Model):
    _name = "res.partner.email"
    _description = "Multiple Emails"

    name = fields.Char(string="Email", required=True)
    is_main = fields.Boolean(string="Is Main?", default=False)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Contact")

    def name_get(self):
        res = []

        for record in self:
            name = "%s" % (record.name or "")
            res.append((record.id, name))

        return res

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        if not args:
            args = []

        if name:
            state = self.search([("name", operator, name)] + args, limit=limit)
        else:
            state = self.search([], limit=limit)

        return state.name_get()
