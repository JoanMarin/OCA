# Copyright 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# Copyright 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# Copyright 2017 Tecnativa - Pedro M. Baeza
# Copyright 2018 EXA Auto Parts S.A.S Guillermo Montoya <Github@guillermm>
# Copyright 2018 EXA Auto Parts S.A.S Joan Marín <Github@JoanMarin>
# Copyright 2020 EXA Auto Parts S.A.S Juan Ocampo <Github@Capriatto>
# Copyright 2021 EXA Auto Parts S.A.S Alejandro Olano <Github@alejo-code>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.addons.partner_firstname import exceptions


class ResPartner(models.Model):
    """Adds other names."""

    _inherit = "res.partner"

    othernames = fields.Char(string="Other Names")

    @api.model
    def _get_computed_name(self, lastname, firstname, lastname2=None, othernames=None):
        """Compute the name combined with the other names too.

        We have 2 lastnames, so lastnames will be separated by a
        comma from the firstname and the other names.
        """
        order = self._get_names_order()
        names = list()

        if order == "first_last":
            if firstname:
                names.append(firstname)
            if othernames:
                names.append(othernames)
            if lastname:
                names.append(lastname)
            if lastname2:
                names.append(lastname2)
        else:
            if lastname:
                names.append(lastname)
            if lastname2:
                names.append(lastname2)
            if names and (firstname or othernames) and order == "last_first_comma":
                names[-1] = names[-1] + ","
            if firstname:
                names.append(firstname)
            if othernames:
                names.append(othernames)

        return " ".join(names)

    @api.depends("firstname", "othernames", "lastname", "lastname2")
    def _compute_name(self):
        """Write :attr:`~.name` according to splitted data."""
        for partner in self:
            partner.name = self._get_computed_name(
                partner.lastname,
                partner.firstname,
                partner.lastname2,
                partner.othernames,
            )

    @api.model
    def _get_inverse_name(self, name, is_company=False):
        """Compute the inverted name.

        - If the partner is a company, save it in the lastname.
        - Otherwise, make a guess.
        """
        result = {
            "firstname": False,
            "othernames": False,
            "lastname": name or False,
            "lastname2": False,
        }

        # Company name goes to the lastname
        if not name or is_company:
            return result

        order = self._get_names_order()
        result.update(super(ResPartner, self)._get_inverse_name(name, is_company))

        if order == "first_last":
            parts = self._split_part("lastname2", result)

            if parts:
                result.update(
                    {
                        "othernames": result["lastname"],
                        "lastname": parts[0],
                        "lastname2": " ".join(parts[1:]),
                    }
                )
        elif order == "last_first_comma":
            parts = self._split_part("firstname", result)

            if parts:
                result.update(
                    {"firstname": parts[0], "othernames": " ".join(parts[1:])}
                )
        else:
            parts = self._split_part("lastname2", result)

            if parts:
                result.update(
                    {
                        "lastname2": parts[0],
                        "firstname": " ".join(parts[1:]),
                        "othernames": result["firstname"],
                    }
                )

        return result

    @api.constrains("firstname", "othernames", "lastname", "lastname2")
    def _check_name(self):
        """Ensure at least one name is set."""
        try:
            super(ResPartner, self)._check_name()
        except exceptions.EmptyNamesError:
            for partner in self:
                if not partner.othernames:
                    raise
