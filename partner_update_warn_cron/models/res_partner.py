# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import models, fields, api, _
from psycopg2 import sql


class ResPartner(models.Model):
    _inherit = "res.partner"

    not_warn_update_by_cron = fields.Boolean(string="Do not Update Warning by Cron?")

    @api.model
    def cron_update_warn(self):
        for company_id in self.env["res.company"].search([]):
            warn_msg = _("Customer has overdue invoices")
            overdue_days = company_id.overdue_days
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
                    COALESCE(RP.not_warn_update_by_cron, FALSE) != TRUE
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
