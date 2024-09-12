# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import api, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    def recalculate_taxes(self, remove_tax_group_ids, taxes):
        """Updates taxes on all invoice lines"""
        taxes_ids = taxes.ids

        for tax in taxes:
            remove_tax_parent = False

            if tax.amount_type == "group":
                children_taxes_ids = [i.id for i in tax.children_tax_ids]

                for children_tax in tax.children_tax_ids:
                    for tax_group_id in remove_tax_group_ids:
                        if children_tax.tax_group_id == tax_group_id:
                            children_taxes_ids.remove(children_tax.id)
                            remove_tax_parent = True
                            break

                if children_taxes_ids and remove_tax_parent:
                    taxes_ids += children_taxes_ids
                elif children_taxes_ids and not remove_tax_parent:
                    for children_tax_id in children_taxes_ids:
                        if children_tax_id in taxes_ids:
                            taxes_ids.remove(children_tax_id)

            for tax_group_id in remove_tax_group_ids:
                if tax.tax_group_id == tax_group_id or remove_tax_parent:
                    if tax.id in taxes_ids:
                        taxes_ids.remove(tax.id)

        if set(self.invoice_line_tax_ids.ids) != set(taxes_ids):
            self.update({"invoice_line_tax_ids": [(6, 0, set(taxes_ids))]})

        return True

    @api.multi
    def _compute_tax_id(self):
        fiscal_position_id = False

        for line_id in self:
            if not line_id.product_id:
                continue

            company_id = line_id.company_id or self.env.user.company_id

            if line_id.invoice_id.type in ("out_invoice", "out_refund"):
                taxes = (
                    line_id.product_id.taxes_id.filtered(
                        lambda r: r.company_id == company_id
                    )
                    or line_id.account_id.tax_ids
                    or company_id.account_sale_tax_id
                )
            else:
                taxes = (
                    line_id.product_id.supplier_taxes_id.filtered(
                        lambda r: r.company_id == company_id
                    )
                    or line_id.account_id.tax_ids
                    or company_id.account_purchase_tax_id
                )

            if not fiscal_position_id:
                fiscal_position_id = (
                    line_id.invoice_id.fiscal_position_id
                    or line_id.invoice_id.partner_id.property_account_position_id
                )

            line_id.invoice_line_tax_ids = fiscal_position_id.map_tax(
                taxes, line_id.product_id, line_id.invoice_id.partner_id
            )

        remove_tax_group_ids = []
        invoice_id = False

        for line_id in self:
            if not invoice_id:
                invoice_id = line_id.invoice_id
                remove_tax_group_ids = invoice_id.get_remove_tax_group_ids()

            line_id.recalculate_taxes(
                remove_tax_group_ids, line_id.invoice_line_tax_ids
            )
