import gi
import requests
import re

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def parse_string(input_string):
    pattern = re.compile(r"\[sentence: (.*?), correct_sentence: (.*?), reason: (.*?)\]")

    match = pattern.search(input_string)

    if match:
        return {
            "sentence": match.group(1),
            "correct_sentence": match.group(2),
            "reason": match.group(3),
        }
    return None


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Write Activity")
        self.set_default_size(800, 600)
        self.grid = Gtk.Grid()
        self.add(self.grid)

    def notification_box(self, widget, data):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="INFO",
        )
        dialog.format_secondary_text(data)
        dialog.run()
        print("INFO dialog closed")

        dialog.destroy()

    def on_button_clicked(self, button, textbuffer):
        start_iter = textbuffer.get_start_iter()
        end_iter = textbuffer.get_end_iter()
        text = textbuffer.get_text(start_iter, end_iter, True)

        response = requests.post("http://localhost:8000", json={"text": text})

        if response.status_code == 200:
            result = response.json()["message"]
            if result == "ok":
                self.notification_box(button, "All sentences are correct")
                return
            parsed_result = parse_string(result)
            if parsed_result:
                formated_text = ""
                for key, value in parsed_result.items():
                    formated_text += f"{key}: {value}\n"
                self.notification_box(button, formated_text)
                textbuffer.set_text(parsed_result["correct_sentence"])
        else:
            self.notification_box(button, "Error occurred")

    def create_toolbar(self):
        toolbar = Gtk.Toolbar()
        self.grid.attach(toolbar, 0, 0, 3, 1)

        button = Gtk.ToolButton()
        button.set_label("Check Grammer")
        button.connect("clicked", self.on_button_clicked, self.textbuffer)
        toolbar.insert(button, 0)

    def create_textview(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.grid.attach(scrolledwindow, 0, 1, 3, 1)

        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        scrolledwindow.add(self.textview)


win = MainWindow()
win.create_textview()
win.create_toolbar()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
