# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ProductEquivalentClassification(models.Model):
    _name = "product.equivalent.classification"
    _description = "Classification of Equivalent Products"

    code = fields.Char(string="Code", required=True)
    name = fields.Char(string="Name", required=True)
    system_id = fields.Integer(string="System ID", required=True)
    system_name = fields.Char(string="System Name", required=True)
    subsystem_id = fields.Integer(string="Subsystem ID", required=True)
    subsystem_name = fields.Char(string="Subsystem Name", required=True)

    def name_get(self):
        res = []

        for record in self:
            if record.code:
                name = "[%s] %s" % (record.code or "", record.name or "")
            else:
                name = "%s" % (record.name or "")

            res.append((record.id, name))

        return res

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        args = args or []

        if name:
            args = ["|", ("code", operator, name), ("name", operator, name)] + args

        return self.search(args, limit=limit).name_get()
