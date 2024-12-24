# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import models


class OverdueReminderStart(models.TransientModel):
    _inherit = "overdue.reminder.start"

    def _prepare_reminder_step(
        self,
        commercial_partner,
        base_domain,
        min_interval_date,
        payment_journals,
        sale_journals,
    ):
        vals = super(OverdueReminderStart, self)._prepare_reminder_step(
            commercial_partner,
            base_domain,
            min_interval_date,
            payment_journals,
            sale_journals,
        )

        if vals:
            invoice_ids = self.env["account.invoice"].search(
                base_domain + [("commercial_partner_id", "=", commercial_partner.id)]
            )
            vals["invoice_ids"] = [(6, 0, invoice_ids.ids)]

        return vals

    def run(self):
        action = super(OverdueReminderStart, self).run()

        if self.interface != "validate_all":
            return action

        for reminder_step_id in self.env["overdue.reminder.step"].search(
            [("interface", "=", "validate_all"), ("state", "=", "draft")]
        ):
            reminder_step_id.validate()
