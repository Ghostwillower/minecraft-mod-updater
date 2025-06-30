import tkinter as tk
from tkinter import filedialog, messagebox

from mod_updater import version_exists, update_jar


class ModUpdaterApp:
    def __init__(self, master):
        self.master = master
        master.title("Minecraft Mod Updater")

        tk.Label(master, text="Jar file:").grid(row=0, column=0, sticky="e")
        self.jar_path_var = tk.StringVar()
        tk.Entry(master, textvariable=self.jar_path_var, width=40).grid(row=0, column=1)
        tk.Button(master, text="Browse", command=self.choose_jar).grid(row=0, column=2)

        tk.Label(master, text="Target version:").grid(row=1, column=0, sticky="e")
        self.version_var = tk.StringVar()
        tk.Entry(master, textvariable=self.version_var).grid(row=1, column=1, sticky="we")

        tk.Label(master, text="Modrinth Project ID:").grid(row=2, column=0, sticky="e")
        self.modrinth_var = tk.StringVar()
        tk.Entry(master, textvariable=self.modrinth_var).grid(row=2, column=1, sticky="we")

        tk.Label(master, text="CurseForge Mod ID:").grid(row=3, column=0, sticky="e")
        self.curse_var = tk.StringVar()
        tk.Entry(master, textvariable=self.curse_var).grid(row=3, column=1, sticky="we")

        tk.Label(master, text="CurseForge API Key:").grid(row=4, column=0, sticky="e")
        self.curse_key_var = tk.StringVar()
        tk.Entry(master, textvariable=self.curse_key_var, show='*').grid(row=4, column=1, sticky="we")

        tk.Button(master, text="Update", command=self.run_update).grid(row=5, column=0, columnspan=3, pady=5)

    def choose_jar(self):
        path = filedialog.askopenfilename(filetypes=[("JAR files", "*.jar")])
        if path:
            self.jar_path_var.set(path)

    def run_update(self):
        jar_path = self.jar_path_var.get()
        target_version = self.version_var.get().strip()
        modrinth_id = self.modrinth_var.get().strip()
        curse_id = self.curse_var.get().strip()
        curse_key = self.curse_key_var.get().strip()

        if not (jar_path and target_version and modrinth_id and curse_id):
            messagebox.showerror("Missing info", "Please fill out all fields")
            return

        if version_exists(modrinth_id, curse_id, target_version, curse_key):
            messagebox.showinfo("Exists", "Target version already published")
            return

        try:
            out_path = update_jar(jar_path, target_version)
            messagebox.showinfo("Success", f"Updated jar saved to {out_path}")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))



def main():
    root = tk.Tk()
    app = ModUpdaterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
