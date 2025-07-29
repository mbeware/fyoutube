import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.Config import USER, all_options
import core.Config as Config

class ConfigEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Configuration fyoutube")
        self.root.geometry("1200x800")
        
        self.setup_dark_theme()
        self.create_widgets()
        self.load_config()
        
    def setup_dark_theme(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TFrame', background='#2b2b2b')
        style.configure('TLabel', background='#2b2b2b', foreground='white')
        style.configure('TButton', background='#404040', foreground='white')
        style.configure('TEntry', background='#404040', foreground='white', fieldbackground='#404040')
        style.configure('TCheckbutton', background='#2b2b2b', foreground='white')
        style.configure('TCombobox', background='#404040', foreground='white', fieldbackground='#404040')
        style.configure('TNotebook', background='#2b2b2b')
        style.configure('TNotebook.Tab', background='#404040', foreground='white')
        
        self.root.configure(bg='#2b2b2b')
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        toolbar_frame = ttk.Frame(main_frame)
        toolbar_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(toolbar_frame, text="Fichier", command=self.file_menu).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar_frame, text="Édition", command=self.edit_menu).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar_frame, text="Aide", command=self.help_menu).pack(side=tk.LEFT, padx=(0, 5))
        
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        nav_frame = ttk.Frame(content_frame)
        nav_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        nav_frame.configure(width=200)
        
        ttk.Label(nav_frame, text="Navigation", font=('Arial', 12, 'bold')).pack(pady=(0, 10))
        
        main_content_frame = ttk.Frame(content_frame)
        main_content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.notebook = ttk.Notebook(main_content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.create_tabs()
        
        bottom_nav_frame = ttk.Frame(nav_frame)
        bottom_nav_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
        ttk.Button(bottom_nav_frame, text="Configuration", command=self.load_config).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(bottom_nav_frame, text="Sortir", command=self.root.quit).pack(fill=tk.X)
        
    def create_tabs(self):
        self.tabs = {}
        self.widgets = {}
        
        tab_configs = [
            ("Téléchargement", "Download"),
            ("Information", "Info"), 
            ("Débogage", "Debug"),
            ("Chemins", "Paths"),
            ("Temporisation", "Sleep"),
            ("Général", "General")
        ]
        
        for tab_name, config_section in tab_configs:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=tab_name)
            self.tabs[config_section] = frame
            self.widgets[config_section] = {}
            
            canvas = tk.Canvas(frame, bg='#2b2b2b', highlightthickness=0)
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            self.create_section_widgets(scrollable_frame, config_section)
            
    def create_section_widgets(self, parent, section):
        row = 0
        
        if section == "Paths":
            path_configs = [
                ("VIDEO_DIR", "Répertoire vidéo"),
                ("ARCHIVE_DIR", "Répertoire archive"),
                ("LOGS_DIR", "Répertoire logs"),
                ("BASE_DOWNLOAD_LIST", "Liste de téléchargement"),
                ("SUBSCRIPTIONS_FILE", "Fichier abonnements"),
                ("LASTDOWNLOADEDCHANNEL_FILE", "Dernier canal")
            ]
            
            for key, label in path_configs:
                ttk.Label(parent, text=f"{label}:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
                entry = ttk.Entry(parent, width=50)
                entry.grid(row=row, column=1, padx=5, pady=2)
                self.widgets[section][key] = entry
                row += 1
                
        elif section == "Sleep":
            sleep_configs = [
                ("SUBTITLES", "Sous-titres (s)"),
                ("INTERVAL", "Intervalle (s)"),
                ("REQUESTS", "Requêtes (s)"),
                ("MAX_INTERVAL", "Intervalle max (s)")
            ]
            
            for key, label in sleep_configs:
                ttk.Label(parent, text=f"{label}:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
                entry = ttk.Entry(parent, width=20)
                entry.grid(row=row, column=1, padx=5, pady=2)
                self.widgets[section][key] = entry
                row += 1
                
        else:
            for option_name, option in all_options.items():
                should_include = False
                
                if section == "Download" and (option.download or option.download_required):
                    should_include = True
                elif section == "Info" and (option.info or option.info_required):
                    should_include = True
                elif section == "Debug" and option.debug:
                    should_include = True
                elif section == "General" and not (option.download or option.info or option.debug):
                    should_include = True
                    
                if should_include:
                    label_text = option_name.replace('_', ' ').title()
                    ttk.Label(parent, text=f"{label_text}:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
                    
                    if option.allowed_values:
                        widget = ttk.Combobox(parent, values=option.allowed_values, width=30)
                    elif isinstance(getattr(option, f'{section.lower()}_value', None), bool):
                        widget = ttk.Checkbutton(parent)
                        widget._variable = tk.BooleanVar()
                        widget.configure(variable=widget._variable)
                    else:
                        widget = ttk.Entry(parent, width=40)
                        
                    widget.grid(row=row, column=1, padx=5, pady=2)
                    self.widgets[section][option_name] = widget
                    row += 1
                    
    def load_config(self):
        try:
            USER.reload()
            
            for section, widgets in self.widgets.items():
                if section in ["Paths", "Sleep"]:
                    config_section = getattr(USER, section, {})
                    for key, widget in widgets.items():
                        value = config_section.get(key, "")
                        if isinstance(widget, ttk.Entry):
                            widget.delete(0, tk.END)
                            widget.insert(0, str(value))
                else:
                    config_section = getattr(USER, section, {})
                    for option_name, widget in widgets.items():
                        value = config_section.get(option_name, "")
                        
                        if isinstance(widget, ttk.Checkbutton):
                            if not hasattr(widget, '_variable'):
                                widget._variable = tk.BooleanVar()
                                widget.configure(variable=widget._variable)
                            widget._variable.set(bool(value))
                        elif isinstance(widget, (ttk.Entry, ttk.Combobox)):
                            widget.delete(0, tk.END)
                            widget.insert(0, str(value))
                            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement: {e}")
            
    def save_config(self):
        try:
            for section, widgets in self.widgets.items():
                if not hasattr(USER, section):
                    setattr(USER, section, {})
                    
                config_section = getattr(USER, section)
                
                for key, widget in widgets.items():
                    if isinstance(widget, ttk.Checkbutton):
                        if hasattr(widget, '_variable'):
                            value = widget._variable.get()
                        else:
                            value = widget.instate(['selected'])
                    else:
                        value = widget.get()
                        
                    config_section[key] = value
                    
            USER.save()
            messagebox.showinfo("Succès", "Configuration sauvegardée avec succès!")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde: {e}")
            
    def file_menu(self):
        menu = tk.Menu(self.root, tearoff=0, bg='#404040', fg='white')
        menu.add_command(label="Ouvrir config", command=lambda: self._menu_command(menu, self.open_config))
        menu.add_command(label="Sauvegarder", command=lambda: self._menu_command(menu, self.save_config))
        menu.add_command(label="Sauvegarder sous...", command=lambda: self._menu_command(menu, self.save_config_as))
        menu.add_separator()
        menu.add_command(label="Quitter", command=lambda: self._menu_command(menu, self.root.quit))
        
        try:
            menu.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())
        finally:
            pass
            
    def edit_menu(self):
        menu = tk.Menu(self.root, tearoff=0, bg='#404040', fg='white')
        menu.add_command(label="Réinitialiser", command=lambda: self._menu_command(menu, self.reset_config))
        menu.add_command(label="Valeurs par défaut", command=lambda: self._menu_command(menu, self.load_defaults))
        
        try:
            menu.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())
        finally:
            pass

    def _menu_command(self, menu, command):
        """Helper method to execute menu command and destroy menu"""
        menu.destroy()
        command()
            
    def help_menu(self):
        messagebox.showinfo("Aide", "Éditeur de configuration fyoutube\n\nUtilisez les onglets pour configurer les différents aspects du téléchargeur.")
        
    def open_config(self):
        filename = filedialog.askopenfilename(
            title="Ouvrir fichier de configuration",
            filetypes=[("Fichiers TOML", "*.toml"), ("Tous les fichiers", "*.*")]
        )
        if filename:
            try:
                USER.config_path = filename
                self.load_config()
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'ouvrir le fichier: {e}")
                
    def save_config_as(self):
        filename = filedialog.asksaveasfilename(
            title="Sauvegarder configuration sous",
            defaultextension=".toml",
            filetypes=[("Fichiers TOML", "*.toml"), ("Tous les fichiers", "*.*")]
        )
        if filename:
            try:
                original_path = USER.config_path
                USER.config_path = filename
                self.save_config()
                USER.config_path = original_path
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de sauvegarder: {e}")
                
    def reset_config(self):
        if messagebox.askyesno("Confirmation", "Réinitialiser toute la configuration?"):
            self.load_defaults()
            
    def load_defaults(self):
        try:
            for section, widgets in self.widgets.items():
                for key, widget in widgets.items():
                    if isinstance(widget, ttk.Checkbutton):
                        var = tk.BooleanVar(value=False)
                        widget.configure(variable=var)
                    elif isinstance(widget, (ttk.Entry, ttk.Combobox)):
                        widget.delete(0, tk.END)
                        
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des défauts: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigEditor(root)
    root.mainloop()
