import tkinter as tk
from tkinter import messagebox

# ----------------------------
# کلاس حساب بانکی
# ----------------------------

class BankAccount:
    def __init__(self, owner, password, balance=0):
        self.owner = owner
        self.password = password
        self.balance = balance
        self.transactions = []

    def authenticate(self, password):
        return self.password == password

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transactions.append(f"واریز: +{amount}")
            return True
        return False

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.transactions.append(f"برداشت: -{amount}")
            return True
        return False

    def transfer(self, target_account, amount):
        if amount <= self.balance:
            self.balance -= amount
            target_account.balance += amount
            self.transactions.append(f"انتقال به {target_account.owner}: -{amount}")
            target_account.transactions.append(f"انتقال از {self.owner}: +{amount}")
            return True
        return False

# ----------------------------
# رابط گرافیکی
# ----------------------------

class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("سیستم بانکی نوید 🏦")
        self.accounts = {}  # ذخیره حساب‌ها
        self.current_account = None

        self.build_login_screen()

    def build_login_screen(self):
        self.clear_window()

        tk.Label(self.root, text="ورود / ساخت حساب", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="نام کاربری:").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="رمز عبور:").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="ورود", command=self.login).pack(pady=5)
        tk.Button(self.root, text="ساخت حساب", command=self.create_account).pack()

    def build_dashboard(self):
        self.clear_window()
        tk.Label(self.root, text=f"خوش آمدی {self.current_account.owner} 👋", font=("Arial", 14)).pack(pady=10)

        tk.Button(self.root, text="مشاهده موجودی", width=30, command=self.show_balance).pack(pady=2)
        tk.Button(self.root, text="واریز وجه", width=30, command=self.deposit_money).pack(pady=2)
        tk.Button(self.root, text="برداشت وجه", width=30, command=self.withdraw_money).pack(pady=2)
        tk.Button(self.root, text="انتقال وجه", width=30, command=self.transfer_money).pack(pady=2)
        tk.Button(self.root, text="تاریخچه تراکنش", width=30, command=self.show_transactions).pack(pady=2)
        tk.Button(self.root, text="خروج از حساب", width=30, command=self.logout).pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.accounts and self.accounts[username].authenticate(password):
            self.current_account = self.accounts[username]
            self.build_dashboard()
        else:
            messagebox.showerror("خطا", "نام کاربری یا رمز اشتباه است!")

    def create_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.accounts:
            messagebox.showerror("خطا", "این کاربر قبلاً ثبت شده!")
        elif username == "" or password == "":
            messagebox.showwarning("هشدار", "همه فیلدها را پر کن.")
        else:
            self.accounts[username] = BankAccount(username, password, 0)
            messagebox.showinfo("موفقیت", "حساب با موفقیت ساخته شد.")

    def logout(self):
        self.current_account = None
        self.build_login_screen()

    def show_balance(self):
        messagebox.showinfo("موجودی", f"موجودی فعلی: {self.current_account.balance} تومان")

    def deposit_money(self):
        self.popup_amount_window("مبلغ واریز را وارد کن:", self.current_account.deposit, "واریز با موفقیت انجام شد.")

    def withdraw_money(self):
        self.popup_amount_window("مبلغ برداشت را وارد کن:", self.current_account.withdraw, "برداشت با موفقیت انجام شد.", True)

    def transfer_money(self):
        def submit():
            target = target_entry.get()
            try:
                amount = int(amount_entry.get())
            except:
                messagebox.showerror("خطا", "مبلغ نامعتبر است.")
                return

            if target not in self.accounts:
                messagebox.showerror("خطا", "کاربر مقصد یافت نشد.")
            elif self.accounts[target] == self.current_account:
                messagebox.showwarning("هشدار", "نمی‌توانی به خودت پول منتقل کنی.")
            elif self.current_account.transfer(self.accounts[target], amount):
                messagebox.showinfo("موفقیت", "انتقال انجام شد.")
                transfer_win.destroy()
            else:
                messagebox.showerror("خطا", "موجودی کافی نیست.")

        transfer_win = tk.Toplevel(self.root)
        transfer_win.title("انتقال وجه")

        tk.Label(transfer_win, text="نام کاربری مقصد:").pack()
        target_entry = tk.Entry(transfer_win)
        target_entry.pack()

        tk.Label(transfer_win, text="مبلغ:").pack()
        amount_entry = tk.Entry(transfer_win)
        amount_entry.pack()

        tk.Button(transfer_win, text="انتقال", command=submit).pack(pady=5)

    def show_transactions(self):
        tx = "\n".join(self.current_account.transactions) or "تراکنشی وجود ندارد."
        messagebox.showinfo("تاریخچه تراکنش‌ها", tx)

    def popup_amount_window(self, title, operation, success_msg, check_balance=False):
        def submit():
            try:
                amount = int(amount_entry.get())
                if check_balance and amount > self.current_account.balance:
                    messagebox.showerror("خطا", "موجودی کافی نیست.")
                    return

                if operation(amount):
                    messagebox.showinfo("موفقیت", success_msg)
                    popup.destroy()
                else:
                    messagebox.showerror("خطا", "عملیات ناموفق بود.")
            except:
                messagebox.showerror("خطا", "عدد وارد کن.")

        popup = tk.Toplevel(self.root)
        popup.title(title)

        tk.Label(popup, text=title).pack()
        amount_entry = tk.Entry(popup)
        amount_entry.pack()

        tk.Button(popup, text="تأیید", command=submit).pack(pady=5)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# اجرای برنامه
if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()
