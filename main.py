import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
#from generate_report import open_generate_report_window
from customerdata import show_customer_data
from generate_report import open_generate_report_window
from listaccount import show_accounts_table

# Hàm để căn chỉnh cửa sổ chính giữa màn hình
def center_window(window, width=400, height=400):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")




class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None

    def connect(self):
        if not self.conn or not self.conn.is_connected():
            try:
                self.conn = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
            except Error as e:
                raise Exception(f"Failed to connect to database: {e}")

    def get_cursor(self):
        self.connect()  # Đảm bảo kết nối còn hoạt động
        return self.conn.cursor(dictionary=True)

    def get_conn(self):
        self.connect()  # Đảm bảo kết nối còn hoạt động
        return self.conn 
    def close(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()

global_username = None
global_password = None

# Hàm cấp quyền cho người dùng Manager
def grant_privileges_to_manager(username, password):
    try:
        # Kết nối với MySQL bằng tài khoản SYS hoặc SYSTEM
        conn = mysql.connector.connect(
            host="localhost",
            user=username,  # Tài khoản với quyền DBA (thay thế nếu không dùng root)
            password=password, 
            database = "bank_db"
        )
        cursor = conn.cursor()

        # Tạo user Manager (nếu chưa tồn tại) và cấp quyền
        cursor.execute("CREATE USER IF NOT EXISTS 'Manager'@'localhost' IDENTIFIED BY 'manager123';")
        cursor.execute("GRANT ALL PRIVILEGES ON *.* TO 'Manager'@'localhost' WITH GRANT OPTION;")
        cursor.execute("FLUSH PRIVILEGES;")
        

        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Success", "All privileges have been granted to 'Manager'.")
        
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to grant privileges: {err}")

# Hàm xác thực
def authenticate():
    global global_username, global_password 
    username = username_entry.get()
    password = password_entry.get()
    try:
        # Kết nối với MySQL để kiểm tra tài khoản
        connm = mysql.connector.connect(
            host="localhost",
            user=username,
            password=password
        )
        connm.close()


        if username == "root":  # Kiểm tra nếu tài khoản là DBA
            global_username = username
            global_password = password 
            messagebox.showinfo("Authentication", "Login successful!")
            grant_privileges_to_manager(username, password)
            login_window.destroy() #cửa sổ login phải tắt thì main_window mới hiện lên

            # Gọi hàm cấp quyền cho user Manager
            

            # Tiếp tục hiển thị giao diện chính
            main_window()
        else:
            messagebox.showerror("Authentication", "You do not have sufficient privileges.")
    except mysql.connector.Error as err:
        messagebox.showerror("Authentication", f"Login failed: {err}")

# Hàm tạo cửa sổ chính
def main_window():
    def open_actions_window():
        # Cửa sổ có các button chức năng
        actions_window = tk.Toplevel()
        actions_window.title("Actions Window")
        center_window(actions_window, width=500, height=500)
        # Hàm xử lý khi nhấn nút "Customer Info"
        def show_customer_info():
            try: 
                conn = mysql.connector.connect(
                    host='localhost',
                    user=global_username,
                    password=global_password,
                    database='bank_db'
                )
                show_customer_data(customer_id, conn)
                
        
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
        def show_employee_info():
            try: 
                conn = mysql.connector.connect(
                    host='localhost',
                    user=global_username,
                    password=global_password,
                    database='bank_db'
                )
                cursor = conn.cursor()
                open_generate_report_window(cursor, customer_id_entry)
                
        
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
        def show_account():
            try: 
                show_accounts_table(global_username, global_password, customer_id)
                
        
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
        def go_back():
        # """Hàm xử lý khi nhấn nút 'Quay trở lại'."""
            actions_window.destroy()  # Đóng cửa sổ hiện tại

        # Các nút chức năng
        button_font = ("Arial", 14)  # Font chữ cho các button
        tk.Button(actions_window, text="Thông tin cá nhân khách hàng", command=show_customer_info, font=button_font, width=35).pack(padx=20, pady=50)
        tk.Button(actions_window, text="Thông tin dịch vụ chăm sóc khách hàng", command= show_employee_info, font=button_font, width=35).pack(padx=20, pady=50)  # Chưa xử lý
        tk.Button(actions_window, text="Thông tin tài khoản khách hàng", command=show_account, font=button_font, width=35).pack(padx=20, pady=50)  # Chưa xử lý
        back_button = tk.Button(actions_window, text=" Quay trở lại trang chính", command=go_back, font=button_font, width=35)
        back_button.pack(pady=20)

    def search_customer():
        global customer_id
        customer_id = customer_id_entry.get()
        
        if not customer_id:
            messagebox.showwarning("Input Error", "Please enter a customer ID!")
            return

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user=global_username,
                password=global_password,
                database='bank_db'
            )
            cursor = conn.cursor()
            # Kiểm tra sự tồn tại của customer_id
            cursor.execute("SELECT CUSCODE FROM customer WHERE CUSCODE = %s", (customer_id,))
            result = cursor.fetchone()
            
            if result:  # Nếu tìm thấy khách hàng
                open_actions_window()
            else:  # Không tìm thấy khách hàng
                messagebox.showerror("Error", "Không tìm thấy khách hàng. Vui lòng nhập lại ID.")
            
            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Database connection failed: {err}")

            
    def logout():
        """Hàm xử lý khi nhấn nút Đăng xuất."""
        if messagebox.askokcancel("Xác nhận", "Bạn có chắc chắn muốn đăng xuất không?"):
            main_win.destroy()  # Đóng tất cả cửa sổ
            
    

    main_win = tk.Tk()
    main_win.title("Main Window")
    center_window(main_win, width=500, height=500)

    # Căn giữa các widget
    main_win.grid_rowconfigure(0, weight=1)
    main_win.grid_rowconfigure(1, weight=1)
    main_win.grid_columnconfigure(0, weight=1)
    main_win.grid_columnconfigure(1, weight=1)

    label_font = ("Arial", 14)  # Font chữ cho label
    tk.Label(main_win, text="Nhập ID khách hàng", font=label_font, width=20, relief=tk.SOLID, border=1).grid(row=0, column=0, padx=10, pady=10)
    customer_id_entry = tk.Entry(main_win, font=("Arial", 14), width=20)
    customer_id_entry.grid(row=0, column=1, padx=10, pady=10)

    button_font = ("Arial", 14)  # Font chữ cho button
    tk.Button(main_win, text="Tìm kiếm", command=search_customer, font=button_font, width=10).grid(row=1, column=0, columnspan=2, pady=20)
    
    # Nút "Đăng xuất"
    tk.Button(main_win, text="Đăng xuất", command=logout, font=button_font, width=10).grid(row=2, column=0, columnspan=2, pady=20)

    main_win.mainloop()

# Tạo cửa sổ đăng nhập
login_window = tk.Tk()
login_window.title("Manager Authentication")
center_window(login_window, width=400, height=400)

# Căn giữa các widget trong cửa sổ đăng nhập
login_window.grid_rowconfigure(0, weight=1)
login_window.grid_rowconfigure(1, weight=1)
login_window.grid_rowconfigure(2, weight=1)
login_window.grid_columnconfigure(0, weight=1)
login_window.grid_columnconfigure(1, weight=1)

label_font = ("Arial", 14)  # Font chữ cho label
entry_font = ("Arial", 14)  # Font chữ cho entry
button_font = ("Arial", 14)  # Font chữ cho button

tk.Label(login_window, text="Username:", font=label_font).grid(row=0, column=0, padx=10, pady=10)
username_entry = tk.Entry(login_window, font=entry_font)
username_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(login_window, text="Password:", font=label_font).grid(row=1, column=0, padx=10, pady=10)
password_entry = tk.Entry(login_window, show="*", font=entry_font)
password_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Button(login_window, text="Login", command=authenticate, font=button_font, width=10).grid(row=2, column=0, columnspan=2, pady=20)

login_window.mainloop()
