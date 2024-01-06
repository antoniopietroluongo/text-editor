import json
from ctypes import windll
from tkinter import messagebox
import tkinter
import tkinter.filedialog
import tkinter.scrolledtext
import sys
import os
import tkinter.font
import subprocess

windll.shcore.SetProcessDpiAwareness(1)


class TextEditor:
    def __init__(self):
        self.cwd = (os.getcwd())
        try:
            with open(self.cwd + "/.config.json", "r") as f:
                self.config = json.load(f)
        except:
            self.config = {"geometry": "1006x464", "font": "Consolas", "size": 10}

        self.size = self.config["size"]
        self._window = tkinter.Tk()
        self._window.title("Untitled")
        self._window.geometry(self.config["geometry"])
        self._window.bind("<Configure>", self._set_geometry)
        self._window.bind("<Control-Shift-N>", self._new_file)
        self._window.bind("<Control-Shift-O>", self._open_file)
        self._window.bind("<Control-Shift-S>", self._save_file)
        self._window.bind("<F1>", self._show_info)
        self._window.bind("<Control-Shift-R>", self._reset_geometry)
        self._window.bind("<Control-Shift-r>", self._reset_geometry)
        self._window.grid_columnconfigure(0, weight=1)
        self._window.grid_rowconfigure(0, weight=1)
        self._text = tkinter.scrolledtext.ScrolledText(self._window, undo=True, wrap=tkinter.WORD)
        self._text.configure(font=(self.config["font"], self.size))
        self._text.focus_set()
        self._text.bind("<Button-3>", self._show_context_menu)
        self._text.bind("<Control-Z>", self._undo)
        self._text.bind("<Control-Shift-Z>", self._redo)
        self._text.bind("<Control-X>", self._cut)
        self._text.bind("<Control-C>", self._copy)
        self._text.bind("<Control-V>", self._paste)
        self._text.bind("<Cancel>", self._delete)
        self._text.bind("<Control-A>", self._select_all)
        self._text.bind("<Control-a>", self._select_all)
        self._text.grid(row=0, column=0, sticky="nsew")
        self._var = tkinter.BooleanVar()
        self.menu_bar = tkinter.Menu(self._window)
        self.file_menu = tkinter.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", accelerator="Ctrl+Shift+N", command=self._new_file)
        self.file_menu.add_command(label="Open...", accelerator="Ctrl+Shift+O", command=self._open_file)
        self.file_menu.add_command(label="Save", accelerator="Ctrl+Shift+S", command=self._save_file)
        self.file_menu.add_command(label="Save as...", command=self._save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", accelerator="Alt+F4", command=self._exit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.edit_menu = tkinter.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=self._undo)
        self.edit_menu.add_command(label="Redo", accelerator="Ctrl+Shift+Z", command=self._redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=self._cut)
        self.edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=self._copy)
        self.edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=self._paste)
        self.edit_menu.add_command(label="Delete", accelerator="Canc", command=self._delete)
        self.edit_menu.add_command(label="Select all", accelerator="Ctrl+A", command=self._select_all)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.view_menu = tkinter.Menu(self.menu_bar, tearoff=0)
        self.view_menu.add_checkbutton(label="Always on top", command=self._always_on_top, variable=self._var)
        self.view_menu.add_command(label="Open in Notepad", command=self._open_in, state="disabled")
        self.view_menu.add_command(label="Increase font size", accelerator="Ctrl+Plus",
                                   command=self._increase_font_size)
        self.view_menu.add_command(label="Decrease font size", accelerator="Ctrl+Minus",
                                   command=self._decrease_font_size)
        self.view_menu.add_command(label="Reset font size", accelerator="Ctrl+0", command=self._reset_font_size)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
        self.help_menu = tkinter.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About", accelerator="F1", command=self._show_info)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self._window.config(menu=self.menu_bar)
        self._window.protocol("WM_DELETE_WINDOW", self._exit)
        self._fpath = None
        self._window.bind("<Control-plus>", self._increase_font_size)
        self._window.bind("<Control-minus>", self._decrease_font_size)
        self._window.bind("<Control-0>", self._reset_font_size)

    def _reset_font_size(self, event=None):
        self.size = 10
        self.config["size"] = self.size
        self._text.configure(font=(self.config["font"], self.size))

    def _increase_font_size(self, event=None):
        if self.size < 28:
            self.size += 1
            self.config["size"] = self.size
            self._text.configure(font=(self.config["font"], self.size))

    def _decrease_font_size(self, event=None):
        if self.size > 5:
            self.size -= 1
            self.config["size"] = self.size
            self._text.configure(font=(self.config["font"], self.size))

    def _reset_geometry(self, event):
        self._window.geometry("1006x464")

    def _open_in(self):
        try:
            subprocess.Popen(["notepad.exe", self._fpath])
        except:
            pass

    def _always_on_top(self):
        if self._var.get():
            self._window.attributes("-topmost", "True")
        else:
            self._window.attributes("-topmost", "False")

    def _set_geometry(self, event):
        self.config["geometry"] = self._window.geometry()

    def _new_file(self, event=None):
        if len(sys.argv) > 1:
            sys.argv = [sys.argv[0]]
        if self._text.edit_modified() == 0:
            self._text.delete("1.0", "end")
            self._text.configure(font=(self.config["font"], self.size))
            self._window.title("Untitled")
            self._fpath = None
            self._text.edit_modified(0)
            self.view_menu.entryconfig("Open in Notepad", state="disabled")
        else:
            a = messagebox.askyesnocancel("Save", "Do you want to save changes?")
            if a == True:
                self._save_file()
                if self._text.edit_modified() == 0:
                    self._text.delete("1.0", "end")
                    self._text.configure(font=(self.config["font"], self.size))
                    self._window.title("Untitled")
                    self._fpath = None
                    self._text.edit_modified(0)
            elif a == False:
                self._text.delete("1.0", "end")
                self._text.configure(font=(self.config["font"], self.size))
                self._window.title("Untitled")
                self._fpath = None
                self._text.edit_modified(0)
            elif a == None:
                pass

    def _open_file(self, event=None):
        if self._text.edit_modified():
            a = messagebox.askyesnocancel("Save", "Do you want to save changes?")
            if a == True:
                self._save_file()
                if self._text.edit_modified() == 0:
                    self._open()
            elif a == False:
                self._open()
            elif a == None:
                pass
        else:
            self._open()

    def _open(self):
        path = tkinter.filedialog.askopenfilename(title="Choose a file",
                                                  filetypes=[("Text documents", "*.txt"), ("All files", "*.*")])
        if path:
            if len(sys.argv) > 1:
                sys.argv = [sys.argv[0]]
            self._text.delete("1.0", "end")
            with open(path) as f:
                self._text.insert("1.0", f.read())
                self._text.configure(font=(self.config["font"], self.size))
            self._window.title(path)
            self._fpath = path
            self._text.edit_modified(0)
            self.view_menu.entryconfig("Open in Notepad", state="normal")

    def _save_file_as(self):
        path = tkinter.filedialog.asksaveasfilename(title="Save as",
                                                    filetypes=[("Text documents", "*.txt"),
                                                               ("All files", "*.*")],
                                                    defaultextension=".txt")
        if path:
            if len(sys.argv) > 1:
                sys.argv = [sys.argv[0]]
            with open(path, "w", encoding="utf-8") as f:
                f.write(self._text.get("1.0", "end-1c"))
            self._window.title(path)
            self._fpath = path
            self._text.edit_modified(0)

    def _save_file(self, event=None):
        if len(sys.argv) > 1:
            with open(sys.argv[1], "w", encoding="utf-8") as f:
                f.write(self._text.get("1.0", "end-1c"))
            sys.argv = [sys.argv[0]]
            self._text.edit_modified(0)
        elif self._fpath == None:
            self._save_file_as()
        else:
            with open(self._fpath, "w", encoding="utf-8") as f:
                f.write(self._text.get("1.0", "end-1c"))
            self._text.edit_modified(0)

    def _undo(self, event=None):
        try:
            self._text.edit_undo()
        except Exception:
            pass

    def _redo(self, event=None):
        try:
            self._text.edit_redo()
        except Exception:
            pass

    def _copy(self, event=None):
        try:
            self._window.clipboard_clear()
            self._window.clipboard_append(self._text.get("sel.first", "sel.last"))
        except Exception:
            pass

    def _cut(self, event=None):
        try:
            self._copy()
            self._text.delete("sel.first", "sel.last")
        except Exception:
            pass

    def _paste(self, event=None):
        try:

            if self._text.tag_ranges("sel"):
                self._text.delete("sel.first", "sel.last")
            self._text.insert("insert", self._window.selection_get(selection="CLIPBOARD"))
        except Exception:
            pass

    def _select_all(self, event=None):
        self._text.tag_add("sel", "1.0", "end")
        return "break"

    def _delete(self, event=None):
        try:
            self._text.delete("sel.first", "sel.last")
        except Exception:
            pass

    def _show_context_menu(self, event):
        context_menu = tkinter.Menu(None, tearoff=0)
        context_menu.add_command(label="Cut", command=self._cut)
        context_menu.add_command(label="Copy", command=self._copy)
        context_menu.add_command(label="Paste", command=self._paste)
        context_menu.add_command(label="Delete", command=self._delete)
        context_menu.add_command(label="Select all", command=self._select_all)
        context_menu.tk_popup(event.x_root, event.y_root, entry="")

    def _exit(self, event=None):
        if self._text.edit_modified() == 0:
            with open(self.cwd + "/.config.json", "w") as f:
                json.dump(self.config, f)
            self._window.destroy()
        else:
            a = messagebox.askyesnocancel("Save", "Do you want to save changes?")
            if a == True:
                self._save_file()
                with open(self.cwd + "/.config.json", "w") as f:
                    json.dump(self.config, f)
                if len(sys.argv) > 1:
                    self._window.destroy()
                if self._fpath:
                    self._window.destroy()
            elif a == False:
                with open(self.cwd + "/.config.json", "w") as f:
                    json.dump(self.config, f)
                self._window.destroy()
            elif a == None:
                pass

    def _show_info(self, event=None):
        tkinter.messagebox.showinfo("About", "\n".join(["Version: 1.00", "Author: Antonio Pietroluongo"]))

    def open_with(self, p):
        with open(p, encoding="utf-8") as f:
            self._text.insert("1.0", f.read())
        self._text.edit_modified(0)
        self._fpath = p
        self._window.title(p)

    def show_window(self):
        self._window.mainloop()


if __name__ == '__main__':
    text_editor = TextEditor()
    if len(sys.argv) > 1:
        text_editor.open_with(sys.argv[1])
    text_editor.show_window()
