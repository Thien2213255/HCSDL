import mysql.connector
import tkinter as tk
from tkinter import ttk

#=========================================== src cho phần generate report ======================================================================

# def create_table(window, data):
#      # Tạo bảng Treeview
#     tree = ttk.Treeview(window, height=5)


# 	# Định nghĩa các cột
#     tree["columns"] = ("ID", "Ngày sinh", "Email", "Họ", "Tên", "Số nhà", "Đường", "Quận/Huyện", "Tỉnh/Thành phố", "Tên chi nhánh làm việc")
    
#     #set định dạng cho mỗi cột
#     tree.column("#0",                     width=50,      anchor="center")
#     tree.column("ID",                     width=100,      anchor="center")
#     tree.column("Ngày sinh",              width=100,      anchor="center")
#     tree.column("Email",                  width=200,      anchor="center")
#     tree.column("Họ",                     width=100,      anchor="center")
#     tree.column("Tên",                    width=100,      anchor="center")
#     tree.column("Số nhà",                 width=100,      anchor="center")
#     tree.column("Đường",                  width=100,      anchor="center")
#     tree.column("Quận/Huyện",             width=100,      anchor="center")
#     tree.column("Tỉnh/Thành phố",         width=100,      anchor="center")
#     tree.column("Tên chi nhánh làm việc", width=200,      anchor="center")

#     # Đặt tiêu đề cho các cột
#     tree.heading("#0",                    text="STT")
#     tree.heading("ID",                    text="ID")
#     tree.heading("Ngày sinh",             text="Ngày sinh")
#     tree.heading("Email",                 text="Email")
#     tree.heading("Họ",                    text="Họ")
#     tree.heading("Tên",                   text="Tên")    
#     tree.heading("Số nhà",                text="Số nhà")
#     tree.heading("Đường",                 text="Đường")
#     tree.heading("Quận/Huyện",            text="Quận/Huyện")
#     tree.heading("Tỉnh/Thành phố",        text="Tỉnh/Thành phố")
#     tree.heading("Tên chi nhánh làm việc",text="Tên chi nhánh làm việc")

#     #insert data vào bảng
#     for item in data:
#         tree.insert("", "end", text="1", values=item[0:])

#     #đặt bảng vào màn 
#     tree.grid(row=2, column=0, sticky="nsew")


# def open_generate_report_window(cursor, entry):   # để tiện cho cpy paste (main frame, tên cursor kết nối với db, entry chứa cuscode)

# 	#truy xuất dữ liệu nhân viên
# 	CUSCODE = entry.get()
# 	query = "SELECT * FROM EMPLOYEE WHERE EMPLOYEECODE IN (SELECT EMPLOYEECODE FROM CUSTOMER WHERE CUSCODE = %s)"
# 	cursor.execute(query, (CUSCODE,))
# 	result = cursor.fetchall()
# 	#đóng cửa sổ chính
# 	# root.withdraw()

# 	#tạo cửa sổ mới
# 	generate_report_window = tk.Toplevel()
# 	generate_report_window.title("Employee Information")
	

# 	# Nếu không có dữ liệu, hiển thị thông báo
# 	if not result:
# 		generate_report_window.geometry("300x100")
# 		label = tk.Label(generate_report_window, text="Xin hãy kiểm tra lại mã khách hàng", font=("Arial", 10, "bold"), fg="red")
# 		label.grid(row=0, column=0, padx=10, pady=10)
# 	else:
#         # In ra thông tin nhân viên
# 		generate_report_window.geometry("1250x400")
# 		label = tk.Label(generate_report_window, text="Thông tin nhân viên phục vụ của khách hàng ", font=("Arial", 10))
# 		label.grid(row=0, column=0)


#         # Tạo bảng và hiển thị dữ liệu
# 		create_table(generate_report_window, result)

# 	# Tạo nút thoát
# 	#button = tk.Button(generate_report_window, text = "Complete")
# 	#button.grid(row=4,column=0, padx=10, pady=10)

import tkinter as tk
from tkinter import ttk

def create_table(window, data, r, c):
    # Tạo bảng Treeview
    tree = ttk.Treeview(window, height=len(data))

    # Định nghĩa các cột
    tree["columns"] = ("Attribute", "Value")

    # Đặt định dạng cho mỗi cột
    tree.column("#0", width=40, anchor="center")
    tree.column("Attribute", width=125, anchor="w")
    tree.column("Value", width=200, anchor="w")

    # Đặt tiêu đề cho các cột
    tree.heading("#0", text="STT")
    tree.heading("Attribute", text="Thuộc tính")
    tree.heading("Value", text="Giá trị")

    # Chèn dữ liệu vào bảng
    for idx, item in enumerate(data):
        tree.insert("", "end", text=f"{idx + 1}", values=item)

    # Đặt bảng vào màn hình
    tree.grid(row=r, column=c, sticky="nsew", pady = 5, padx = 5)


def open_generate_report_window(cursor, entry):
    

    # Truy xuất thông tin nhân viên
    CUSCODE = entry.get()
    query = "SELECT * FROM EMPLOYEE WHERE EMPLOYEECODE IN (SELECT EMPLOYEECODE FROM CUSTOMER WHERE CUSCODE = %s)"
    cursor.execute(query, (CUSCODE,))
    result1 = cursor.fetchall()

    # Truy xuất số điện thoại
    EMPLOYEECODE = result1[0][0]
    query = "SELECT PHONENUMBER FROM EMPLOYEEPHONENUMBER WHERE EMPLOYEECODE = %s"
    cursor.execute(query, (EMPLOYEECODE,))
    result2 = cursor.fetchall()

    # Truy xuất thông tin branch
    EMPLOYEECODE = result1[0][0]
    query = "SELECT * FROM BRANCH WHERE BNAME IN (SELECT BNAME FROM EMPLOYEE WHERE EMPLOYEECODE = %s)"
    cursor.execute(query, (EMPLOYEECODE,))
    result3 = cursor.fetchall()
    
    # Truy xuất số điện thoại branch
    BNAME =  result3[0][0]
    query = "SELECT PHONENUMBER FROM BRANCHPHONE WHERE BNAME = %s"
    cursor.execute(query, (BNAME,))
    result4 = cursor.fetchall()

    # Truy xuất số fax branch
    BNAME = result3[0][0]
    query = "SELECT FAXNUMBER FROM BRANCHFAX WHERE BNAME = %s"
    cursor.execute(query, (BNAME,))
    result5 = cursor.fetchall()

    # Truy xuất thông tin nhân viên quản lý
    EMPLOYEECODE = result3[0][7]
    query = "SELECT * FROM EMPLOYEE WHERE EMPLOYEECODE = %s"
    cursor.execute(query, (EMPLOYEECODE,))
    result6 = cursor.fetchall()

    # Truy xuất số điện thoại nhân viên quản lý
    EMPLOYEECODE = result3[0][7]
    query = "SELECT PHONENUMBER FROM EMPLOYEEPHONENUMBER WHERE EMPLOYEECODE = %s"
    cursor.execute(query, (EMPLOYEECODE,))
    result7 = cursor.fetchall()


    # Tạo cửa sổ mới
    generate_report_window = tk.Toplevel()
    generate_report_window.title("Employee Information")

    if not result1:
        generate_report_window.geometry("300x100")
        label = tk.Label(
            generate_report_window,
            text="Không tìm thấy thông tin nhân viên. Vui lòng kiểm tra lại mã khách hàng.",
            font=("Arial", 10, "bold"),
            fg="red",
        )
        label.grid(row=0, column=0, padx=10, pady=10)
    else:
        generate_report_window.geometry("1140x400")

        # Xử lý dữ liệu
        employee_data = result1[0] 
        employee_phone = []
        for row in result2:
            for col in row:
                employee_phone.append(col)
        branch_data = result3[0]
        branch_phone = []
        for row in result4:
            for col in row:
                branch_phone.append(col)
        branch_fax = []
        for row in result5:
            for col in row:
                branch_fax.append(col)
        manager_data = result6[0]
        manager_phone = []
        for row in result7:
            for col in row:
                manager_phone.append(col)

        label = tk.Label(
            generate_report_window,
            text="Thông tin nhân viên phục vụ của khách hàng",
            font=("Arial", 10, "bold"),
        )
        label.grid(row=0, column=0)

        # Định dạng và hiển thị dữ liệu
        employee_attr = [
            "EMPLOYEECODE", "DOB", "Email", "Last Name", "First Name",
            "House Number", "Street", "District", "City", "Branch Name"
        ]
        formatted_employee_data = [
            (employee_attr[i], str(employee_data[i])) for i in range(len(employee_data))
        ]


        # Employee phonenumbers
        employee_phone_attr = [
            "Phone number 1", "Phone number 2" , "Phone number 3" , "Phone number 4"
        ]
        formatted_phone_data = [
            (employee_phone_attr[i], str(employee_phone[i]))for i in range(len(employee_phone))
        ]
        formatted_data = formatted_employee_data + formatted_phone_data

        # Tạo bảng và hiển thị dữ liệu
        create_table(generate_report_window, formatted_data, 1, 0)


        # dữ liệu branch
        label = tk.Label(
            generate_report_window,
            text="Thông tin chi nhánh",
            font=("Arial", 10, "bold"),
        )
        label.grid(row=0, column=1)

        # Branch attribute
        branch_attr = [
            "Branch Name", "Email", "Street", "District", "City", 
            "Region", "Number", "Manager ID"
        ]
        formatted_branch_data = [
            (branch_attr[i], str(branch_data[i])) for i in range(len(branch_data))
        ]
        # Branch phone
        branch_phone_attr = [
            "phone number 1", "phone number 2", "phone number 3",
            "phone number 4", "phone number 5", "phone number 6",
        ]
        formatted_branch_phone = [
            (branch_phone_attr[i], str(branch_phone[i])) for i in range(len(branch_phone))
        ]
        #Branch fax
        branch_fax_attr = [
            "fax number 1", "fax number 2", "fax number 3",
            "fax number 4", "fax number 5", "fax number 6",
        ]
        formatted_branch_fax = [
            (branch_fax_attr[i], str(branch_fax[i])) for i in range(len(branch_fax))
        ]

        formatted_data = formatted_branch_data + formatted_branch_phone + formatted_branch_fax

        # tao bang hien thi du lieu branch
        create_table(generate_report_window, formatted_data, 1, 1)


        # Thông tin nhân viên quản lý
        label = tk.Label(
            generate_report_window,
            text="Thông tin nhân viên quản lý",
            font=("Arial", 10, "bold"),
        )
        label.grid(row=0, column=2)
        # Định dạng và hiển thị dữ liệu
        manager_attr = [
            "EMPLOYEECODE", "DOB", "Email", "Last Name", "First Name",
            "House Number", "Street", "District", "City", "Branch Name"
        ]
        formatted_manager_data = [
            (manager_attr[i], str(manager_data[i])) for i in range(len(manager_data))
        ]

        # manager phonenumbers
        manager_phone_attr = [
            "Phone number 1", "Phone number 2" , "Phone number 3" , "Phone number 4"
        ]
        formatted_phone_data = [
            (manager_phone_attr[i], str(manager_phone[i])) for i in range(len(manager_phone))
        ]

        # Tổng hợp dữ liệu
        formatted_data = formatted_manager_data + formatted_phone_data

        # Tạo bảng và hiển thị dữ liệu
        create_table(generate_report_window, formatted_data, 1, 2)





    # Nút thoát
    close_button = tk.Button(
        generate_report_window, text="Thoát", command=generate_report_window.destroy
    )
    close_button.grid(row=2, column=1, padx=10, pady=10)



def close_window(root, window):
	window.destroy()
	root.deiconify() 