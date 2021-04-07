# Pipy libraries
from PyQt5.QtWidgets import *

# User libraries
from views.settings_ui import SettingsUi
from views.custom_widgets import LineEditTable, MultiNameButton


class SettingsView(QDialog):
	def __init__(self, model, category=0, parent=None):
		super().__init__(parent)

		# MVC compononents
		self._model = model
		self._ui = SettingsUi(self)

		# Connect all signals
		self._connect_signals()

		# Set the current category
		self._ui.tree.setCurrentItem(self._ui.tree.topLevelItem(category))

	
	def _connect_signals(self):
		# Connect behavior widgets
		self._ui.buttons['ok'].clicked.connect(lambda: self.accept())
		self._ui.buttons['cancel'].clicked.connect(lambda: self.reject())
		self._ui.tree.currentItemChanged.connect(self.on_category_change)

		# Connect model signals
		self._model.propertyChanged.connect(self.on_propertyChanged)
		self._model.propertyInserted.connect(self.on_propertyInserted)
		self._model.propertyRemoved.connect(self.on_propertyRemoved)

		# Nomad widgets
		self._ui.nomad.widget('append-add').clicked.connect(lambda: self._model.insert_property('nomad', 'append', ['', '']))
		self._ui.nomad.widget('append-remove').clicked.connect(lambda: self._model.remove_property('nomad', 'append', index=self._ui.nomad.widget('append')._lastfocusrow))
		self._ui.nomad.widget('custom-clear').clicked.connect(lambda: self._model.set_property('nomad', 'custom', ''))

		# Connect the property widgets to their respecting model properties
		for group in self._ui.categories.values():
			for prop, widget in getattr(self._ui, group).items():
				if isinstance(widget, QLineEdit):
					widget.textEdited.connect(lambda text, group=group, prop=prop: self._model.set_property(group, prop, text))
				elif isinstance(widget, QCheckBox):
					widget.clicked.connect(lambda state, group=group, prop=prop: self._model.set_property(group, prop, state))
				elif isinstance(widget, MultiNameButton):
					widget.clickedState.connect(lambda state, group=group, prop=prop: self._model.set_property(group, prop, state))
				elif isinstance(widget, QComboBox):
					widget.activated.connect(lambda index, group=group, prop=prop: self._model.set_property(group, prop, index))
				elif isinstance(widget, QSpinBox):
					widget.valueChanged.connect(lambda value, group=group, prop=prop: self._model.set_property(group, prop, value))
				elif isinstance(widget, LineEditTable):
					widget.textEdited.connect(lambda row, col, text, group=group, prop=prop: self._model.set_property(group, prop, row, col, text))
				self._set_special_behavior(group, prop)
	

	"""Slots"""
	def on_category_change(self, current, previous):
		if previous:
			getattr(self._ui, self._ui.categories[previous.text(0)]).widget('scroll').hide()
		getattr(self._ui, self._ui.categories[current.text(0)]).widget('scroll').show()

	def on_propertyChanged(self, args):
		if args[:2] == ('nomad', 'append'):
			self._ui.nomad.widget('append').setValue(args[-3], args[-2], args[-1])
		else:
			getattr(self._ui, args[0])[args[1]] = args[2]
	
	def on_propertyInserted(self, args):
		if args[:2] == ('nomad', 'append'):
			self._ui.nomad.widget('append').insertRow(args[-1])
			self._ui.nomad.widget('append').setRowValues(args[-1], args[-2])
	
	def on_propertyRemoved(self, args):
		if args[:2] == ('nomad', 'append'):
			self._ui.nomad.widget('append').removeFocusedRow()

	
	"""Special behavior widgets"""
	def _set_special_behavior(self, *args):
		function_name = '_special_' + '_'.join(args).replace('-','_')
		# Call the appropriate special behavior function if it exists
		if hasattr(self, function_name):
			getattr(self, function_name)(*args)
	
	def _special_nomad_append_enabled(self, *args):
		def __on_nomad_append_enabled(state):
			self._ui.nomad.widget('append').setEnabled(state)
			self._ui.nomad.widget('append-add').setEnabled(state)
			self._ui.nomad.widget('append-remove').setEnabled(state and bool(self._ui.nomad.widget('append').countRows()))
		self._ui.nomad.widget('append_enabled').stateChanged.connect(__on_nomad_append_enabled)
	
	def _special_nomad_append(self, *args):
		def __on_nomad_append(*args):
			self._ui.nomad.widget('append-remove').setEnabled(
				self._ui.nomad['append_enabled']
				and bool(self._ui.nomad.widget('append').countRows())
				and all([False if v is None else True for v in self._ui.nomad.widget('append').currentFocus()]))
		self._ui.nomad.widget('append').rowAdded.connect(lambda: __on_nomad_append())
		self._ui.nomad.widget('append').rowRemoved.connect(lambda: __on_nomad_append())
		self._ui.nomad.widget('append').focused.connect(lambda: __on_nomad_append())
	
	def _special_nomad_custom_enabled(self, *args):
		def __on_nomad_custom_enabled(state):
			self._ui.nomad.widget('custom').setEnabled(state)
			self._ui.nomad.widget('custom-clear').setEnabled(state)
		self._ui.nomad.widget('custom_enabled').stateChanged.connect(__on_nomad_custom_enabled)

	def _special_nomad_custom(self, *args):
		def __on_nomad_custom():
			self._ui.nomad.widget('custom').blockSignals(True)
			self._model.set_property('nomad', 'custom', self._ui.nomad['custom'])
			self._ui.nomad.widget('custom').blockSignals(False)
		self._ui.nomad.widget('custom').textChanged.connect(__on_nomad_custom)