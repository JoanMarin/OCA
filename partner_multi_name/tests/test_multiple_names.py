# Copyright 2024 EXA Auto Parts S.A.S Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestMultipleNames(TransactionCase):
    def assert_name(self, config_settings, partner, vals, order, expected_name):
        config_settings.partner_names_order = order
        config_settings.action_recalculate_partners_name()
        vals["name"] = expected_name
        self.assertRecordValues(partner, [vals])
        copy_partner = partner.copy()
        self.assertEqual(copy_partner.name, f"{partner.name} (copy)")

    def test_recalculate_names(self):
        firstname = "Xavier"
        othernames = "De Jesús"
        lastname = "Payen"
        lastname2 = "Sandoval"
        vals = {
            "firstname": firstname,
            "othernames": othernames,
            "lastname": lastname,
            "lastname2": lastname2,
        }
        partner = self.env["res.partner"].create(vals)
        config_settings = self.env["res.config.settings"].create({})

        self.assert_name(
            config_settings,
            partner,
            vals,
            "first_last",
            f"{firstname} {othernames} {lastname} {lastname2}",
        )
        self.assert_name(
            config_settings,
            partner,
            vals,
            "last_first",
            f"{lastname} {lastname2} {firstname} {othernames}",
        )
        self.assert_name(
            config_settings,
            partner,
            vals,
            "last_first_comma",
            f"{lastname} {lastname2}, {firstname} {othernames}",
        )
