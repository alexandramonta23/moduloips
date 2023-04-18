# -*- coding: utf-8 -*-
{
    'name': "gestiondirecciones",

    'summary': """
        Módulo para el control de asignación  de ips""",

    'description': """
        EL presente módulo 
    """,

    'author': "David Valdiviezo ft. Cristhian Velez",
    'website': " ",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'AGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/menusyacciones.xml',
        'views/control_gestiondirecciones.xml',
        'views/usuario_gestiondirecciones.xml',
        'views/vlan_gestionvlan.xml',
        'views/ip_gestiondirecciones.xml',
        'views/direccion_gestiondirecciones.xml',
        'views/switch_gestiondirecciones.xml',
        'views/puerto_gestiondirecciones.xml',
        'views/dispositivo_gestiondirecciones.xml',
        'views/reporte.xml',
        'views/reporte_num_ip_utilizadas_vlan.xml',
        'views/reporte_num_ip_utilizadas_vlan.xml',
        'views/reporte_dispositivos_con_ip.xml',
        # 'views/asignar_ip.xml',

    ],

}
