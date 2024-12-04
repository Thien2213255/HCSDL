import tkinter as tk
from tkinter import messagebox
import mysql.connector

def show_customer_data(customer_id, conn):
    try:
        # conn = mysql.connector.connect(
        #     host='localhost',
        #     user='root',
        #     password='1234',
        #     database='bank_db'
        # )
        cursor = conn.cursor(dictionary=True)
        
        #cursor.execute("SELECT * FROM (customer JOIN cusphonenumber ON customer.cuscode = cusphonenumber.cuscode) WHERE CUSCODE = %s", (customer_id,))
        cursor.execute(
            """
            SELECT 
                CONCAT(CFNAME, ' ', CLNAME) AS FULLNAME, 
                CEMAIL, 
                PHONENUMBER ,
                HOMEADDR
            FROM 
                customer 
            JOIN 
                cusphonenumber 
            ON 
                customer.cuscode = cusphonenumber.cuscode 
            WHERE 
                customer.CUSCODE = %s
            """, 
            (customer_id,)
        )
        customer_data = cursor.fetchone()
        # print("Fetched customer data:", customer_data)


        if not customer_data:
            messagebox.showerror("Error", "Customer not found!")
            conn.close()
            return

        # Lấy danh sách tài khoản của khách hàng
        cursor.execute("""
            SELECT ACCTYPE, COUNT(*) AS COUNT 
            FROM account 
            JOIN customer ON account.cuscode = customer.cuscode 
            WHERE customer.cuscode = %s 
            GROUP BY ACCTYPE
            """, (customer_id,))
        accounts = cursor.fetchall()
        conn.close()
        # accounts = cursor.fetchall()
        # account_list = [account["ACCTYPE"] for account in accounts]
        # conn.close()

        # Tạo cửa sổ hiển thị thông tin
        info_window = tk.Toplevel()
        info_window.title("Thông tin của khách hàng")
        info_window.geometry("800x400")

        # Tiêu đề
        tk.Label(info_window, text="Thông tin của khách hàng", font=("Arial", 16, "bold")).pack(pady=10)

        # Tạo frame để căn chỉnh
        frame = tk.Frame(info_window)
        frame.pack(pady=10, padx=20, fill="x")

        # Hàm tạo các dòng thông tin
        def create_info_row(label_text, value):
            row_frame = tk.Frame(frame)
            row_frame.pack(fill="x", pady=5)

            label = tk.Label(row_frame, text=label_text, font=("Arial", 12), anchor="w", width=25)
            label.pack(side="left")

            entry = tk.Entry(row_frame, font=("Arial", 12), readonlybackground="white")
            entry.pack(side="left", fill="x", expand=True, padx=5)
            entry.insert(0, value)


        # Hiển thị thông tin khách hàng
        create_info_row("Tên của khách hàng:", customer_data.get("FULLNAME", ""))
        create_info_row("Số điện thoại của khách hàng:", customer_data.get("PHONENUMBER", ""))
        create_info_row("Địa chỉ của khách hàng:", customer_data.get("HOMEADDR", ""))
        create_info_row("Email của khách hàng:", customer_data.get("CEMAIL", ""))

        # Tài khoản của khách hàng với thanh cuộn
        account_frame = tk.Frame(frame)
        account_frame.pack(fill="x", pady=5)

        label = tk.Label(account_frame, text="Tài khoản của khách hàng:", font=("Arial", 12), anchor="w", width=25)
        label.pack(side="left")

        # Tạo thanh cuộn
        account_scroll = tk.Scrollbar(account_frame, orient="vertical")
        account_listbox = tk.Listbox(account_frame, yscrollcommand=account_scroll.set, height=5, font=("Arial", 12))
        account_scroll.config(command=account_listbox.yview)
        account_scroll.pack(side="right", fill="y")
        account_listbox.pack(side="left", fill="x", expand=True)

        # Thêm tài khoản vào Listbox
        # for account in account_list:
        #     account_listbox.insert(tk.END, account)
        for account in accounts:
            account_type = account["ACCTYPE"]
            account_count = account["COUNT"]
            account_listbox.insert(tk.END, f"{account_type}: {account_count}")

        # Nút thoát
        # Nút thoát
        exit_button = tk.Button(info_window, text="Thoát", font=("Arial", 12), command=info_window.destroy)
        exit_button.pack(pady=10)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
