# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import models
from odoo.tools import float_compare


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

    def _set_taxes(self):
        for line_id in self:
            super(AccountInvoiceLine, line_id)._set_taxes()

        remove_tax_group_ids = []
        invoice_id = False

        for line_id in self:
            if not invoice_id:
                invoice_id = line_id.invoice_id
                remove_tax_group_ids = invoice_id.get_remove_tax_group_ids()

            taxes = line_id.invoice_line_tax_ids
            line_id.recalculate_taxes(remove_tax_group_ids, taxes)
            new_taxes = line_id.invoice_line_tax_ids

            if taxes == new_taxes:
                return

            fix_price = line_id.env["account.tax"]._fix_tax_included_price

            if invoice_id.type in ("in_invoice", "in_refund"):
                prec = self.env["decimal.precision"].precision_get("Product Price")
                if (
                    not line_id.price_unit
                    or float_compare(
                        line_id.price_unit,
                        line_id.product_id.standard_price,
                        precision_digits=prec,
                    )
                    == 0
                ):
                    line_id.price_unit = fix_price(
                        line_id.product_id.standard_price, taxes, new_taxes
                    )
                    line_id._set_currency()
            else:
                line_id.price_unit = fix_price(
                    line_id.product_id.lst_price, taxes, new_taxes
                )
                line_id._set_currency()
