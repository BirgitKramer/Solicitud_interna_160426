# -*- coding: utf-8 -*-
{
    "name": "Solicitud Internas",
    "version": "19.0.1.0.0",
    "summary": "Gestion de solicitudes internas (IT, RRHH, Compras)",
    "description": """
        Modulo para gestionar solicitudes internas de la empresa.
        Permite registrar y dar seguimiento a solicitudes de:
        - IT (Soporte tecnico, falhas, nuevos equipos)
        - RRHH (Vacaciones, permisos, nominas)
        - Compras (Solicitudes de compra, requisiciones)
    """,
    "category": "Generic",
    "author": "Tu Empresa",
    "website": "https://tuempresa.com",
    "license": "LGPL-3",
    "depends": ["base", "mail"],
    "data": [
        "data/secuencia.xml",
        "security/ir.model.access.csv",
        "views/solicitud_menu.xml",
        "views/solicitud_views.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
