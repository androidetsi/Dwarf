"""
Dwarf - Copyright (C) 2018 iGio90

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>
"""
from PyQt5.QtCore import Qt

from ui.widget_context import ContextItem
from ui.widget_item_not_editable import NotEditableTableWidgetItem
from ui.widget_memory_address import MemoryAddressWidget
from ui.widget_table_base import TableBaseWidget


class ContextsPanel(TableBaseWidget):
    def __init__(self, app, *__args):
        super().__init__(app, 0, 3)

        self.setHorizontalHeaderLabels(['tid', 'pc', 'symbol'])
        self.horizontalHeader().setStretchLastSection(True)

    def add_context(self, data, library_onload=None):
        row = self.rowCount()
        self.insertRow(row)
        q = ContextItem(data, str(data['tid']))
        q.setForeground(Qt.darkCyan)
        self.setItem(row, 0, q)
        is_java = data['is_java']
        if not is_java:
            q = MemoryAddressWidget(data['ptr'])
        else:
            parts = data['ptr'].split('.')
            q = NotEditableTableWidgetItem(parts[len(parts) - 1])
            q.setForeground(Qt.red)
            q.setFlags(Qt.NoItemFlags)
        self.setItem(row, 1, q)
        if library_onload is None:
            if not is_java:
                q = NotEditableTableWidgetItem('%s - %s' % (
                    data['symbol']['moduleName'], data['symbol']['name']))
            else:
                q = NotEditableTableWidgetItem('.'.join(parts[:len(parts) - 1]))
        else:
            q = NotEditableTableWidgetItem('loading %s' % library_onload)

        q.setFlags(Qt.NoItemFlags)
        q.setForeground(Qt.gray)
        self.setItem(row, 2, q)
        self.resizeRowsToContents()
        self.horizontalHeader().setStretchLastSection(True)

    def item_double_clicked(self, item):
        if isinstance(item, ContextItem):
            self.app.apply_context(item.get_context())
            return False
        return True
