# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

MSG = _("There can only be one main email.")


class ResPartner(models.Model):
    _inherit = "res.partner"

    email_ids = fields.One2many(
        comodel_name="res.partner.email", inverse_name="partner_id", string="Emails"
    )

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        res = super(ResPartner, self).name_search(name, args, operator, limit)

        if name:
            args = [
                "|",
                ("email_ids", operator, name),
                ("id", "in", [x[0] for x in res]),
            ]

            return self.search(args, limit=limit).name_get()

        return res

    def write(self, vals):
        res = super(ResPartner, self).write(vals)

        if not vals.get("email_ids"):
            return res

        for partner_id in self:
            main_emails = []

            for email_id in partner_id.email_ids:
                if email_id.is_main:
                    main_emails.append(email_id.name)

            if len(main_emails) > 1:
                raise ValidationError(MSG)
            elif len(main_emails) == 1 and partner_id.email != main_emails[0]:
                partner_id.email = main_emails[0]
            elif len(main_emails) == 0 and len(partner_id.email_ids) > 0:
                partner_id.email_ids[0].is_main = True
                partner_id.email = partner_id.email_ids[0].name

        return res

    @api.model
    def create(self, vals):
        rec = super(ResPartner, self).create(vals)

        if not vals.get("email_ids"):
            return rec

        for partner_id in rec:
            main_emails = [
                email_id.name for email_id in partner_id.email_ids if email_id.is_main
            ]

            if len(main_emails) > 1:
                raise ValidationError(MSG)
            elif len(main_emails) == 1 and partner_id.email != main_emails[0]:
                partner_id.email = main_emails[0]
            elif len(main_emails) == 0 and partner_id.email_ids:
                partner_id.email_ids[0].is_main = True
                partner_id.email = partner_id.email_ids[0].name

        return rec
