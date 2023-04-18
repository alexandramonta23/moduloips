# import string
# from odoo import api, models, fields
# from odoo.exceptions import UserError, ValidationError

# class asignar(models.Model):
# 	_name = 'asignar.ip'
# 	_description = 'Asignar ips a dispositivos'

# 	# @api.onchange('nom_dispo')
# 	# def onchange_partner_id(self):
# 	# 	for rec in self:
# 	# 		return {'domain': {'ip_disp': [('dispositivo_asig', '=', rec.nom_dispo.dispositivo_asig)]}}

# 	usuario = fields.Many2one('usuario.gestiondirecciones',string="Usuario",required=True)
# 	nom_dispo = fields.Many2one('dispositivo.gestiondirecciones',string="Dispositivo")
# 	ip_disp = fields.Many2one('control.gestiondirecciones' ,string="IP del Dispositivo", related='nom_dispo.ip', tracking=True, readonly=True)

# 	obs = fields.Text(string="Observaciones")

# ===================================================
# acceso_asignar,asignar.ip,model_asignar_ip,,1,1,1,1
# ===================================================
