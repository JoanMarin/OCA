# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import models, fields, api, _
from psycopg2 import sql


class ResPartner(models.Model):
    _inherit = "res.partner"

    warn_updated_by_cron = fields.Boolean(string="Warning Updated By Cron?")

    @api.model
    def cron_update_warn(self):
        for company_id in self.env["res.company"].search([]):
            overdue_days = company_id.overdue_days
            query = (
                """
                UPDATE
                    res_partner RP
                SET
                    warn_updated_by_cron = TRUE,
                    invoice_warn = 'block',
                    invoice_warn_msg = '{invoice_warn_msg}'
                WHERE
                    COALESCE(RP.warn_updated_by_cron, FALSE) != TRUE
                    AND COALESCE(RP.invoice_warn, '') != 'block'
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
            ).format(
                invoice_warn_msg=_("Customer has overdue invoices"),
                overdue_days=overdue_days,
            )
            self.env.cr.execute(sql.SQL(query))
            query = (
                """
                UPDATE
                    res_partner RP
                SET
                    warn_updated_by_cron = FALSE,
                    invoice_warn = 'no-message',
                    invoice_warn_msg = NULL
                WHERE
                    RP.warn_updated_by_cron = TRUE
                    AND RP.invoice_warn = 'block'
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
            ).format(overdue_days=overdue_days)
            self.env.cr.execute(sql.SQL(query))
