# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SolicitudInterna(models.Model):
    _name = "solicitud.interna"
    _description = "Solicitud Interna"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Número de Solicitud",
        required=True,
        copy=False,
        readonly=True,
        index="trigram",
        default=lambda self: self._generate_name(),
    )
    state = fields.Selection(
        [
            ("borrador", "Borrador"),
            ("enviada", "Enviada"),
            ("en_revision", "En Revisión"),
            ("aprobada", "Aprobada"),
            ("rechazada", "Rechazada"),
            ("proceso", "En Proceso"),
            ("finalizada", "Finalizada"),
            ("cancelada", "Cancelada"),
        ],
        string="Estado",
        default="borrador",
        tracking=True,
    )

    fecha_solicitud = fields.Datetime(
        string="Fecha de Solicitud", default=fields.Datetime.now, required=True
    )
    fecha_necesaria = fields.Date(string="Fecha Necesaria")
    fecha_respuesta = fields.Datetime(string="Fecha de Respuesta", readonly=True)

    tipo = fields.Selection(
        [
            ("it", "IT"),
            ("rrhh", "RRHH"),
            ("compras", "Compras"),
        ],
        string="Tipo de Solicitud",
        required=True,
        tracking=True,
    )

    prioridad = fields.Selection(
        [
            ("baja", "Baja"),
            ("normal", "Normal"),
            ("alta", "Alta"),
            ("urgente", "Urgente"),
        ],
        string="Prioridad",
        default="normal",
        tracking=True,
    )

    solicitante_id = fields.Many2one(
        "res.users",
        string="Solicitante",
        default=lambda self: self.env.user,
        required=True,
    )
    departamento_id = fields.Many2one("hr.department", string="Departamento")

    asignada_id = fields.Many2one("res.users", string="Asignado a", tracking=True)
    company_id = fields.Many2one(
        "res.company", string="Empresa", default=lambda self: self.env.company
    )

    titulo = fields.Char(string="Título", required=True)
    descripcion = fields.Text(string="Descripción")
    solucion = fields.Text(string="Solución/Respuesta")
    notas_internas = fields.Text(string="Notas Internas")

    category_id = fields.Many2one("solicitud.interna.category", string="Categoría")
    parent_id = fields.Many2one("solicitud.interna", string="Solicitud Padre")

    @api.model
    def _generate_name(self):
        seq = self.env["ir.sequence"].next_by_code("solicitud.interna")
        return seq or "/"

    def action_enviar(self):
        self.write({"state": "enviada"})

    def action_revisar(self):
        self.write({"state": "en_revision", "fecha_respuesta": fields.Datetime.now()})

    def action_aprobar(self):
        self.write({"state": "aprobada"})

    def action_rechazar(self):
        self.write({"state": "rechazada", "fecha_respuesta": fields.Datetime.now()})

    def action_procesar(self):
        self.write({"state": "proceso"})

    def action_finalizar(self):
        self.write({"state": "finalizada", "fecha_respuesta": fields.Datetime.now()})

    def action_cancelar(self):
        self.write({"state": "cancelada"})

    def action_reabrir(self):
        self.write({"state": "borrador", "fecha_respuesta": False})


class SolicitudCategoria(models.Model):
    _name = "solicitud.interna.category"
    _description = "Categoría de Solicitud"

    name = fields.Char(string="Nombre", required=True)
    tipo = fields.Selection(
        [
            ("it", "IT"),
            ("rrhh", "RRHH"),
            ("compras", "Compras"),
        ],
        string="Tipo",
        required=True,
    )
    description = fields.Text(string="Descripción")
    active = fields.Boolean(default=True)
