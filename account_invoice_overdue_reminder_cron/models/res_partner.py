# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import models, fields, api, _
from psycopg2 import sql


class ResPartner(models.Model):
    _inherit = "res.partner"

    no_update_warn_by_cron = fields.Boolean(string="Don't update warnings by Cron?")

    @api.model
    def cron_update_warn(self):
        for company_id in self.env["res.company"].search([]):
            warn_msg = _("Customer has overdue invoices")
            overdue_days = company_id.overdue_reminder_start_days
            query = (
                """
                UPDATE
                    res_partner RP
                SET
                    sale_warn = 'block',
                    sale_warn_msg = '{warn_msg}',
                    invoice_warn = 'block',
                    invoice_warn_msg = '{warn_msg}',
                    picking_warn = 'block',
                    picking_warn_msg = '{warn_msg}'
                WHERE
                    COALESCE(RP.no_update_warn_by_cron, FALSE) != TRUE
                    AND RP.invoice_warn = 'no-message'
                    AND RP.id IN (
                        SELECT
                            DISTINCT partner_id
                        FROM
                            account_invoice AI
                        WHERE
                            AI.type = 'out_invoice'
                            AND AI.state = 'open'
                            AND (CURRENT_DATE - AI.date_due) >= {overdue_days}
                    )
                """
            ).format(warn_msg=warn_msg, overdue_days=overdue_days)
            self.env.cr.execute(sql.SQL(query))
            query = (
                """
                UPDATE
                    res_partner RP
                SET
                    sale_warn = 'no-message',
                    sale_warn_msg = NULL,
                    invoice_warn = 'no-message',
                    invoice_warn_msg = NULL,
                    picking_warn = 'no-message',
                    picking_warn_msg = NULL
                WHERE
                    RP.invoice_warn = 'block'
                    AND RP.invoice_warn_msg = '{warn_msg}'
                    AND RP.id NOT IN (
                        SELECT
                            DISTINCT partner_id
                        FROM
                            account_invoice AI
                        WHERE
                            AI.type = 'out_invoice'
                            AND AI.state = 'open'
                            AND (CURRENT_DATE - AI.date_due) >= {overdue_days}
                    )
                """
            ).format(warn_msg=warn_msg, overdue_days=overdue_days)
            self.env.cr.execute(sql.SQL(query))

    @api.model
    def cron_overdue_reminder(self):
        self.env.cr.execute(
            sql.SQL(
                """
                SELECT
                    RP.id
                FROM
                    account_invoice AI,
                    res_partner RP
                WHERE
                    AI.partner_id = RP.id
                    AND RP.email IS NOT NULL
                    AND RP.id NOT IN (
                        SELECT
                            REPLACE(RES_ID, 'res.partner,', '')::INT PARTNER_ID
                        FROM
                            ir_property
                        WHERE
                            NAME = 'no_overdue_reminder'
                            AND VALUE_INTEGER = 1
                    )
                    AND AI.state IN ('open')
                    AND AI.type IN ('out_invoice')
                    AND AI.date_due < CURRENT_DATE
                GROUP BY
                    RP.id
                """
            )
        )
        partner_ids = [row["id"] for row in self.env.cr.dictfetchall()]
        reminder_start_id = self.env["overdue.reminder.start"].create(
            {
                "up_to_date": True,
                "interface": "validate_all",
                "partner_ids": [(6, 0, partner_ids)],
            }
        )
        reminder_start_id.run()
