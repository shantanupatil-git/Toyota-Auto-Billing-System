import tkinter as tk
from tkinter import ttk, messagebox
import random
import datetime

class MinimalToyotaBilling:
    def __init__(self, root):
        self.root = root
        self.root.title("Toyota Auto Billing - Minimal Dashboard")
        self.root.geometry("850x620")
        self.root.configure(bg="#fff")

        # --- Models & Parts/Services ---
        self.models = {
            "Fortuner": [
                ("Front Bumper", 20400), ("Rear Bumper", 14210), ("Head Light", 35500),
                ("Oil Filter", 660), ("Engine Oil (L)", 990), ("Battery", 10500)
            ],
            "Innova Crysta": [
                ("Front Bumper", 16200), ("Rear Bumper", 12100), ("Head Light", 19500),
                ("Oil Filter", 540), ("Engine Oil (L)", 850), ("Battery", 9600)
            ],
            "Camry": [
                ("Front Bumper", 44500), ("Rear Bumper", 28500), ("Head Light", 48900),
                ("Oil Filter", 980), ("Engine Oil (L)", 1680), ("Battery", 14800)
            ]
        }
        self.services = [
            ("General Service", 4900), ("Brake Overhaul", 3200), ("AC Service", 2300)
        ]
        self.selected_model = tk.StringVar(value=list(self.models.keys())[0])
        self.part_vars = {}
        self.svc_vars = {name: tk.IntVar() for name, _ in self.services}
        self.cust_name = tk.StringVar()
        self.phone = tk.StringVar()
        self.reg_no = tk.StringVar()
        self.bill_no = tk.StringVar(value=str(random.randint(1000, 9999)))
        self.bill_date = tk.StringVar(value=datetime.date.today())
        self.init_part_vars()

        # --- Top: Customer/Form ---
        formf = ttk.LabelFrame(self.root, text="Customer & Vehicle", padding=8)
        formf.pack(fill=tk.X, padx=12, pady=7)
        ttk.Label(formf, text="Name:").grid(row=0, column=0)
        ttk.Entry(formf, textvariable=self.cust_name, width=19).grid(row=0, column=1)
        ttk.Label(formf, text="Phone:").grid(row=0, column=2)
        ttk.Entry(formf, textvariable=self.phone, width=12).grid(row=0, column=3)
        ttk.Label(formf, text="Reg No:").grid(row=0, column=4)
        ttk.Entry(formf, textvariable=self.reg_no, width=10).grid(row=0, column=5)
        ttk.Label(formf, text="Model:").grid(row=0, column=6)
        combo = ttk.Combobox(formf, values=list(self.models.keys()), textvariable=self.selected_model, state="readonly", width=15)
        combo.grid(row=0, column=7)
        combo.bind("<<ComboboxSelected>>", self.model_changed)

        # --- Parts Table ---
        self.partsf = ttk.LabelFrame(self.root, text="Parts", padding=6)
        self.partsf.pack(fill=tk.X, padx=18, pady=7)
        self.update_parts_table()

        # --- Services Table ---
        svc_table = ttk.LabelFrame(self.root, text="Services", padding=6)
        svc_table.pack(fill=tk.X, padx=18, pady=7)
        ttk.Label(svc_table, text="Service Name").grid(row=0, column=0)
        ttk.Label(svc_table, text="Unit Price").grid(row=0, column=1)
        ttk.Label(svc_table, text="Qty").grid(row=0, column=2)
        for r, (name, price) in enumerate(self.services, 1):
            ttk.Label(svc_table, text=name).grid(row=r, column=0, sticky="w")
            ttk.Label(svc_table, text=f"₹{price}").grid(row=r, column=1)
            ttk.Entry(svc_table, textvariable=self.svc_vars[name], width=5).grid(row=r, column=2)

        # --- Bill area ---
        self.billf = ttk.LabelFrame(self.root, text="Bill Summary", padding=8)
        self.billf.pack(fill=tk.BOTH, padx=18, pady=7, expand=1)
        self.billtext = tk.Text(self.billf, font=("Consolas",11), width=70, height=10, bg="#f8f8f8")
        self.billtext.pack(fill=tk.BOTH, expand=1)

        # --- Buttons ---
        btnf = ttk.Frame(self.root)
        btnf.pack(fill=tk.X, padx=20, pady=7)
        ttk.Button(btnf, text="Calculate Bill", command=self.calculate_bill).pack(side=tk.LEFT, padx=3)
        ttk.Button(btnf, text="Clear", command=self.clear_all).pack(side=tk.LEFT, padx=3)
        ttk.Button(btnf, text="Exit", command=self.root.quit).pack(side=tk.RIGHT, padx=3)

    def init_part_vars(self):
        self.part_vars = {}
        for name, _ in self.models[self.selected_model.get()]:
            self.part_vars[name] = tk.IntVar()

    def model_changed(self, event=None):
        self.init_part_vars()
        self.update_parts_table()

    def update_parts_table(self):
        for widget in self.partsf.winfo_children():
            widget.destroy()
        ttk.Label(self.partsf, text="Part Name").grid(row=0, column=0)
        ttk.Label(self.partsf, text="Unit Price").grid(row=0, column=1)
        ttk.Label(self.partsf, text="Qty").grid(row=0, column=2)
        for r, (name, price) in enumerate(self.models[self.selected_model.get()], 1):
            ttk.Label(self.partsf, text=name).grid(row=r, column=0, sticky="w")
            ttk.Label(self.partsf, text=f"₹{price}").grid(row=r, column=1)
            ttk.Entry(self.partsf, textvariable=self.part_vars[name], width=5).grid(row=r, column=2)

    def calculate_bill(self):
        cust = self.cust_name.get().strip()
        phone = self.phone.get().strip()
        regno = self.reg_no.get().strip()
        if not cust or not phone or not regno:
            messagebox.showerror("Error", "Please fill customer and vehicle details.")
            return
        brand = self.selected_model.get()
        parts_sel = []
        parts_total = 0
        for name, price in self.models[brand]:
            qty = self.part_vars[name].get()
            if qty > 0:
                amt = qty * price
                parts_sel.append(f"{name:16} x{qty:<2} ₹{amt:>8}")
                parts_total += amt
        svc_sel = []
        svc_total = 0
        for name, price in self.services:
            qty = self.svc_vars[name].get()
            if qty > 0:
                amt = qty * price
                svc_sel.append(f"{name:16} x{qty:<2} ₹{amt:>8}")
                svc_total += amt
        gst_parts = round(parts_total * 0.12)
        gst_svc = round(svc_total * 0.18)
        total_amt = parts_total + svc_total + gst_parts + gst_svc
        self.billtext.delete(1.0, tk.END)
        self.billtext.insert(tk.END, f"BILL - TOYOTA SERVICE\nCustomer: {cust}\nModel: {brand}  Reg:{regno}\nBill: {self.bill_no.get()}  Date: {self.bill_date.get()}\n")
        self.billtext.insert(tk.END, "-"*48+"\nParts:\n")
        self.billtext.insert(tk.END, "\n".join(parts_sel) if parts_sel else "  None\n")
        self.billtext.insert(tk.END, f"\n  Subtotal: ₹{parts_total}\n  GST@12%: ₹{gst_parts}\n")
        self.billtext.insert(tk.END, "-"*48+"\nServices:\n")
        self.billtext.insert(tk.END, "\n".join(svc_sel) if svc_sel else "  None\n")
        self.billtext.insert(tk.END, f"\n  Subtotal: ₹{svc_total}\n  GST@18%: ₹{gst_svc}\n")
        self.billtext.insert(tk.END, "="*48+f"\nTOTAL: ₹{total_amt}\n")

    def clear_all(self):
        for v in self.part_vars.values(): v.set(0)
        for v in self.svc_vars.values(): v.set(0)
        self.cust_name.set("")
        self.phone.set("")
        self.reg_no.set("")
        self.bill_no.set(str(random.randint(1000, 9999)))
        self.bill_date.set(str(datetime.date.today()))
        self.selected_model.set(list(self.models.keys())[0])
        self.model_changed()
        self.billtext.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    MinimalToyotaBilling(root)
    root.mainloop()
