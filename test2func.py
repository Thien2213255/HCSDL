import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import re #thao tác với biểu thức chính quy

# Hàm hiển thị danh sách tài khoản checking
def show_checking_accounts(window, username, password, customer_id):
    # Tạo cửa sổ mới
    list_window = tk.Toplevel(window)
    list_window.title("Danh sách Checking accounts")
    list_window.geometry("400x400")
    list_window.grid_rowconfigure(0, weight=1)
    list_window.grid_columnconfigure(0, weight=1)

    # Tạo Frame để chứa thanh cuộn và dữ liệu
    frame = tk.Frame(list_window)
    frame.grid(row=0, column=0, sticky="nsew")

    # Tạo canvas để hỗ trợ cuộn
    canvas = tk.Canvas(frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Thanh cuộn dọc
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Gắn thanh cuộn vào canvas
    canvas.configure(yscrollcommand=scrollbar.set)

    # Frame con để đặt nội dung
    content_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=content_frame, anchor="w")

    # Kết nối MySQL và lấy dữ liệu
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user=username,
            password=password,
            database="bank_db"
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT checkingacc.ACCNUMBER, checkingacc.BALANCE, account.opendate FROM (account JOIN checkingacc ON checkingacc.ACCNUMBER = account.ACCNUMBER JOIN customer ON account.CUSCODE = customer.CUSCODE) where customer.CUSCODE = %s ORDER BY opendate DESC", (customer_id,))
        accounts = cursor.fetchall()
        conn.close()

        # Kiểm tra nếu không có tài khoản nào
        if not accounts:
            # Hiển thị thông báo không có tài khoản
            tk.Label(content_frame, text="Hiện chưa có tài khoản checking được thêm", 
                     font=("Times New Roman", 16), fg="black", justify="center").pack(pady=20)
        else:
            # Hiển thị danh sách tài khoản
            for i, account in enumerate(accounts):
                info = f"Số tài khoản: {account['ACCNUMBER']}\nSố dư: {account['BALANCE']}\nNgày tạo: {account['opendate']}\n"
                tk.Label(content_frame, text=info, font=("Times New Roman", 12), justify="left", anchor="w").grid(
                    row=i, column=0, sticky="w", padx=10, pady=5)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to retrieve data: {err}")

    # Điều chỉnh kích thước canvas
    content_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    canvas.yview_moveto(0)


def add_checking_account(window, username, password, customer_id):
    # Tạo cửa sổ con
    add_window = tk.Toplevel(window)
    add_window.title("Thêm tài khoản checking account")
    add_window.geometry("450x250")
    add_window.grid_rowconfigure(0, weight=1)
    add_window.grid_columnconfigure(0, weight=1)
    
    # Đặt cửa sổ con luôn ở phía trên
    add_window.transient(window)  # Liên kết với cửa sổ cha
    add_window.grab_set()         # Ngăn người dùng tương tác với cửa sổ chính
    add_window.lift()             # Đưa cửa sổ con lên phía trước

    # Tạo các widget nhập liệu
    tk.Label(add_window, text="Tạo tài khoản mới:", font=("Times New Roman", 14)).grid(row=0, column=0, pady=5, padx=(10, 5), sticky="w")
    acc_entry = tk.Entry(add_window, font=("Arial", 14), width=20)
    acc_entry.grid(row=0, column=1, pady=5, padx=10)

    tk.Label(add_window, text="Nhập số dư:", font=("Times New Roman", 14)).grid(row=1, column=0, pady=5, padx=(10, 5), sticky="w")
    balance_entry = tk.Entry(add_window, font=("Arial", 14))
    balance_entry.grid(row=1, column=1, pady=5, padx=10)

    # Hàm kiểm tra định dạng tài khoản
    def is_valid_accnumber(acc_number):
        pattern = r"^ACC\d{3}$"  # Định dạng ACCxxx
        return re.match(pattern, acc_number) is not None

    # Hàm xử lý thêm tài khoản
    def save_account():
        acc_number = acc_entry.get()
        balance = balance_entry.get()

        # Kiểm tra tài khoản có đúng định dạng không
        if not is_valid_accnumber(acc_number):
            messagebox.showwarning("Input Error", "Tài khoản sai định dạng! Định dạng hợp lệ: ACCxxx (ví dụ: ACC001).")
            # Đưa cửa sổ con trở lại phía trước sau khi messagebox đóng
            add_window.lift()
            return

        # Kiểm tra số dư có phải là số hay không
        if not balance.isdigit():
            messagebox.showwarning("Input Error", "Số dư phải là một số!")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user=username,
                password=password,
                database="bank_db"
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO account (ACCNUMBER, CUSCODE, ACCTYPE, opendate) VALUES (%s, %s, %s, NOW())",
                           (acc_number, customer_id, "Checking"))
            cursor.execute("INSERT INTO checkingacc (ACCNUMBER, BALANCE) VALUES (%s, %s)",
                           (acc_number, balance))
            conn.commit()
            
            conn.close()
            messagebox.showinfo("Thông báo", "Thêm tài khoản thành công!")
            add_window.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to insert data: {err}")
            # Đưa cửa sổ con trở lại phía trước sau khi messagebox đóng
            add_window.lift()

    # Nút xác nhận thêm tài khoản
    save_button = tk.Button(add_window, text="Xác nhận thêm tài khoản", command=save_account, font=("Arial", 14), bg="lightblue")
    save_button.grid(row=2, column=0, columnspan=2, pady=20)

#---------------------------------SAVING ACCOUNT---------------------------------------



def show_saving_accounts(window, username, password, customer_id):
    # Tạo cửa sổ mới
    list_window = tk.Toplevel(window)
    list_window.title("Danh sách Saving accounts")
    list_window.geometry("400x400")
    list_window.grid_rowconfigure(0, weight=1)
    list_window.grid_columnconfigure(0, weight=1)

    # Tạo Frame để chứa thanh cuộn và dữ liệu
    frame = tk.Frame(list_window)
    frame.grid(row=0, column=0, sticky="nsew")

    # Tạo canvas để hỗ trợ cuộn
    canvas = tk.Canvas(frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Thanh cuộn dọc
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Gắn thanh cuộn vào canvas
    canvas.configure(yscrollcommand=scrollbar.set)

    # Frame con để đặt nội dung
    content_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=content_frame, anchor="w")

    # Kết nối MySQL và lấy dữ liệu
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user=username,
            password=password,
            database="bank_db"
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT savingacc.ACCNUMBER, savingacc.BALANCE, account.opendate FROM (account JOIN savingacc ON savingacc.ACCNUMBER = account.ACCNUMBER JOIN customer ON account.CUSCODE = customer.CUSCODE) where customer.CUSCODE = %s ORDER BY opendate DESC", (customer_id,))
        accounts = cursor.fetchall()
        conn.close()

        # Kiểm tra nếu không có tài khoản nào
        if not accounts:
            # Hiển thị thông báo không có tài khoản
            tk.Label(content_frame, text="Hiện chưa có tài khoản saving được thêm", 
                     font=("Times New Roman", 16), fg="black", justify="center").pack(pady=20)
        else:
            # Hiển thị danh sách tài khoản
            for i, account in enumerate(accounts):
                info = f"Số tài khoản: {account['ACCNUMBER']}\nSố dư: {account['BALANCE']}\nNgày tạo: {account['opendate']}\n"
                tk.Label(content_frame, text=info, font=("Times New Roman", 12), justify="left", anchor="w").grid(
                    row=i, column=0, sticky="w", padx=10, pady=5)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to retrieve data: {err}")

    # Điều chỉnh kích thước canvas
    content_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    canvas.yview_moveto(0)


def add_saving_account(window, username, password, customer_id):
    # Tạo cửa sổ con
    add_window = tk.Toplevel(window)
    add_window.title("Thêm tài khoản saving account")
    add_window.geometry("450x250")
    add_window.grid_rowconfigure(0, weight=1)
    add_window.grid_columnconfigure(0, weight=1)
    
    # Đặt cửa sổ con luôn ở phía trên
    add_window.transient(window)  # Liên kết với cửa sổ cha
    add_window.grab_set()         # Ngăn người dùng tương tác với cửa sổ chính
    add_window.lift()             # Đưa cửa sổ con lên phía trước

    # Tạo các widget nhập liệu
    tk.Label(add_window, text="Tạo tài khoản mới:", font=("Times New Roman", 14)).grid(row=0, column=0, pady=5, padx=(10, 5), sticky="w")
    acc_entry = tk.Entry(add_window, font=("Arial", 14), width=20)
    acc_entry.grid(row=0, column=1, pady=5, padx=10)

    tk.Label(add_window, text="Nhập số dư:", font=("Times New Roman", 14)).grid(row=1, column=0, pady=5, padx=(10, 5), sticky="w")
    balance_entry = tk.Entry(add_window, font=("Arial", 14))
    balance_entry.grid(row=1, column=1, pady=5, padx=10)

    # Hàm kiểm tra định dạng tài khoản
    def is_valid_accnumber(acc_number):
        pattern = r"^ACC\d{3}$"  # Định dạng ACCxxx
        return re.match(pattern, acc_number) is not None

    # Hàm xử lý thêm tài khoản
    def save_account():
        acc_number = acc_entry.get()
        balance = balance_entry.get()

        # Kiểm tra tài khoản có đúng định dạng không
        if not is_valid_accnumber(acc_number):
            messagebox.showwarning("Input Error", "Tài khoản sai định dạng! Định dạng hợp lệ: ACCxxx (ví dụ: ACC001).")
            # Đưa cửa sổ con trở lại phía trước sau khi messagebox đóng
            add_window.lift()
            return

        # Kiểm tra số dư có phải là số hay không
        if not balance.isdigit():
            messagebox.showwarning("Input Error", "Số dư phải là một số!")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user=username,
                password=password,
                database="bank_db"
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO account (ACCNUMBER, CUSCODE, ACCTYPE, opendate) VALUES (%s, %s, %s, NOW())",
                           (acc_number, customer_id, "Checking"))
            cursor.execute("INSERT INTO savingacc (ACCNUMBER, BALANCE) VALUES (%s, %s)",
                           (acc_number, balance))
            conn.commit()
            
            conn.close()
            messagebox.showinfo("Thông báo", "Thêm tài khoản thành công!")
            add_window.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to insert data: {err}")
            # Đưa cửa sổ con trở lại phía trước sau khi messagebox đóng
            add_window.lift()

    # Nút xác nhận thêm tài khoản
    save_button = tk.Button(add_window, text="Xác nhận thêm tài khoản", command=save_account, font=("Arial", 14), bg="lightblue")
    save_button.grid(row=2, column=0, columnspan=2, pady=20)
    
#------------------------------------------LOAN ACCOUNT--------------------------------------------



def show_loan_accounts(window, username, password, customer_id):
    # Tạo cửa sổ mới
    list_window = tk.Toplevel(window)
    list_window.title("Danh sách Loan accounts")
    list_window.geometry("400x400")
    list_window.grid_rowconfigure(0, weight=1)
    list_window.grid_columnconfigure(0, weight=1)

    # Tạo Frame để chứa thanh cuộn và dữ liệu
    frame = tk.Frame(list_window)
    frame.grid(row=0, column=0, sticky="nsew")

    # Tạo canvas để hỗ trợ cuộn
    canvas = tk.Canvas(frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Thanh cuộn dọc
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Gắn thanh cuộn vào canvas
    canvas.configure(yscrollcommand=scrollbar.set)

    # Frame con để đặt nội dung
    content_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=content_frame, anchor="w")

    # Kết nối MySQL và lấy dữ liệu
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user=username,
            password=password,
            database="bank_db"
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT loanacc.ACCNUMBER, loanacc.BALANCE, loanacc.INSRATE, account.opendate FROM (account JOIN loanacc ON loanacc.ACCNUMBER = account.ACCNUMBER JOIN customer ON account.CUSCODE = customer.CUSCODE) where customer.CUSCODE = %s ORDER BY opendate DESC", (customer_id,))
        accounts = cursor.fetchall()
        conn.close()

        # Kiểm tra nếu không có tài khoản nào
        if not accounts:
            # Hiển thị thông báo không có tài khoản
            tk.Label(content_frame, text="Hiện chưa có tài khoản loan được thêm", 
                     font=("Times New Roman", 16), fg="black", justify="center").pack(pady=20)
        else:
            # Hiển thị danh sách tài khoản
            for i, account in enumerate(accounts):
                info = f"Số tài khoản: {account['ACCNUMBER']}\nSố dư: {account['BALANCE']}\nLãi suất: {account['INSRATE']}%\nNgày tạo: {account['opendate']}\n"
                tk.Label(content_frame, text=info, font=("Times New Roman", 12), justify="left", anchor="w").grid(
                    row=i, column=0, sticky="w", padx=10, pady=5)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to retrieve data: {err}")

    # Điều chỉnh kích thước canvas
    content_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    canvas.yview_moveto(0)

def add_loan_account(window, username, password, customer_id):
    # Tạo cửa sổ con
    add_window = tk.Toplevel(window)
    add_window.title("Thêm tài khoản loan account")
    add_window.geometry("450x350")

    # Căn chỉnh các hàng và cột
    for i in range(3):
        add_window.grid_rowconfigure(i, weight=1)  # Đảm bảo cân bằng chiều cao hàng
    add_window.grid_columnconfigure(0, weight=1)  # Căn trái
    add_window.grid_columnconfigure(1, weight=1)  # Căn phải

    # Đặt cửa sổ con luôn ở phía trên
    add_window.transient(window)  # Liên kết với cửa sổ cha
    add_window.grab_set()         # Ngăn người dùng tương tác với cửa sổ chính
    add_window.lift()             # Đưa cửa sổ con lên phía trước

    # Tạo các widget nhập liệu
    tk.Label(add_window, text="Số tài khoản:", font=("Times New Roman", 14)).grid(row=0, column=0, pady=10, padx=5, sticky="e")
    acc_entry = tk.Entry(add_window, font=("Arial", 14), width=20)
    acc_entry.grid(row=0, column=1, pady=10, padx=5, sticky="w")

    tk.Label(add_window, text="Số dư:", font=("Times New Roman", 14)).grid(row=1, column=0, pady=10, padx=5, sticky="e")
    balance_entry = tk.Entry(add_window, font=("Arial", 14), width=20)
    balance_entry.grid(row=1, column=1, pady=10, padx=5, sticky="w")
    
    tk.Label(add_window, text="Lãi suất:", font=("Times New Roman", 14)).grid(row=2, column=0, pady=10, padx=5, sticky="e")
    ins_entry = tk.Entry(add_window, font=("Arial", 14), width=20)
    ins_entry.grid(row=2, column=1, pady=10, padx=5, sticky="w")

    # Hàm kiểm tra định dạng tài khoản
    def is_valid_accnumber(acc_number):
        pattern = r"^ACC\d{3}$"  # Định dạng ACCxxx
        return re.match(pattern, acc_number) is not None

    # Hàm xử lý thêm tài khoản
    def save_account():
        acc_number = acc_entry.get()
        balance = balance_entry.get()
        rate = ins_entry.get()

        # Kiểm tra tài khoản có đúng định dạng không
        if not is_valid_accnumber(acc_number):
            messagebox.showwarning("Input Error", "Tài khoản sai định dạng! Định dạng hợp lệ: ACCxxx (ví dụ: ACC001).")
            add_window.lift()
            return

        # Kiểm tra số dư có phải là số hay không
        if not balance.isdigit():
            messagebox.showwarning("Input Error", "Số dư phải là một số!")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user=username,
                password=password,
                database="bank_db"
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO account (ACCNUMBER, CUSCODE, ACCTYPE, opendate) VALUES (%s, %s, %s, NOW())",
                           (acc_number, customer_id, "Checking"))
            cursor.execute("INSERT INTO loanacc (ACCNUMBER, BALANCE, INSRATE) VALUES (%s, %s, %s)",
                           (acc_number, balance, rate))
            conn.commit()
            
            conn.close()
            messagebox.showinfo("Thông báo", "Thêm tài khoản thành công!")
            add_window.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to insert data: {err}")
            add_window.lift()

    # Nút xác nhận thêm tài khoản
    save_button = tk.Button(add_window, text="Xác nhận thêm tài khoản", command=save_account, font=("Arial", 14), bg="lightblue")
    save_button.grid(row=3, column=0, columnspan=2, pady=20)


# def add_loan_account(window, username, password, customer_id):
#     # Tạo cửa sổ con
#     add_window = tk.Toplevel(window)
#     add_window.title("Thêm tài khoản loan account")
#     add_window.geometry("450x350")
#     add_window.grid_rowconfigure(0, weight=1)
#     add_window.grid_columnconfigure(0, weight=1)
    
#     # Đặt cửa sổ con luôn ở phía trên
#     add_window.transient(window)  # Liên kết với cửa sổ cha
#     add_window.grab_set()         # Ngăn người dùng tương tác với cửa sổ chính
#     add_window.lift()             # Đưa cửa sổ con lên phía trước

#     # Tạo các widget nhập liệu
#     tk.Label(add_window, text="Tạo tài khoản mới:", font=("Times New Roman", 14)).grid(row=0, column=0, pady=5, padx=(10, 5), sticky="w")
#     acc_entry = tk.Entry(add_window, font=("Arial", 14), width=20)
#     acc_entry.grid(row=0, column=1, pady=5, padx=10)

#     tk.Label(add_window, text="Nhập số dư:", font=("Times New Roman", 14)).grid(row=1, column=0, pady=5, padx=(10, 5), sticky="w")
#     balance_entry = tk.Entry(add_window, font=("Arial", 14))
#     balance_entry.grid(row=1, column=1, pady=5, padx=10)
    
#     tk.Label(add_window, text="Nhập lãi suất:", font=("Times New Roman", 14)).grid(row=2, column=0, pady=5, padx=(10, 5), sticky="w")
#     ins_entry = tk.Entry(add_window, font=("Arial", 14))
#     ins_entry.grid(row=2, column=1, pady=5, padx=10)

#     # Hàm kiểm tra định dạng tài khoản
#     def is_valid_accnumber(acc_number):
#         pattern = r"^ACC\d{3}$"  # Định dạng ACCxxx
#         return re.match(pattern, acc_number) is not None

#     # Hàm xử lý thêm tài khoản
#     def save_account():
#         acc_number = acc_entry.get()
#         balance = balance_entry.get()
#         rate = ins_entry.get()

#         # Kiểm tra tài khoản có đúng định dạng không
#         if not is_valid_accnumber(acc_number):
#             messagebox.showwarning("Input Error", "Tài khoản sai định dạng! Định dạng hợp lệ: ACCxxx (ví dụ: ACC001).")
#             # Đưa cửa sổ con trở lại phía trước sau khi messagebox đóng
#             add_window.lift()
#             return

#         # Kiểm tra số dư có phải là số hay không
#         if not balance.isdigit():
#             messagebox.showwarning("Input Error", "Số dư phải là một số!")
#             return

#         try:
#             conn = mysql.connector.connect(
#                 host="localhost",
#                 user=username,
#                 password=password,
#                 database="bank_db"
#             )
#             cursor = conn.cursor()
#             cursor.execute("INSERT INTO account (ACCNUMBER, CUSCODE, ACCTYPE, opendate) VALUES (%s, %s, %s, NOW())",
#                            (acc_number, customer_id, "Checking"))
#             cursor.execute("INSERT INTO loanacc (ACCNUMBER, BALANCE, INSRATE) VALUES (%s, %s, %s)",
#                            (acc_number, balance, rate))
#             conn.commit()
            
#             conn.close()
#             messagebox.showinfo("Thông báo", "Thêm tài khoản thành công!")
#             add_window.destroy()
#         except mysql.connector.Error as err:
#             messagebox.showerror("Database Error", f"Failed to insert data: {err}")
#             # Đưa cửa sổ con trở lại phía trước sau khi messagebox đóng
#             add_window.lift()

#     # Nút xác nhận thêm tài khoản
#     save_button = tk.Button(add_window, text="Xác nhận thêm tài khoản", command=save_account, font=("Arial", 14), bg="lightblue")
#     save_button.grid(row=2, column=0, columnspan=2, pady=20)

# def show_saving_accounts(window, data):
#     pass
# def add_saving_account(window):
#     pass

# def show_loan_accounts(window, data):
#     pass
# def add_loan_account(window):
#     pass
# # Tạo một ví dụ để hiển thị
# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("Accounts Management")
#     root.geometry("500x500")

#     # Dữ liệu mẫu để kết nối database
#     db_data = {"username": "root", "password": "1234"}

#     # Giao diện chính
#     button_font = ("Arial", 16)
#     tk.Button(root, text="List Checking Accounts", command=lambda: show_checking_accounts(root, db_data, "d369d27a-ad63-11ef-bb6e-00155d23183c"), font=button_font).pack(pady=20)
#     tk.Button(root, text="Add Checking Account", command=lambda: add_checking_account(root, db_data, 'd369d27a-ad63-11ef-bb6e-00155d23183c'), font=button_font).pack(pady=20)

#     root.mainloop()
