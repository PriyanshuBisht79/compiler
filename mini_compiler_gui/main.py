import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from lexer import tokenize
from parser import parse
from semantic import build_symbol_table
from ir_generator import generate_ir
from optimizer import optimize_ir
from codegen import generate_code
from visualize import generate_ast_image
from PIL import Image, ImageTk  
from semantic import build_symbol_table, SemanticError
from tkinter import filedialog
import os


class CompilerGUI:

    def apply_dark_theme(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")

        self.root.configure(bg="#2e2e2e")
        style.configure("TNotebook", background="#2e2e2e", borderwidth=0)
        style.configure("TNotebook.Tab", background="#444", foreground="#eee", padding=10)
        style.map("TNotebook.Tab", background=[("selected", "#1e90ff")])

        for tab in self.tabs.values():
            tab.configure(bg="#1e1e1e", fg="#dcdcdc", insertbackground="white", font=("Courier New", 11))



    def load_input(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as f:
                content = f.read()
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert(tk.END, content)

    def save_output(self):
        current_tab = self.output_notebook.tab(self.output_notebook.select(), "text")
        content = self.tabs[current_tab].get("1.0", tk.END).strip()

        if not content:
            messagebox.showinfo("Save Output", "No output to save in the selected tab.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as f:
                f.write(content)
            messagebox.showinfo("Saved", f"{current_tab} output saved to:\n{file_path}")



    def log_error(self, message):
        self.tabs["Errors"].insert(tk.END, message + "\n")
        self.tabs["Errors"].see(tk.END)

    def __init__(self, root):
        self.root = root
        self.root.title("Mini Compiler with Visualization")
        self.root.geometry("1000x700")

        self.create_widgets()
        self.create_widgets()
        self.apply_dark_theme()  # <- ADD THIS LINE


    def create_widgets(self):
        self.input_text = tk.Text(self.root, height=10)
        self.input_text.pack(fill=tk.X, padx=10, pady=5)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Load Input", command=self.load_input).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Save Output", command=self.save_output).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Lexical", command=self.lexical_phase).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Parse", command=self.parse_phase).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Semantic", command=self.semantic_phase).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="IR Gen", command=self.ir_phase).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Optimize", command=self.optimize_phase).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Codegen", command=self.codegen_phase).pack(side=tk.LEFT, padx=5)

        self.output_notebook = ttk.Notebook(self.root)
        self.output_notebook.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

        self.tabs = {}
        for name in ["Tokens", "AST", "Semantic", "IR", "Optimized IR", "Target Code", "Errors"]:
            frame = tk.Frame(self.output_notebook)
            text = tk.Text(frame)
            text.pack(expand=True, fill=tk.BOTH)
            self.output_notebook.add(frame, text=name)
            self.tabs[name] = text


        btn_frame = tk.Frame(self.root, bg="#2e2e2e")  # Dark background for the button bar
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        # Define all buttons and their actions
        buttons = [
            ("Load Input", self.load_input),
            ("Save Output", self.save_output),
            ("Lexical", self.lexical_phase),
            ("Parse", self.parse_phase),
            ("Semantic", self.semantic_phase),
            ("IR Gen", self.ir_phase),
            ("Optimize", self.optimize_phase),
            ("Codegen", self.codegen_phase)
        ]

        # styled buttons in a row
        for text, cmd in buttons:
            tk.Button(
                btn_frame,
                text=text,
                command=cmd,
                bg="#444",            # Dark button
                fg="white",           # White text
                activebackground="#1e90ff",  # Bright blue on click/hover
                activeforeground="white",
                relief="flat",        # Flat look (no borders)
                font=("Segoe UI", 10),
                padx=10,
                pady=5
            ).pack(side=tk.LEFT, padx=4)



    def set_output(self, tab, content):
        self.tabs[tab].delete("1.0", tk.END)
        self.tabs[tab].insert(tk.END, content)

    def lexical_phase(self):
        self.tabs["Errors"].delete("1.0", tk.END)
        code = self.input_text.get("1.0", tk.END)
        tokens = tokenize(code)
        out = "\n".join([f"{t.type:<10} {t.value}" for t in tokens])
        self.set_output("Tokens", out)

    def parse_phase(self):
        self.tabs["Errors"].delete("1.0", tk.END)
        code = self.input_text.get("1.0", tk.END)
        tree = parse(code)
        if tree:
            generate_ast_image(tree)

            tab = self.output_notebook.tabs()[1]
            frame = self.output_notebook.nametowidget(tab)

            for widget in frame.winfo_children():
                widget.destroy()

            try:
                image_path = "C:/Users/Admin/Desktop/mini_compiler_gui/assets/ast.png"
                img = Image.open(image_path)
                photo = ImageTk.PhotoImage(img)

                canvas = tk.Canvas(frame, bg="white", scrollregion=(0, 0, photo.width(), photo.height()))
                canvas.image = photo
                canvas.create_image(0, 0, anchor=tk.NW, image=photo)

                h_scroll = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=canvas.xview)
                v_scroll = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
                canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

                canvas.grid(row=0, column=0, sticky="nsew")
                v_scroll.grid(row=0, column=1, sticky="ns")
                h_scroll.grid(row=1, column=0, sticky="ew")

                frame.grid_rowconfigure(0, weight=1)
                frame.grid_columnconfigure(0, weight=1)

                # ✅ Mousewheel scrolling (Windows)
                def _on_mousewheel(event):
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

                def _on_shift_mousewheel(event):
                    canvas.xview_scroll(int(-1*(event.delta/120)), "units")

                canvas.bind_all("<MouseWheel>", _on_mousewheel)         # Vertical
                canvas.bind_all("<Shift-MouseWheel>", _on_shift_mousewheel)  # Horizontal

            except Exception as e:
                self.set_output("AST", f"Error loading AST image: {e}")




    def semantic_phase(self):
        self.tabs["Errors"].delete("1.0", tk.END)
        code = self.input_text.get("1.0", tk.END)
        try:
            tree = parse(code)
            symbol_table = build_symbol_table(tree)

            output = "Symbol Table:\n"
            for var, typ in symbol_table.items():
                output += f"{var} : {typ}\n"

            self.set_output("Semantic", output)

        except SemanticError as e:
            msg = f"Semantic Error:\n{e}"
            self.set_output("Semantic", msg)
            self.log_error(msg)

        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            self.set_output("Semantic", f"Unexpected Error:\n{e}")
            self.log_error("Unexpected Error:\n" + tb)


    def ir_phase(self):
        self.tabs["Errors"].delete("1.0", tk.END)
        code = self.input_text.get("1.0", tk.END)
        tree = parse(code)

        if tree is None:
            self.set_output("IR", "Parsing failed. No IR generated.")
            self.log_error("Parsing failed. Please fix syntax errors before IR generation.")
            return

        ir = generate_ir(tree)
        self.set_output("IR", "\n".join(ir))



    def optimize_phase(self):
        self.tabs["Errors"].delete("1.0", tk.END)
        code = self.input_text.get("1.0", tk.END)
        tree = parse(code)

        if tree is None:
            self.set_output("Optimized IR", "Parsing failed. Optimization skipped.")
            self.log_error("Parsing failed. Cannot optimize invalid code.")
            return

        ir = generate_ir(tree)
        optimized = optimize_ir(ir)
        self.set_output("Optimized IR", "\n".join(optimized))


    def codegen_phase(self):
        self.tabs["Errors"].delete("1.0", tk.END)
        code = self.input_text.get("1.0", tk.END)
        tree = parse(code)

        if tree is None:
            self.set_output("Target Code", "Parsing failed. No code generated.")
            self.log_error("Parsing failed. Cannot generate code from invalid syntax.")
            return

        ir = generate_ir(tree)
        code = generate_code(ir)
        self.set_output("Target Code", "\n".join(code))

if __name__ == "__main__":
    root = tk.Tk()
    app = CompilerGUI(root)
    root.mainloop()
