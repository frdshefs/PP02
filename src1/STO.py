import tkinter as tk
from tkinter import ttk, messagebox
import client_manager, vehicle_manager, order_manager

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Автосервис")
        self.root.geometry("1200x600")
        self.create_ui()

    def create_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.orders_frame = tk.Frame(self.notebook)
        self.clients_frame = tk.Frame(self.notebook)
        self.vehicles_frame = tk.Frame(self.notebook)

        self.notebook.add(self.orders_frame, text="Заказы")
        self.notebook.add(self.clients_frame, text="Клиенты")
        self.notebook.add(self.vehicles_frame, text="Автомобили")

        self.create_orders_tab()
        self.create_clients_tab()
        self.create_vehicles_tab()

    # ========================= Заказы =========================
    def create_orders_tab(self):
        columns = ("Id","Номер","Клиент","Авто","Дата","Статус","Стоимость")
        self.order_tree = ttk.Treeview(self.orders_frame, columns=columns, show="headings")
        for col in columns: self.order_tree.heading(col,text=col); self.order_tree.column(col,width=130)
        self.order_tree.pack(fill="both", expand=True,padx=10,pady=10)

        btn_frame = tk.Frame(self.orders_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame,text="Обновить",command=self.load_orders).grid(row=0,column=0,padx=5)
        ttk.Button(btn_frame,text="Изменить статус",command=self.change_status).grid(row=0,column=1,padx=5)
        ttk.Button(btn_frame,text="Редактировать заказ",command=self.edit_order).grid(row=0,column=2,padx=5)
        ttk.Button(btn_frame,text="Удалить",command=self.delete_order).grid(row=0,column=3,padx=5)

        self.load_orders()

    def get_selected_order_id(self):
        sel = self.order_tree.selection()
        if not sel: return None
        try: return int(self.order_tree.item(sel[0])["values"][0])
        except: return None

    def load_orders(self):
        order_manager.load_orders(self.order_tree)

    def change_status(self):
        order_id = self.get_selected_order_id()
        if not order_id: messagebox.showwarning("Ошибка","Выберите заказ"); return
        win = tk.Toplevel(self.root); win.title("Изменить статус"); win.geometry("300x150")
        ttk.Label(win,text="Новый статус").pack(pady=10)
        status_combo = ttk.Combobox(win, values=["Новый","В работе","Завершён"]); status_combo.pack(); status_combo.current(0)
        def save(): order_manager.update_status(order_id,status_combo.get()); self.load_orders(); win.destroy()
        ttk.Button(win,text="Сохранить",command=save).pack(pady=15)

    def delete_order(self):
        order_id = self.get_selected_order_id()
        if not order_id: messagebox.showwarning("Ошибка","Выберите заказ"); return
        if messagebox.askyesno("Подтверждение","Удалить заказ?"): order_manager.delete_order(order_id); self.load_orders()

    def edit_order(self):
        order_id = self.get_selected_order_id()
        if not order_id: messagebox.showwarning("Ошибка","Выберите заказ"); return
        import pyodbc
        from database import get_connection
        conn = get_connection(); cursor = conn.cursor()
        cursor.execute("SELECT Id, FullName FROM Clients"); clients = cursor.fetchall()
        cursor.execute("SELECT Id, Brand + ' ' + Model FROM Vehicles"); vehicles = cursor.fetchall()
        conn.close()
        values = self.order_tree.item(self.order_tree.selection()[0])["values"]

        win = tk.Toplevel(self.root); win.title("Редактирование заказа"); win.geometry("400x500")
        tk.Label(win,text="Номер").pack(pady=5); number_entry = ttk.Entry(win); number_entry.pack(); number_entry.insert(0,values[1])
        tk.Label(win,text="Клиент").pack(pady=5); client_combo = ttk.Combobox(win, values=[f"{c.Id} - {c.FullName}" for c in clients]); client_combo.pack(); client_combo.current(0)
        tk.Label(win,text="Авто").pack(pady=5); vehicle_combo = ttk.Combobox(win, values=[f"{v.Id} - {v[1]}" for v in vehicles]); vehicle_combo.pack(); vehicle_combo.current(0)
        tk.Label(win,text="Дата").pack(pady=5); date_entry = ttk.Entry(win); date_entry.pack(); date_entry.insert(0,values[4])
        tk.Label(win,text="Статус").pack(pady=5); status_combo = ttk.Combobox(win, values=["Новый","В работе","Завершён"]); status_combo.pack(); status_combo.set(values[5])
        tk.Label(win,text="Стоимость").pack(pady=5); total_entry = ttk.Entry(win); total_entry.pack(); total_entry.insert(0,values[6])

        def save_changes():
            client_id = int(client_combo.get().split(" - ")[0])
            vehicle_id = int(vehicle_combo.get().split(" - ")[0])
            order_manager.update_order(order_id, number_entry.get(), client_id, vehicle_id, date_entry.get(), status_combo.get(), float(total_entry.get()))
            self.load_orders(); win.destroy()
        ttk.Button(win,text="Сохранить",command=save_changes).pack(pady=20)

    # ========================= Клиенты =========================
    def create_clients_tab(self):
        columns = ("Id","ФИО","Телефон","Email")
        self.client_tree = ttk.Treeview(self.clients_frame, columns=columns, show="headings")
        for col in columns: self.client_tree.heading(col,text=col); self.client_tree.column(col,width=150)
        self.client_tree.pack(fill="both", expand=True,padx=10,pady=10)

        btn_frame = tk.Frame(self.clients_frame); btn_frame.pack(pady=10)
        ttk.Button(btn_frame,text="Обновить",command=self.load_clients).grid(row=0,column=0,padx=5)
        ttk.Button(btn_frame,text="Добавить",command=self.add_client).grid(row=0,column=1,padx=5)
        ttk.Button(btn_frame,text="Редактировать",command=self.edit_client).grid(row=0,column=2,padx=5)
        ttk.Button(btn_frame,text="Удалить",command=self.delete_client).grid(row=0,column=3,padx=5)

        self.load_clients()

    def load_clients(self): client_manager.load_clients(self.client_tree)

    def get_selected_client_id(self):
        sel = self.client_tree.selection()
        if not sel: return None
        try: return int(self.client_tree.item(sel[0])["values"][0])
        except: return None

    def add_client(self):
        win = tk.Toplevel(self.root); win.title("Добавить клиента"); win.geometry("300x250")
        tk.Label(win,text="ФИО").pack(); fullname = ttk.Entry(win); fullname.pack()
        tk.Label(win,text="Телефон").pack(); phone = ttk.Entry(win); phone.pack()
        tk.Label(win,text="Email").pack(); email = ttk.Entry(win); email.pack()
        def save(): client_manager.add_client(fullname.get(),phone.get(),email.get()); self.load_clients(); win.destroy()
        ttk.Button(win,text="Сохранить",command=save).pack(pady=10)

    def edit_client(self):
        client_id = self.get_selected_client_id()
        if not client_id: messagebox.showwarning("Ошибка","Выберите клиента"); return
        values = self.client_tree.item(self.client_tree.selection()[0])["values"]
        win = tk.Toplevel(self.root); win.title("Редактировать клиента"); win.geometry("300x250")
        tk.Label(win,text="ФИО").pack(); fullname = ttk.Entry(win); fullname.pack(); fullname.insert(0,values[1])
        tk.Label(win,text="Телефон").pack(); phone = ttk.Entry(win); phone.pack(); phone.insert(0,values[2])
        tk.Label(win,text="Email").pack(); email = ttk.Entry(win); email.pack(); email.insert(0,values[3])
        def save(): client_manager.update_client(client_id, fullname.get(), phone.get(), email.get()); self.load_clients(); win.destroy()
        ttk.Button(win,text="Сохранить",command=save).pack(pady=10)

    def delete_client(self):
        client_id = self.get_selected_client_id()
        if not client_id: messagebox.showwarning("Ошибка","Выберите клиента"); return
        if messagebox.askyesno("Подтверждение","Удалить клиента?"): client_manager.delete_client(client_id); self.load_clients()

    # ========================= Автомобили =========================
    def create_vehicles_tab(self):
        columns = ("Id","Владелец","Марка","Модель","VIN","Госномер","Год","Пробег")
        self.vehicle_tree = ttk.Treeview(self.vehicles_frame, columns=columns, show="headings")
        for col in columns: self.vehicle_tree.heading(col,text=col); self.vehicle_tree.column(col,width=130)
        self.vehicle_tree.pack(fill="both", expand=True,padx=10,pady=10)

        btn_frame = tk.Frame(self.vehicles_frame); btn_frame.pack(pady=10)
        ttk.Button(btn_frame,text="Обновить",command=self.load_vehicles).grid(row=0,column=0,padx=5)
        ttk.Button(btn_frame,text="Добавить",command=self.add_vehicle).grid(row=0,column=1,padx=5)
        ttk.Button(btn_frame,text="Редактировать",command=self.edit_vehicle).grid(row=0,column=2,padx=5)
        ttk.Button(btn_frame,text="Удалить",command=self.delete_vehicle).grid(row=0,column=3,padx=5)

        self.load_vehicles()

    def load_vehicles(self): vehicle_manager.load_vehicles(self.vehicle_tree)

    def get_selected_vehicle_id(self):
        sel = self.vehicle_tree.selection()
        if not sel: return None
        try: return int(self.vehicle_tree.item(sel[0])["values"][0])
        except: return None

    def add_vehicle(self):
        # аналогично клиентам: окно с полями, выбор клиента из выпадающего списка
        pass

    def edit_vehicle(self):
        pass

    def delete_vehicle(self):
        vehicle_id = self.get_selected_vehicle_id()
        if not vehicle_id: messagebox.showwarning("Ошибка","Выберите авто"); return
        if messagebox.askyesno("Подтверждение","Удалить авто?"): vehicle_manager.delete_vehicle(vehicle_id); self.load_vehicles()


if __name__=="__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
