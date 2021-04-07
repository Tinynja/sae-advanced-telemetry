# Built-in libraries

# Pipy libraries
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# User libraries
from views.custom_widgets import WidgetDict, GridFormLayout, LineEditTable
from views.validators import SoftRegExpValidator


class SettingsUi:
	def __init__(self, dialog):
		self.dialog = dialog

		# Set the dialog window flags
		self.dialog.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)

		# Set the window title
		self.dialog.setWindowTitle('Settings')

		# Create the Ok and cancel buttons and put them in a layout
		self.buttons = {}
		self.buttons['ok'] = QPushButton('OK')
		self.buttons['cancel'] = QPushButton('Cancel')
		buttons_layout = QHBoxLayout()
		buttons_layout.addStretch(1)
		buttons_layout.addWidget(self.buttons['ok'])
		buttons_layout.addWidget(self.buttons['cancel'])

		# Create all the categories
		self.categories = {'Solve (NOMAD)': 'nomad', 'Post-process': 'postprocess', 'Sensitivity matrix': 'sensitivity', 'Export': 'export'}
		for name in self.categories.values():
			getattr(self, '_category_' + name)()
		self._create_tree()
		
		# Create the dialog layout
		dialog_layout = QGridLayout(self.dialog)
		dialog_layout.addWidget(QLabel('Categories:'), 0, 0)
		dialog_layout.addWidget(self.tree, 1, 0)
		# Add all categories to the dialog layout:
		for category in self.categories.values():
			dialog_layout.addWidget(getattr(self, category).widget('scroll'), 0, 1, 2, 1)
		dialog_layout.addLayout(buttons_layout, 2, 0, 1, 2)
		dialog_layout.setRowStretch(1, 1)
		dialog_layout.setColumnStretch(1, 1)

		# Set the minimum width of the window according to its contents to avoid showing a horizontal scroll bar
		# scroll.setMinimumWidth(
		# 	widget.sizeHint().width() +
		# 	scroll.verticalScrollBar().sizeHint().width())
		# self.setMaximumHeight(500)
		# self.resize(0, 300)
		
		self._create_tooltips()

	def _create_tree(self):
		self.tree = QTreeWidget()

		# Set the properties of the tree
		self.tree.setHeaderHidden(True)
		self.tree.setRootIsDecorated(False)
		self.tree.resizeColumnToContents(0)
		
		# Add all the categories to the tree
		for name, attr in self.categories.items():
			self.tree.addTopLevelItem(QTreeWidgetItem(self.tree, (name,)))
			getattr(self, attr).widget('scroll').hide()
			

	def _category_nomad(self):
		self.nomad = WidgetDict()

		# Create the "main" widgets
		self.nomad['scroll'] = QScrollArea()
		self.nomad.widget('scroll').setWidget(QWidget())
		self.nomad.widget('scroll').setWidgetResizable(True)

		# Create the widgets
		self.nomad['mdids_args'] = QLineEdit()
		self.nomad['bb_exe'] = QLineEdit()
		self.nomad['bb_exe-locate'] = QToolButton()
		self.nomad.widget('bb_exe-locate').setIcon(QIcon.fromTheme('document-open'))
		self.nomad['problem_specification'] = QComboBox()
		self.nomad.widget('problem_specification').addItems(('Unknown', 'Fully specified'))
		self.nomad['f_target_quick'] = QLineEdit()
		self.nomad['max_bb_eval_quick'] = QSpinBox()
		self.nomad.widget('max_bb_eval_quick').setMaximum(1e9)
		self.nomad['max_time_quick'] = QSpinBox()
		self.nomad.widget('max_time_quick').setMaximum(31536000)
		self.nomad.widget('max_time_quick').setSuffix('s')
		self.nomad['f_target_full'] = QLineEdit()
		self.nomad['max_bb_eval_full'] = QSpinBox()
		self.nomad.widget('max_bb_eval_full').setMaximum(1e9)
		self.nomad['max_time_full'] = QSpinBox()
		self.nomad.widget('max_time_full').setMaximum(31536000)
		self.nomad.widget('max_time_full').setSuffix('s')
		self.nomad['display_stats'] = QLineEdit()
		self.nomad['display_all_eval'] = QCheckBox()
		self.nomad['display_degree'] = QComboBox()
		self.nomad.widget('display_degree').addItems(('No display (0)', 'Minimal display (1)', 'Normal display (2)', 'Full display (3)'))
		self.nomad['solution_file'] = QLineEdit()
		self.nomad['solution_file-locate'] = QToolButton()
		self.nomad.widget('solution_file-locate').setIcon(QIcon.fromTheme('document-open'))
		self.nomad['history_file'] = QLineEdit()
		self.nomad['history_file-locate'] = QToolButton()
		self.nomad.widget('history_file-locate').setIcon(QIcon.fromTheme('document-open'))
		self.nomad['stats_file'] = QLineEdit()
		self.nomad['stats_file-locate'] = QToolButton()
		self.nomad.widget('stats_file-locate').setIcon(QIcon.fromTheme('document-open'))
		self.nomad['append_enabled'] = QCheckBox()
		self.nomad['append_enabled'] = True
		self.nomad['append'] = LineEditTable(0, 2)
		# self.nomad.widget('append').setFocusRow(False)
		self.nomad.widget('append').setColumnLabels(('Parameter', 'Value'))
		# self.nomad.widget('append').setColumnValidator(0, SoftRegExpValidator('.+'))
		# self.nomad.widget('append').setColumnValidator(1, SoftRegExpValidator('.+'))
		self.nomad['append-add'] = QToolButton()
		self.nomad.widget('append-add').setIcon(QIcon.fromTheme('list-add'))
		self.nomad.widget('append-add').setStyleSheet('border: none')
		self.nomad['append-remove'] = QToolButton()
		self.nomad.widget('append-remove').setIcon(QIcon.fromTheme('list-remove'))
		self.nomad.widget('append-remove').setStyleSheet('border: none')
		self.nomad.widget('append-remove').setEnabled(False)
		self.nomad['custom_enabled'] = QCheckBox()
		self.nomad['custom_enabled'] = True
		self.nomad['custom'] = QTextEdit()
		self.nomad['custom-clear'] = QToolButton()
		self.nomad.widget('custom-clear').setIcon(QIcon.fromTheme('edit-clear'))
		self.nomad.widget('custom-clear').setStyleSheet('border: none')

		# Create the "append parameters" layout
		append_layout = QHBoxLayout()
		append_table_group = QFrame()
		append_table_group.setFrameStyle(QFrame.Box)
		append_layout_table = QVBoxLayout(append_table_group)
		append_layout_table.addWidget(self.nomad.widget('append'))
		append_layout_table.addStretch(1)
		append_layout_side = QVBoxLayout()
		append_layout_side.addWidget(self.nomad.widget('append-add'))
		append_layout_side.addWidget(self.nomad.widget('append-remove'))
		append_layout_side.addStretch(1)
		append_layout.addWidget(append_table_group)
		append_layout.addLayout(append_layout_side)

		# Create the "custom parameters" layout
		custom_layout = QHBoxLayout()
		custom_layout_side = QVBoxLayout()
		custom_layout_side.addWidget(self.nomad.widget('custom-clear'))
		custom_layout_side.addStretch(1)
		custom_layout.addWidget(self.nomad.widget('custom'))
		custom_layout.addLayout(custom_layout_side)

		layout = GridFormLayout(self.nomad.widget('scroll').widget())
		# Add widgets to the layout
		layout.addRow('MDIDSGTconsole arguments:', self.nomad.widget('mdids_args'))
		layout.addRow('Blackbox path:', self.nomad.widget('bb_exe'))
		layout.addRow('Problem specification:', self.nomad.widget('problem_specification'))
		layout.addRow('Solution accuracy (Quick):', self.nomad.widget('f_target_quick'))
		layout.addRow('Maximum evaluations (Quick):', self.nomad.widget('max_bb_eval_quick'))
		layout.addRow('Maximum time (Quick):', self.nomad.widget('max_time_quick'))
		layout.addRow('Solution accuracy (Full):', self.nomad.widget('f_target_full'))
		layout.addRow('Maximum evaluations (Full):', self.nomad.widget('max_bb_eval_full'))
		layout.addRow('Maximum time (Full):', self.nomad.widget('max_time_full'))
		layout.addRow('Display format:', self.nomad.widget('display_stats'))
		layout.addRow('Display all evaluations:', self.nomad.widget('display_all_eval'))
		layout.addRow('Display degree:', self.nomad.widget('display_degree'))
		layout.addRow('Solution file path:', self.nomad.widget('solution_file'))
		layout.addRow('History file path:', self.nomad.widget('history_file'))
		layout.addRow('Display log path:', self.nomad.widget('stats_file'))
		layout.addRow('Use appended parameters:', self.nomad.widget('append_enabled'))
		layout.addRow(append_layout)
		layout.addRow('Use custom parameters file:', self.nomad.widget('custom_enabled'))
		layout.addRow(custom_layout)
		layout.setColumnStretch(1, 1)

	def _category_postprocess(self):
		self.postprocess = WidgetDict()

		# Create the "main" widgets
		self.postprocess['scroll'] = QScrollArea()
		self.postprocess.widget('scroll').setWidget(QWidget())
		self.postprocess.widget('scroll').setWidgetResizable(True)

		# Create the widgets
		self.postprocess['placeholder'] = QLineEdit()

		layout = GridFormLayout(self.postprocess.widget('scroll').widget())
		# Add widgets to the layout
		layout.addRow('[PLACEHOLDER]', self.postprocess.widget('placeholder'))
		layout.setColumnStretch(1, 1)

	def _category_sensitivity(self):
		self.sensitivity = WidgetDict()

		# Create the "main" widgets
		self.sensitivity['scroll'] = QScrollArea()
		self.sensitivity.widget('scroll').setWidget(QWidget())
		self.sensitivity.widget('scroll').setWidgetResizable(True)

		# Create the widgets
		self.sensitivity['placeholder'] = QLineEdit()

		layout = GridFormLayout(self.sensitivity.widget('scroll').widget())
		# Add widgets to the layout
		layout.addRow('[PLACEHOLDER]', self.sensitivity.widget('placeholder'))
		layout.setColumnStretch(1, 1)

	def _category_export(self):
		self.export = WidgetDict()

		# Create the "main" widgets
		self.export['scroll'] = QScrollArea()
		self.export.widget('scroll').setWidget(QWidget())
		self.export.widget('scroll').setWidgetResizable(True)

		# Create the widgets
		self.export['placeholder'] = QLineEdit()

		layout = GridFormLayout(self.export.widget('scroll').widget())
		# Add widgets to the layout
		layout.addRow('[PLACEHOLDER]', self.export.widget('placeholder'))
		layout.setColumnStretch(1, 1)

	def _create_tooltips(self):
		pass