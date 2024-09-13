# Copyright 2017 Tecnativa - Pedro M. Baeza
# Copyright 2018 EXA Auto Parts S.A.S Guillermo Montoya <Github@guillermm>
# Copyright 2018 EXA Auto Parts S.A.S Joan Marín <Github@JoanMarin>
# Copyright 2020 EXA Auto Parts S.A.S Juan Ocampo <Github@Capriatto>
# Copyright 2021 EXA Auto Parts S.A.S Alejandro Olano <Github@alejo-code>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestConfig(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.wizard = cls.env["res.config.settings"].create({})
        cls.partner = cls.env["res.partner"].create(
            {
                "firstname": "First",
                "othernames": "Other",
                "lastname": "Last",
                "lastname2": "Second",
            }
        )

    def test_last_first(self):
        self.wizard.partner_names_order = "last_first"
        self.wizard.set_values()
        self.wizard.action_recalculate_partners_name()
        self.assertEqual(self.partner.name, "Last Second First Other")

    def test_last_first_comma(self):
        self.wizard.partner_names_order = "last_first_comma"
        self.wizard.set_values()
        self.wizard.action_recalculate_partners_name()
        self.assertEqual(self.partner.name, "Last Second, First Other")

    def test_first_last(self):
        self.wizard.partner_names_order = "first_last"
        self.wizard.set_values()
        self.wizard.action_recalculate_partners_name()
        self.assertEqual(self.partner.name, "First Other Last Second")
