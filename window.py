import gi
import requests
import json
import time
import threading

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib, Pango


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Write Activity")
        self.set_default_size(1000, 800)

        self.paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        self.add(self.paned)

        self.typing_timer = None
        self.last_typing_time = 0

        self.create_textview()
        self.create_sidebar()
        self.create_text_tags()

        self.paned.set_position(int(0.7 * 1000))

    def notification_box(self, widget, data=None):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="INFO",
        )
        dialog.format_secondary_text(data)
        dialog.run()
        print("[LOG]: INFO dialog closed")

        dialog.destroy()

    def apply_highlight(self, start_index, end_index):
        start_iter = self.textbuffer.get_iter_at_offset(start_index)
        end_iter = self.textbuffer.get_iter_at_offset(end_index)

        self.textbuffer.apply_tag_by_name("highlight", start_iter, end_iter)

    def update_sidebar(self, text):
        self.sidebar_buffer.set_text(json.dumps(text, indent=4))

    def handle_response(self, data):
        GLib.idle_add(self.update_sidebar, data)
        for item in data:
            start = item["start"]
            end = item["end"]
            self.apply_highlight(start, end)

    def send_grammar_check_request(self, text):
        try:
            print("[LOG]: Sending request to server")
            GLib.idle_add(self.spinner.start)
            response = requests.post("http://localhost:8000", json={"text": text})
            if response.status_code == 200:
                data = response.json()["message"]
                data = json.loads(data)
                GLib.idle_add(self.handle_response, data)
            else:
                self.notification_box("Server Error")
                print("[LOG]: ERROR Server Error")
        except Exception as e:
            print("[LOG]: ERROR", e)
        finally:
            GLib.idle_add(self.spinner.stop)

    def grammer_check(self, button, textbuffer):
        start_iter = textbuffer.get_start_iter()
        end_iter = textbuffer.get_end_iter()
        text = textbuffer.get_text(start_iter, end_iter, True)

        thread = threading.Thread(target=self.send_grammar_check_request, args=(text,))
        thread.daemon = True
        thread.start()

    def on_text_inserted(self, textbuffer, location, text, length):
        if text == "\n":
            print("[LOG]: Enter key pressed")
            self.grammer_check(self.textview, self.textbuffer)
            return

        print("[LOG]: Text inserted")

        self.last_typing_time = time.time()
        if self.typing_timer:
            GLib.source_remove(self.typing_timer)
        self.typing_timer = GLib.timeout_add(1000, self.detect_stopped_typing)

    def detect_stopped_typing(self):
        if time.time() - self.last_typing_time >= 3:
            print("[LOG]: Typing stopped")
            self.typing_timer = None
            self.grammer_check(self.textview, self.textbuffer)
            return False
        return True

    def create_textview(self):

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)

        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        scrolledwindow.add(self.textview)

        self.paned.pack1(scrolledwindow, True, False)

        self.textbuffer.connect("insert-text", self.on_text_inserted)

    def create_sidebar(self):
        sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.sidebar_label = Gtk.Label(label="Grammar Check Results")
        sidebar_box.pack_start(self.sidebar_label, False, False, 5)

        self.spinner = Gtk.Spinner()
        sidebar_box.pack_start(self.spinner, False, False, 5)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)

        self.sidebar_textview = Gtk.TextView()
        self.sidebar_textview.set_editable(False)
        self.sidebar_textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.sidebar_buffer = self.sidebar_textview.get_buffer()
        scrolledwindow.add(self.sidebar_textview)

        sidebar_box.pack_start(scrolledwindow, True, True, 0)

        self.paned.pack2(sidebar_box, resize=True, shrink=True)

    def create_text_tags(self):
        tag_table = self.textbuffer.get_tag_table()

        tag = Gtk.TextTag.new("highlight")
        tag.set_property("weight", Pango.Weight.BOLD)
        tag.set_property("underline", Pango.Underline.SINGLE)

        tag_table.add(tag)


if __name__ == "__main__":
    win = MainWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
