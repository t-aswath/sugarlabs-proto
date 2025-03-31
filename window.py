import gi
import requests
import time
import threading
from enum import Enum

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib, Pango


class Level(Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3


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
        self.load_css()

        self.paned.set_position(int(0.55 * 1000))

        self.suggestions = {}
        self.level = Level.HIGH
        self.lvlmp = {
            "high": "red",
            "medium": "yellow",
            "low": "green",
        }

    def load_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(
            b"""
            .red {
                background-color: #FDAB9E;
            }
            .yellow {
                background-color: #FFF0BD;
            }
            .green {
                background-color: #C7DB9C;
            }
            .text{
                color: #000000;
                padding: 10px;
            }
        """
        )

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def level_state_handler(self, button, level):
        self.level = level

    def replace_text(self, widget, event, index):
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 1:
            item = self.suggestions[index]

            start_iter = self.textbuffer.get_iter_at_mark(item["start"])
            end_iter = self.textbuffer.get_iter_at_mark(item["end"])

            self.textbuffer.delete(start_iter, end_iter)
            self.textbuffer.insert(start_iter, item["correct"])

            start_iter = self.textbuffer.get_iter_at_mark(item["start"])
            end_iter = self.textbuffer.get_iter_at_mark(item["end"])

            self.textbuffer.remove_tag_by_name("highlight", start_iter, end_iter)

            widget.destroy()
            if index in self.suggestions:
                del self.suggestions[index]

    def apply_highlight(self, item):
        start_iter = self.textbuffer.get_iter_at_mark(item["start"])
        end_iter = self.textbuffer.get_iter_at_mark(item["end"])
        self.textbuffer.apply_tag_by_name("highlight", start_iter, end_iter)

    def update_sidebar(self, item, index):
        label = Gtk.Label(
            label=f"Original: {item["sentence"]}\n\nCorrected: {item["correct"]}\n\nReason: {item["reason"]}\n"
        )
        label.set_xalign(0)
        label.set_justify(Gtk.Justification.LEFT)
        label.set_line_wrap(True)
        label.get_style_context().add_class("text")

        frame = Gtk.Frame()
        frame.set_shadow_type(Gtk.ShadowType.OUT)
        frame.set_margin_start(10)
        frame.set_margin_end(10)
        frame.set_hexpand(True)
        frame.get_style_context().add_class(self.lvlmp[item["importance"].lower()])
        frame.add(label)

        event_box = Gtk.EventBox()
        event_box.add(frame)
        event_box.connect("button-press-event", self.replace_text, index)

        return event_box

    def clear_prev_results(self):
        self.textbuffer.remove_all_tags(
            self.textbuffer.get_start_iter(), self.textbuffer.get_end_iter()
        )

        self.suggestions = {}

        for child in self.scrolledwindow.get_children():
            self.scrolledwindow.remove(child)

    def handle_response(self, data):
        self.clear_prev_results()

        self.container_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.container_box.set_halign(Gtk.Align.FILL)
        self.container_box.set_hexpand(True)

        for index, item in enumerate(data["suggestions"]):

            if item["importance"] == "none":
                continue

            start_iter = self.textbuffer.get_start_iter()

            match = start_iter.forward_search(
                item["sentence"], Gtk.TextSearchFlags.TEXT_ONLY, None
            )
            if match:
                item["start"], item["end"] = match
                item["start"] = self.textbuffer.create_mark(None, item["start"], True)
                item["end"] = self.textbuffer.create_mark(None, item["end"], False)

                self.apply_highlight(item)
                self.container_box.pack_start(
                    self.update_sidebar(item, index), False, False, 2
                )
                self.suggestions[index] = item

        self.scrolledwindow.add(self.container_box)
        self.scrolledwindow.show_all()

    def send_grammar_check_request(self, text):
        try:
            print("[LOG]: Sending request to server")
            GLib.idle_add(self.spinner.start)
            response = requests.post(
                "http://localhost:8000/chain",
                json={"text": text, "level": self.level.name.lower()},
            )
            if response.status_code == 200:
                data = response.json()
                GLib.idle_add(self.handle_response, data)
            else:
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
        print("[LOG]: Text inserted")

        self.last_typing_time = time.time()
        if self.typing_timer:
            GLib.source_remove(self.typing_timer)
        self.typing_timer = GLib.timeout_add(1000, self.detect_stopped_typing)

    def detect_stopped_typing(self):
        if time.time() - self.last_typing_time >= 5:
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
        sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        self.sidebar_label = Gtk.Label(label="Grammar Check Results")
        sidebar_box.pack_start(self.sidebar_label, False, False, 5)

        self.spinner = Gtk.Spinner()
        sidebar_box.pack_start(self.spinner, False, False, 5)

        button_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.button_high = Gtk.Button.new_with_mnemonic("_High")
        self.button_medium = Gtk.Button.new_with_mnemonic("_Medium")
        self.button_low = Gtk.Button.new_with_mnemonic("_Low")

        self.button_high.connect("clicked", self.level_state_handler, Level.HIGH)
        self.button_medium.connect("clicked", self.level_state_handler, Level.MEDIUM)
        self.button_low.connect("clicked", self.level_state_handler, Level.LOW)

        button_container.pack_start(self.button_high, True, True, 0)
        button_container.pack_start(self.button_medium, True, True, 0)
        button_container.pack_start(self.button_low, True, True, 0)

        sidebar_box.pack_start(button_container, False, False, 0)

        self.scrolledwindow = Gtk.ScrolledWindow()
        self.scrolledwindow.set_hexpand(True)
        self.scrolledwindow.set_vexpand(True)

        sidebar_box.pack_start(self.scrolledwindow, True, True, 0)

        self.paned.pack2(sidebar_box, resize=True, shrink=False)

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
