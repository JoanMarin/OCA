# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import api, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def recalculate_taxes(self, remove_tax_group_ids, taxes):
        """Updates taxes on all order lines"""
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

        if set(self.taxes_id.ids) != set(taxes_ids):
            self.update({"taxes_id": [(6, 0, set(taxes_ids))]})

        return True

    @api.multi
    def _compute_tax_id(self):
        super(PurchaseOrderLine, self)._compute_tax_id()
        remove_tax_group_ids = []
        order_id = False

        for line_id in self:
            if not order_id:
                order_id = line_id.order_id
                remove_tax_group_ids = order_id.get_remove_tax_group_ids()

            line_id.recalculate_taxes(remove_tax_group_ids, line_id.taxes_id)
