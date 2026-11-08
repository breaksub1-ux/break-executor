import json
import tkinter as tk
import tkinter.font as tkfont
from tkinter import filedialog, messagebox, simpledialog
from pathlib import Path

APP_NAME = "BREAK EXECUTOR"
APP_VERSION = "2.0"
DATA_DIR = Path.home() / "BreakExecutor"
SCRIPTS_DIR = DATA_DIR / "scripts"
CONFIG_FILE = DATA_DIR / "config.json"

BG = "#090b12"
PANEL = "#111624"
PANEL2 = "#171f30"
TEXT = "#e8f0ff"
MUTED = "#91a0bb"
ACCENT = "#00e5ff"
PINK = "#ff36b8"
GREEN = "#55f2a5"
DEFAULT_CONFIG = {"username": "admin", "password": "1234"}


def ensure_data():
    """Create the application folders and recover safely from a bad config file."""
    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    try:
        if CONFIG_FILE.exists():
            config = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            if not isinstance(config, dict):
                raise ValueError("configuração inválida")
            username = str(config.get("username", "")).strip()
            password = str(config.get("password", ""))
            if username and password:
                return {"username": username, "password": password}
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError):
        pass

    CONFIG_FILE.write_text(json.dumps(DEFAULT_CONFIG, indent=2), encoding="utf-8")
    return DEFAULT_CONFIG.copy()


class BreakExecutor:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("1120x720")
        self.root.minsize(900, 600)
        self.root.configure(bg=BG)
        self.root.option_add("*Font", self.ui_font(10))
        self.config = ensure_data()
        self.current_file = None
        self.draft_text = None
        self.rgb_index = 0
        self.rgb_after_id = None
        self.build_login()

    def ui_font(self, size, weight="normal"):
        return tkfont.Font(root=self.root, family="Segoe UI", size=size, weight=weight)

    def clear(self):
        if self.rgb_after_id is not None:
            try:
                self.root.after_cancel(self.rgb_after_id)
            except tk.TclError:
                pass
            self.rgb_after_id = None
        for widget in self.root.winfo_children():
            widget.destroy()

    def build_login(self):
        self.clear()
        wrap = tk.Frame(self.root, bg=BG)
        wrap.place(relx=.5, rely=.5, anchor="center")
        tk.Label(wrap, text="BREAK", fg=ACCENT, bg=BG, font=self.ui_font(34, "bold")).pack()
        tk.Label(wrap, text="EXECUTOR", fg=TEXT, bg=BG, font=self.ui_font(18, "bold")).pack(pady=(0, 22))
        card = tk.Frame(wrap, bg=PANEL, padx=28, pady=26, highlightthickness=1, highlightbackground=ACCENT)
        card.pack()
        tk.Label(card, text="ENTRAR NO PAINEL", fg=TEXT, bg=PANEL, font=self.ui_font(12, "bold")).pack(anchor="w", pady=(0, 14))
        tk.Label(card, text="Usuário", fg=MUTED, bg=PANEL).pack(anchor="w")
        self.user_entry = tk.Entry(card, width=32, bg=PANEL2, fg=TEXT, insertbackground=TEXT, relief="flat")
        self.user_entry.pack(ipady=9, pady=(4, 12))
        tk.Label(card, text="Senha", fg=MUTED, bg=PANEL).pack(anchor="w")
        self.pass_entry = tk.Entry(card, width=32, show="•", bg=PANEL2, fg=TEXT, insertbackground=TEXT, relief="flat")
        self.pass_entry.pack(ipady=9, pady=(4, 18))
        self.pass_entry.bind("<Return>", lambda e: self.login())
        self.button(card, "ENTRAR", self.login, ACCENT, "#00151a").pack(fill="x")
        tk.Label(wrap, text="Acesso inicial: admin / 1234  •  Altere a senha nas configurações.", fg=MUTED, bg=BG, font=self.ui_font(8)).pack(pady=14)
        self.user_entry.focus_set()

    def button(self, parent, label, command, bg=ACCENT, fg="#061018"):
        return tk.Button(parent, text=label, command=command, bg=bg, fg=fg,
                         activebackground=PINK, activeforeground="#080810",
                         relief="flat", bd=0, cursor="hand2", padx=13, pady=9,
                         font=self.ui_font(9, "bold"))

    def login(self):
        if self.user_entry.get() == self.config.get("username") and self.pass_entry.get() == self.config.get("password"):
            self.build_main()
        else:
            messagebox.showerror("Acesso negado", "Usuário ou senha incorretos.")

    def build_main(self):
        self.clear()
        header = tk.Frame(self.root, bg=PANEL, height=58)
        header.pack(fill="x")
        header.pack_propagate(False)
        self.title_label = tk.Label(header, text="  BREAK EXECUTOR  //  LUA WORKSPACE", bg=PANEL, fg=ACCENT, font=self.ui_font(14, "bold"))
        self.title_label.pack(side="left", padx=12)
        tk.Label(header, text=f"v{APP_VERSION}  •  LOCAL", bg=PANEL, fg=MUTED, font=self.ui_font(9)).pack(side="left", padx=8)
        self.button(header, "⚙ CONFIGURAÇÕES", self.settings, PANEL2, TEXT).pack(side="right", padx=8, pady=9)
        self.button(header, "SAIR", self.build_login, "#402035", "#ffd9ee").pack(side="right", padx=4, pady=9)

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=12, pady=12)
        side = tk.Frame(body, bg=PANEL, width=190, padx=10, pady=12)
        side.pack(side="left", fill="y", padx=(0, 12))
        side.pack_propagate(False)
        tk.Label(side, text="MENU", bg=PANEL, fg=MUTED, font=self.ui_font(9, "bold")).pack(anchor="w", pady=(0, 12))
        for name, fn in [("EDITOR LUA", self.show_editor), ("BIBLIOTECA", self.show_library), ("PAINEL ADM", self.show_admin), ("SOBRE", self.show_about)]:
            self.button(side, name, fn, PANEL2, TEXT).pack(fill="x", pady=4)

        self.content = tk.Frame(body, bg=BG)
        self.content.pack(side="left", fill="both", expand=True)
        self.show_editor()
        self.animate_rgb()

    def animate_rgb(self):
        if not getattr(self, "title_label", None) or not self.title_label.winfo_exists():
            self.rgb_after_id = None
            return
        colors = [ACCENT, PINK, "#8b5cff", GREEN]
        self.title_label.configure(fg=colors[self.rgb_index % len(colors)])
        self.rgb_index += 1
        self.rgb_after_id = self.root.after(650, self.animate_rgb)

    def clear_content(self):
        if hasattr(self, "editor") and self.editor.winfo_exists():
            self.draft_text = self.editor.get("1.0", "end-1c")
        for w in self.content.winfo_children():
            w.destroy()

    def section_title(self, title, subtitle=""):
        tk.Label(self.content, text=title, bg=BG, fg=TEXT, font=self.ui_font(20, "bold")).pack(anchor="w")
        if subtitle:
            tk.Label(self.content, text=subtitle, bg=BG, fg=MUTED).pack(anchor="w", pady=(2, 12))

    def show_editor(self):
        self.clear_content()
        self.section_title("EDITOR LUA", "Escreva, edite e organize seus arquivos Lua localmente.  •  Ctrl+S salva  •  Ctrl+N cria um arquivo")
        bar = tk.Frame(self.content, bg=BG)
        bar.pack(fill="x", pady=(0, 8))
        for label, fn in [("NOVO", self.new_file), ("ABRIR", self.open_file), ("SALVAR", self.save_file), ("SALVAR COMO", self.save_as), ("LIMPAR", self.clear_editor)]:
            self.button(bar, label, fn, PANEL2, TEXT).pack(side="left", padx=(0, 6))
        self.editor = tk.Text(self.content, bg="#080d17", fg="#d9e7ff", insertbackground=ACCENT,
                              selectbackground="#23465b", relief="flat", padx=14, pady=14,
                              wrap="none", undo=True, font=("Consolas", 11))
        self.editor.pack(fill="both", expand=True)
        initial_text = self.draft_text
        if initial_text is None:
            initial_text = "-- BREAK EXECUTOR | Editor Lua local\n-- Este aplicativo não injeta código em jogos.\n\nprint(\"Olá, mundo!\")\n"
        self.editor.insert("1.0", initial_text)
        self.editor.bind("<Control-s>", self.shortcut_save)
        self.editor.bind("<Control-n>", self.shortcut_new)
        self.editor.bind("<Control-o>", self.shortcut_open)
        self.editor.bind("<KeyRelease>", self.update_editor_status)
        self.status = tk.Label(self.content, text="Pronto • Arquivos salvos em " + str(SCRIPTS_DIR), bg=BG, fg=MUTED, anchor="w")
        self.status.pack(fill="x", pady=(7, 0))
        self.editor.focus_set()
        self.update_editor_status()

    def update_editor_status(self, event=None):
        if not hasattr(self, "editor") or not self.editor.winfo_exists():
            return
        line, column = self.editor.index("insert").split(".")
        content = self.editor.get("1.0", "end-1c")
        if hasattr(self, "status") and self.status.winfo_exists():
            self.status.configure(text=f"Linha {line}, coluna {int(column) + 1}  •  {len(content)} caracteres  •  {len(content.splitlines()) or 1} linhas")

    def shortcut_save(self, event=None):
        self.save_file()
        return "break"

    def shortcut_new(self, event=None):
        self.new_file()
        return "break"

    def shortcut_open(self, event=None):
        self.open_file()
        return "break"

    def new_file(self):
        self.current_file = None
        self.draft_text = ""
        self.editor.delete("1.0", "end")
        self.status.configure(text="Novo arquivo • pronto para editar")

    def open_file(self):
        path = filedialog.askopenfilename(initialdir=SCRIPTS_DIR, filetypes=[("Lua", "*.lua"), ("Texto", "*.txt"), ("Todos", "*.*")])
        if path:
            try:
                self.current_file = Path(path)
                content = self.current_file.read_text(encoding="utf-8", errors="replace")
            except OSError as exc:
                messagebox.showerror("Abrir arquivo", f"Não foi possível abrir o arquivo:\n{exc}")
                return
            self.editor.delete("1.0", "end")
            self.editor.insert("1.0", content)
            self.draft_text = content
            self.status.configure(text=f"Aberto: {self.current_file.name}")

    def save_file(self):
        if not self.current_file:
            return self.save_as()
        try:
            content = self.editor.get("1.0", "end-1c")
            self.current_file.write_text(content, encoding="utf-8")
        except OSError as exc:
            messagebox.showerror("Salvar arquivo", f"Não foi possível salvar o arquivo:\n{exc}")
            return
        self.draft_text = content
        self.status.configure(text=f"Salvo: {self.current_file.name}")

    def save_as(self):
        path = filedialog.asksaveasfilename(initialdir=SCRIPTS_DIR, defaultextension=".lua", filetypes=[("Lua", "*.lua"), ("Texto", "*.txt")])
        if path:
            self.current_file = Path(path)
            self.save_file()

    def clear_editor(self):
        self.editor.delete("1.0", "end")
        self.update_editor_status()

    def show_library(self):
        self.clear_content()
        self.section_title("BIBLIOTECA DE SCRIPTS", "Arquivos Lua armazenados no seu computador.")
        row = tk.Frame(self.content, bg=BG)
        row.pack(fill="x", pady=6)
        filter_var = tk.StringVar()
        search = tk.Entry(row, textvariable=filter_var, width=28, bg=PANEL2, fg=TEXT, insertbackground=TEXT, relief="flat")
        search.pack(side="right", ipady=7, padx=(8, 0))
        tk.Label(row, text="BUSCAR", bg=BG, fg=MUTED, font=self.ui_font(8, "bold")).pack(side="right")
        listing = tk.Listbox(self.content, bg=PANEL, fg=TEXT, selectbackground="#17445a", relief="flat", font=("Consolas", 10))
        listing.pack(fill="both", expand=True, pady=8)
        def refresh():
            listing.delete(0, "end")
            try:
                files = sorted(p for p in SCRIPTS_DIR.iterdir() if p.is_file())
            except OSError:
                files = []
            query = filter_var.get().strip().lower()
            for p in files:
                if not query or query in p.name.lower():
                    listing.insert("end", p.name)
        def open_selected():
            sel = listing.curselection()
            if sel:
                p = SCRIPTS_DIR / listing.get(sel[0])
                try:
                    content = p.read_text(encoding="utf-8", errors="replace")
                except OSError as exc:
                    messagebox.showerror("Abrir arquivo", f"Não foi possível abrir o arquivo:\n{exc}")
                    return
                self.show_editor()
                self.current_file = p
                self.editor.delete("1.0", "end")
                self.editor.insert("1.0", content)
                self.status.configure(text=f"Aberto: {p.name}")
        def delete_selected():
            sel = listing.curselection()
            if sel:
                p = SCRIPTS_DIR / listing.get(sel[0])
                if messagebox.askyesno("Confirmar", f"Excluir {p.name}?"):
                    try:
                        p.unlink()
                    except OSError as exc:
                        messagebox.showerror("Excluir arquivo", f"Não foi possível excluir o arquivo:\n{exc}")
                    refresh()
        self.button(row, "ATUALIZAR", refresh).pack(side="left", padx=(0, 6))
        self.button(row, "ABRIR NO EDITOR", open_selected, PANEL2, TEXT).pack(side="left", padx=6)
        self.button(row, "EXCLUIR", delete_selected, "#55253a", "#ffe5ef").pack(side="left", padx=6)
        filter_var.trace_add("write", lambda *_: refresh())
        listing.bind("<Double-Button-1>", lambda event: open_selected())
        refresh()

    def show_admin(self):
        self.clear_content()
        self.section_title("PAINEL ADM", "Ferramentas locais para administrar este aplicativo.")
        card = tk.Frame(self.content, bg=PANEL, padx=18, pady=18)
        card.pack(fill="x", pady=8)
        tk.Label(card, text="STATUS DO APLICATIVO", bg=PANEL, fg=ACCENT, font=self.ui_font(12, "bold")).pack(anchor="w")
        tk.Label(card, text="Conta local: " + self.config.get("username", "admin"), bg=PANEL, fg=TEXT).pack(anchor="w", pady=6)
        tk.Label(card, text=f"Arquivos Lua: {len(list(SCRIPTS_DIR.glob('*.lua')))}", bg=PANEL, fg=TEXT).pack(anchor="w")
        tk.Label(card, text="Permissões: administrador local do BREAK EXECUTOR", bg=PANEL, fg=MUTED).pack(anchor="w", pady=6)
        self.button(card, "ALTERAR CREDENCIAIS", self.settings).pack(anchor="w", pady=(10, 0))
        note = tk.Frame(self.content, bg=PANEL2, padx=16, pady=14)
        note.pack(fill="x", pady=8)
        tk.Label(note, text="Observação", bg=PANEL2, fg=PINK, font=self.ui_font(11, "bold")).pack(anchor="w")
        tk.Label(note, text="Este painel não concede poderes administrativos em experiências Roblox de terceiros. Para comandos globais, use um jogo próprio e implemente validação no servidor.", bg=PANEL2, fg=TEXT, wraplength=700, justify="left").pack(anchor="w", pady=6)

    def settings(self):
        user = simpledialog.askstring("Configurações", "Novo usuário:", initialvalue=self.config.get("username", "admin"), parent=self.root)
        if not user or not user.strip():
            return
        password = simpledialog.askstring("Configurações", "Nova senha:", show="*", parent=self.root)
        if not password:
            return
        self.config = {"username": user.strip(), "password": password}
        try:
            CONFIG_FILE.write_text(json.dumps(self.config, indent=2), encoding="utf-8")
        except OSError as exc:
            messagebox.showerror("Configurações", f"Não foi possível salvar as credenciais:\n{exc}")
            return
        messagebox.showinfo("Configurações", "Credenciais atualizadas.")

    def show_about(self):
        self.clear_content()
        self.section_title("SOBRE O BREAK EXECUTOR")
        tk.Label(self.content, text=f"BREAK EXECUTOR\nEditor e biblioteca local de scripts Lua.\n\nVersão {APP_VERSION}\nInterface Tkinter • Windows 64 bits\n\nNão inclui injetor, exploit ou bypass.", bg=PANEL, fg=TEXT, justify="left", padx=22, pady=22).pack(fill="x", pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = BreakExecutor(root)
    root.mainloop()
