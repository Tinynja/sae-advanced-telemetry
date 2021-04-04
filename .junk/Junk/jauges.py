		#Jauge du voltage de l'avion mère (6*4.2=25.2V)
		
		self.volt_Avion = AnalogGaugeWidget()
		#self.volt_Avion.update_value(5)
		self.volt_Avion.value_min=0
		self.volt_Avion.value_max=nb_cell_avion*4.2
		jauges.addWidget(self.volt_Avion, 1, 0)

		#Jauge du voltage de la télémétrie (2*4.2=8.4V max)
		nb_cell_tel=2
		self.volt_telem = AnalogGaugeWidget()
		#self.volt_telem.update_value(5)
		self.volt_telem.value_min=0
		self.volt_telem.value_max=nb_cell_tel*4.2

		jauges.addWidget(self.volt_telem, 2, 0)