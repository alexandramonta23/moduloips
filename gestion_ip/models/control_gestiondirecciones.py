import string
from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError

class control(models.Model):
	_name = 'control.gestiondirecciones'
	_description = 'Control de usuarios e ip'

	h_d = fields.Selection([('hostname','Hostname'), ('dispositivo','Dispositivo')], default='hostname', string="Agregar")

	cod_usuario = fields.Many2one('usuario.gestiondirecciones',string="Hostname")
	dispositivo_asig = fields.Many2one('dispositivo.gestiondirecciones',string="Dispositivo")
	piso = fields.Many2one('switch.gestiondirecciones',string="Piso", required=True) #required=True
	asignar_puerto = fields.Many2one('puerto.gestiondirecciones',string="Asignar Puerto")
	vlan_asig = fields.Many2one('vlan.gestionvlan',string="Vlan", required=True) #required=True
	cod_ip = fields.Many2one('ip.gestiondirecciones',string="Ip", required=True) #required=True
	observaciones = fields.Text(string="Observaciones")

	usuario_host = fields.Char(string="Usuario del Hostname", related='cod_usuario.usuario', tracking=True)
	funcionario = fields.Text(string="Funcionario", related='cod_usuario.apellidos_nombres', tracking=True)
	# ext = fields.Char(string="Ext", related='cod_usuario.ext_telefonica', tracking=True) ELIMINAR ESTA LINEA DE CÓDIGO
	# ext2 = fields.Char(string="Ext2") ELIMINAR ESTA LINEA DE CÓDIGO
	num_switch = fields.Char(string="Número Switch", related='piso.name', readonly=True)
	ip_switch_swtch = fields.Char(string="IP Switch", related='piso.ip_switch', readonly=True)
	puert_disp_switch = fields.Char(string="Puertos Disponibles", related='piso.puert_disponibles', readonly=True)
	
	vlan_o = fields.Char(string="Vlan que sirve", related='vlan_asig.name', readonly=False)
	ip = fields.Char(string="IP", related='cod_ip.ip', tracking=True, readonly=False)
	# Estas variables se crean para guardar automaticamente lo que escriben en los campos 
    # de arriba, ya que si queremos utilizarlos directamente no se puede
	obtener_hostname = fields.Char(string="Host")
	obtener_numero_switch = fields.Char(string="Num Switch")
	
	# Función para retornar las IP's que esten disponibles e inactivas de cada Vlan 
	# seleccionada dentro del campo "cod_ip"
	@api.onchange('vlan_asig')
	def onchange_partner_id(self):
		for rec in self:
			return {'domain': {'cod_ip': ['|',('disponible2', '=', 'disponible'),('disponible2', '=', 'inactivo'),('vlan_otro', '=', rec.vlan_o)]}}

	# Función para retornar los puertos que esten libres de cada switch en el campo "asignar_puerto"
	@api.onchange('piso')
	def conseguir_puertos_disponibles(self):
		for rec in self:
			rec.obtener_numero_switch = rec.num_switch
			return {'domain': {'asignar_puerto': [('estado_puerto', '=', 'libre'), ('id_switch_2', '=', rec.obtener_numero_switch)]}}

	# Funcion para cambiar el estado de un puerto (de "libre" a "ocupado") al momento de 
	# asignar o guardar una IP como registro final
	@api.constrains('asignar_puerto')
	def _verificar_puerto(self):
		for record in self:
			record.asignar_puerto.hostname_del_usuario = record.obtener_hostname

			if record.asignar_puerto.estado_puerto == 'libre':
				record.asignar_puerto.estado_puerto = 'ocupado'
				
	# Función para guardar lo que contiene "cod_usuario.name" en "obtener_hostname"
	@api.onchange('cod_usuario')
	def obtener_host(self):
		for rec in self:
			rec.obtener_hostname = rec.cod_usuario.name

	# Funcion para cambiar el estado de un puerto (de "disponible" a "asignada") al momento de 
	# asignar o guardar una IP como registro final
	@api.constrains('cod_ip')
	def _verificar_estado(self):
		for record in self:
			# record.cod_usuario.ext_telefonica = record.ext2 #asdfasdfadsfasdfasdfasfasdf ELIMINAR ESTA LINEA DE CÓDIGO
			if record.cod_ip.disponible2 == 'disponible':
				record.cod_ip.disponible2 = 'asignada'

	# Esta Función hace lo siguiente al momento de eliminar un regstro de este modelo "control.gestiondirecciones"
	# 1. Cambiar el estado de una IP (de "asignada" a "inactiva") 
	# 2. Cambiar el estado de un puerto (de "ocupado" a "libre")
	# 3. Poner en blanco el campo "asignar_puerto.hostname_del_usuario"
	def unlink(self):
		for record in self:
			record.cod_ip.disponible2 = 'inactivo' #inactivo
			record.asignar_puerto.estado_puerto = 'libre'
			record.asignar_puerto.hostname_del_usuario = ' '
		return super(control, self).unlink()

	# OJO ===============================================
	# def name_get(self):
	# 	result = []
	# 	for record in self:
	# 		name = record.dispositivo_asig
	# 		result.append((record.id, name))
	# 	return result

	# CÓDIGO QUE PUEDE SER ÚTIL
	# @api.model_create_multi
    # @api.model
	# def create(self, vals):
	# 	for i in vals:
	# 		datos = [
    #             {'hostname_del_usuario':i['obtener_hostname']} 
    #         ]
	# 		self.env['puerto.gestiondirecciones'].create(datos)
	# 	return super(control, self).create(vals)

	# @api.depends('cod_ip')
	# def _compute_is_approval(self):
	# 	for rec in self:
	# 		rec.cod_ip.disponible2 = 'asignada'

	# @api.model
	# def create(self, vals):
	# 	self.env['ip.gestiondirecciones'].update({'disponible2':'asignada'})
	# 	return super(control, self).create(vals)

	#funcion para al momento de eliminar un registro poner el campo "Activo" 
	# del modelo "ip.gestiondirecciones" en "si"

	# @api.constrains('cod_ip')
	# def _verificar_registro(self):
	# 	for record in self:
	# 		# if record.cod_ip.name == self.ip:
	# 		if record.cod_ip.name == self.ip:
	# 			raise ValidationError("La IP ya esta en uso")

	# Funcion para evitar ingresar datos repetidos en el campo "ip"
	# @api.constrains('ip')
	# def _verificar_registro(self):
	# 	for record in self:
	# 		if record.ip:
	# 			register = self.env['control.gestiondirecciones'].search([['ip', '=', record.ip]])
	# 			if register:
	# 				for r in register:
	# 					if r.id != record.id:
	# 						raise ValidationError('La IP ya esta en uso!')

	# @api.constrains('cod_ip')
	# def _verificar_registro(self):
	# 	contact = ['control.gestiondirecciones']
	# 	for c in contact:
	# 		if c.vlan_asig == self.ip:
	# 			raise Warning('la identificación debe ser unica!')

	# @api.constrains('cod_ip')
	# def _verificar_registro(self):
	# 	for record in self:
	# 		# if record.cod_ip.name == self.ip:
	# 		if record.cod_ip.name == self.ip:
	# 			raise ValidationError("La IP ya esta en uso")

	# @api.model
	# def default_get(self, fields):
	# 	res = super()

	# 	if record.vat:
	#   contact = env['res.partner'].search([['vat', '=', record.vat]])
  
	#   if contact:
	#     for c in contact:
	#       if c.id != record.id:
	#         raise Warning('la identificación debe ser unica!')	

	# def leyenda(self):
	# 	num = 10
	# 	return num

	# def print_report(self):
	# 	data={
    #         'cod_usuario': self.cod_usuario,
    #         'cod_ip': self.cod_ip,
    #         'observaciones': self.observaciones,
    #             }

	# 	return self.env.ref('report_custom_template').report_action(self, data=data)

	# @api.onchange('cod_ip')
	# def onchange_partner_id(self):
	# 	for rec in self:
	# 		return {'domain': {'vlan_asig': [('cod_ip', '=', rec.cod_ip.id)]}}

	