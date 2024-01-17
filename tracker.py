#!/usr/bin/env python
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import pandas as pd

class StockPriceAnalyzer(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Stock Price Analyzer")

        self.set_border_width(10)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        hbox = Gtk.Box(spacing=10)
        vbox.pack_start(hbox, False, False, 0)

        self.file_chooser_button = Gtk.FileChooserButton(title="Select a file")
        self.file_chooser_button.connect("file-set", self.on_file_set)
        hbox.pack_start(self.file_chooser_button, True, True, 0)

        self.analyze_button = Gtk.Button(label="Analyze")
        self.analyze_button.connect("clicked", self.on_analyze_button_clicked)
        hbox.pack_start(self.analyze_button, False, False, 0)

        self.stock_data_label = Gtk.Label()
        vbox.pack_start(self.stock_data_label, False, False, 0)

        self.stock_data_store = Gtk.ListStore(str, str)
        self.stock_data_treeview = Gtk.TreeView(model=self.stock_data_store)

        stock_name_renderer = Gtk.CellRendererText()
        stock_name_column = Gtk.TreeViewColumn("Stock Name", stock_name_renderer, text=0)
        self.stock_data_treeview.append_column(stock_name_column)

        meets_criteria_renderer = Gtk.CellRendererText()
        meets_criteria_column = Gtk.TreeViewColumn("Meets Criteria?", meets_criteria_renderer, text=1)
        self.stock_data_treeview.append_column(meets_criteria_column)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.add(self.stock_data_treeview)
        vbox.pack_start(scrolled_window, True, True, 0)

    def on_file_set(self, button):
        self.file_path = button.get_filename()

    def on_analyze_button_clicked(self, button):
        stock_symbols = []
        with open(self.file_path, "r") as f:
            for line in f:
                stock_symbols.append(line.strip())

        stock_data = pd.DataFrame()
        for symbol in stock_symbols:
            data = pd.read_csv(f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1=0&period2=9999999999&interval=1d&events=history")
            data["Date"] = pd.to_datetime(data["Date"])
            data.set_index("Date", inplace=True)
            data = data.resample("Y").last()
            data["symbol"] = symbol
            stock_data = pd.concat([stock_data, data])

        filtered_data = stock_data.groupby("symbol").apply(lambda x: x["Close"].is_monotonic_increasing)
        filtered_data = filtered_data[filtered_data == True]

        for symbol in stock_symbols:
            meets_criteria = "Yes" if symbol in filtered_data.index else "No"
            self.stock_data_store.append([symbol, meets_criteria])

window = StockPriceAnalyzer()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()

