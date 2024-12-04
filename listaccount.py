import tkinter as tk
from tkinter import ttk
from test2func import show_checking_accounts, add_checking_account
from test2func import show_saving_accounts, add_saving_account
from test2func import show_loan_accounts, add_loan_account

def show_accounts_table(username, password, customer_id):
    window = tk.Tk()
    window.title("Accounts Table")
    window.geometry("700x400")
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)

    # Font chữ lớn hơn
    label_font = ("Arial", 18, "bold")
    button_font = ("Arial", 16)
    button_width = 25  # Độ rộng của nút

    # Tạo nhãn Checking Accounts
    checking_label = tk.Label(window, text="Tài khoản Checking", font=label_font)
    checking_label.grid(row=0, column=0, columnspan=2, pady=20, sticky="n")

    # Tạo 2 nút cho Checking Accounts
    list_button = tk.Button(window, text="Danh sách tài khoản Checking", command=lambda: show_checking_accounts(window, username, password, customer_id), font=button_font, width=button_width)
    list_button.grid(row=1, column=0, pady=10, padx=20, sticky="n")
    add_button = tk.Button(window, text="Thêm tài khoản Checking", command=lambda: add_checking_account(window, username, password, customer_id), font=button_font, width=button_width)
    add_button.grid(row=1, column=1, pady=10, padx=20, sticky="n")

    # Tạo nhãn Saving Accounts
    saving_label = tk.Label(window, text="Tài khoản Saving", font=label_font)
    saving_label.grid(row=2, column=0, columnspan=2, pady=20, sticky="n")

    # Tạo 2 nút cho Saving Accounts
    list_button = tk.Button(window, text="Danh sách tài khoản Saving", command=lambda: show_saving_accounts(window, username, password, customer_id), font=button_font, width=button_width)
    list_button.grid(row=3, column=0, pady=10, padx=20, sticky="n")
    add_button = tk.Button(window, text="Thêm tài khoản Saving", command=lambda: add_saving_account(window, username, password, customer_id), font=button_font, width=button_width)
    add_button.grid(row=3, column=1, pady=10, padx=20, sticky="n")

    # Tạo nhãn Loan Accounts
    loan_label = tk.Label(window, text="Tài khoản Loan", font=label_font)
    loan_label.grid(row=4, column=0, columnspan=2, pady=20, sticky="n")

    # Tạo 2 nút cho Loan Accounts
    list_button = tk.Button(window, text="Danh sách tài khoản Loan", command=lambda: show_loan_accounts(window, username, password, customer_id), font=button_font, width=button_width)
    list_button.grid(row=5, column=0, pady=10, padx=20, sticky="n")
    add_button = tk.Button(window, text="Thêm tài khoản Loan", command=lambda: add_loan_account(window, username, password, customer_id), font=button_font, width=button_width)
    add_button.grid(row=5, column=1, pady=10, padx=20, sticky="n")


    # Căn giữa toàn bộ nội dung trong cửa sổ
    for row in range(6):
        window.grid_rowconfigure(row, weight=1)
        # Nút thoát


# Dữ liệu mẫu
# data = [
#     ("123456", "C001", "Savings", "2023-01-01"),
#     ("234567", "C002", "Checking", "2022-12-31"),
#     ("345678", "C003", "Savings", "2023-02-15"),
# ]

# # Tạo cửa sổ chính
# root = tk.Tk()
# root.title("Accounts Table")
# root.geometry("600x400")

# show_accounts_table(root, data)

# root.mainloop()
