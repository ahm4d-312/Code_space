import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime


DB_NAME = "my_database.db"
LOW_STOCK_LIMIT = 20

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn, conn.cursor()

conn, cursor = get_db_connection()
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    barcode TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    cost_price REAL NOT NULL,
    sell_price REAL NOT NULL,
    quantity INTEGER NOT NULL,
    created_at TEXT
)
""")
conn.commit()
conn.close()


# --- Show Product Info ---
def show_product_info():
    def search():
        barcode = e_barcode.get().strip()
        if not barcode:
            messagebox.showerror("خطأ", "أدخل الباركود")
            return

        conn, cursor = get_db_connection()
        cursor.execute("""
            SELECT name, description, sell_price, quantity
            FROM products WHERE barcode=?
        """, (barcode,))
        product = cursor.fetchone()
        conn.close()

        if not product:
            messagebox.showerror("خطأ", "المنتج غير موجود")
            return

        info_label.config(text=f"""
اسم المنتج: {product[0]}

الوصف:
{product[1]}

سعر البيع: {product[2]}
الكمية المتوفرة: {product[3]}
""")

    win = Toplevel(root)
    win.title("معلومات المنتج")
    win.geometry("400x350")

    Label(win, text="الباركود:").pack(pady=5)
    e_barcode = Entry(win)
    e_barcode.pack(pady=5)

    Button(win, text="عرض المعلومات", command=search).pack(pady=10)

    info_label = Label(win, text="", justify="left")
    info_label.pack(pady=10)

# --- Add Product ---
def add_products():
    def save():
        try:
            barcode = e_barcode.get().strip()
            name = e_name.get().strip()
            desc = e_desc.get("1.0", END).strip()
            cost = float(e_cost.get())
            sell = float(e_sell.get())
            qty = int(e_qty.get())

            if not barcode or not name or qty <= 0 or cost <= 0 or sell <= 0:
                raise ValueError

            conn, cursor = get_db_connection()
            cursor.execute("""
                INSERT INTO products
                (barcode, name, description, cost_price, sell_price, quantity, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                barcode, name, desc, cost, sell, qty,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            conn.commit()
            conn.close()

            messagebox.showinfo("نجاح", "تمت إضافة المنتج بنجاح")
            win.destroy()

        except sqlite3.IntegrityError:
            messagebox.showerror("خطأ", "الباركود موجود مسبقًا")
        except:
            messagebox.showerror("خطأ", "تحقق من جميع المدخلات")

    win = Toplevel(root)
    win.title("إضافة منتج / أكياس")
    win.geometry("400x480")

    Label(win, text="الباركود").pack()
    e_barcode = Entry(win)
    e_barcode.pack()

    Label(win, text="اسم المنتج").pack()
    e_name = Entry(win)
    e_name.pack()

    Label(win, text="سعر التكلفة").pack()
    e_cost = Entry(win)
    e_cost.pack()

    Label(win, text="سعر البيع").pack()
    e_sell = Entry(win)
    e_sell.pack()

    Label(win, text="الكمية").pack()
    e_qty = Entry(win)
    e_qty.pack()

    Label(win, text="وصف المنتج").pack()
    e_desc = Text(win, height=4)
    e_desc.pack()

    Button(win, text="حفظ المنتج", command=save).pack(pady=15)

# --- Sell Product ---
def sell_product():
    def sell():
        try:
            barcode = e_barcode.get().strip()
            qty_to_sell = int(e_qty.get())

            if qty_to_sell <= 0:
                raise ValueError

            conn, cursor = get_db_connection()
            cursor.execute(
                "SELECT quantity FROM products WHERE barcode=?",
                (barcode,)
            )
            row = cursor.fetchone()

            if not row:
                messagebox.showerror("خطأ", "المنتج غير موجود")
                conn.close()
                return

            current_qty = row[0]

            if qty_to_sell > current_qty:
                messagebox.showwarning(
                    "كمية غير كافية",
                    f"الكمية المتوفرة: {current_qty}"
                )
                conn.close()
                return

            cursor.execute(
                "UPDATE products SET quantity = quantity - ? WHERE barcode=?",
                (qty_to_sell, barcode)
            )
            conn.commit()
            conn.close()

            messagebox.showinfo(
                "تم البيع",
                f"تم بيع {qty_to_sell} كيس بنجاح"
            )
            win.destroy()

        except ValueError:
            messagebox.showerror("خطأ", "أدخل كمية صحيحة")
        except Exception as e:
            messagebox.showerror("خطأ", str(e))

    win = Toplevel(root)
    win.title("بيع منتج")
    win.geometry("300x220")

    Label(win, text="الباركود:").pack(pady=5)
    e_barcode = Entry(win)
    e_barcode.pack(pady=5)

    Label(win, text="الكمية المطلوبة:").pack(pady=5)
    e_qty = Entry(win)
    e_qty.pack(pady=5)

    Button(win, text="تأكيد البيع", command=sell).pack(pady=15)

# --- View Stock ---
def view_stock():
    win = Toplevel(root)
    win.title("المخزون")
    win.geometry("900x400")

    columns = ("barcode", "name", "sell_price", "quantity")
    tree = ttk.Treeview(win, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=200)

    tree.pack(fill=BOTH, expand=True)

    conn, cursor = get_db_connection()
    cursor.execute("SELECT barcode, name, sell_price, quantity FROM products")
    for row in cursor.fetchall():
        tree.insert("", END, values=row)
    conn.close()

# ==============================
# 🖥️ Main GUI
# ==============================
root = Tk()
root.title("إدارة مخزون المنتجات")
root.geometry("400x380")

Label(
    root,
    text="إدارة مخزون المنتجات",
    font=("Arial", 12, "bold")
).pack(pady=10)

Button(root, text="➕ إضافة منتج للمخزون",
       width=25, command=add_products).pack(pady=5)

Button(root, text="💰 بيع ",
       width=25, command=sell_product).pack(pady=5)

Button(root, text="ℹ️ معلومات المنتج",
       width=25, command=show_product_info).pack(pady=5)

Button(root, text="📊 عرض المخزون",
       width=25, command=view_stock).pack(pady=5)

Button(root, text="🚪 خروج",
       width=25, command=root.destroy).pack(pady=5)

root.mainloop()
