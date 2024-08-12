import tkinter as tk
from tkinter import messagebox, simpledialog


class ExpenseSharingApp:
    def __init__(self):
        self.friends = {}
        self.expenses = []

    def add_friend(self, name):
        if name and name not in self.friends:
            self.friends[name] = 0
            self.update_status(f"{name} has been added to the group.")
        elif not name:
            self.update_status("Name cannot be empty.", "error")
        else:
            self.update_status(f"{name} is already in the group.", "warning")

    def remove_friend(self, name):
        if name in self.friends:
            del self.friends[name]
            self.update_status(f"{name} has been removed from the group.")
            self.recalculate_balances()
        else:
            self.update_status(f"{name} is not in the group.", "warning")

    def view_all_friends(self):
        if not self.friends:
            messagebox.showinfo("Friends", "No friends in the group yet.")
        else:
            friends_list = "\n".join(self.friends.keys())
            messagebox.showinfo("Friends in the group", friends_list)

    def add_expense(self, description, amount, paid_by, splits=None):
        if paid_by not in self.friends:
            add_option = messagebox.askyesno("Add Friend", f"{paid_by} is not in the group. Add them?")
            if add_option:
                self.add_friend(paid_by)
            else:
                return

        if splits is None:
            split_amount = amount / len(self.friends)
            splits = {friend: split_amount for friend in self.friends}

        for friend, share in splits.items():
            if friend not in self.friends:
                messagebox.showwarning("Warning", f"{friend} is not in the group. Please add them first.")
                return
            if friend == paid_by:
                self.friends[friend] += amount - share
            else:
                self.friends[friend] -= share

        self.expenses.append({
            "description": description,
            "amount": amount,
            "paid_by": paid_by,
            "splits": splits
        })
        self.update_status(f"Expense '{description}' of amount {amount} added, paid by {paid_by}.")

    def show_balances(self):
        balances = "\n".join(
            f"{friend}: {'owes' if balance < 0 else 'is owed'} {abs(balance):.2f}"
            for friend, balance in self.friends.items()
        )
        messagebox.showinfo("Balances", balances if balances else "No balances yet.")

    def show_expenses(self):
        if not self.expenses:
            messagebox.showinfo("Expenses", "No expenses recorded yet.")
            return

        report = ""
        for i, expense in enumerate(self.expenses, 1):
            report += f"{i}. {expense['description']}: {expense['amount']} paid by {expense['paid_by']}\n"
            for friend, share in expense['splits'].items():
                report += f"   {friend} owes {share:.2f}\n"
        messagebox.showinfo("Expense Report", report)

    def settle_up(self, name):
        if name in self.friends:
            self.friends[name] = 0
            self.update_status(f"{name}'s balance has been settled.")
        else:
            self.update_status(f"{name} is not in the group.", "warning")

    def clear_all(self):
        self.friends.clear()
        self.expenses.clear()
        self.update_status("All data has been cleared.")

    def recalculate_balances(self):
        self.friends = {friend: 0 for friend in self.friends}
        for expense in self.expenses:
            self.add_expense(expense['description'], expense['amount'], expense['paid_by'], expense['splits'])

    def update_status(self, message, status_type="info"):
        self.status_var.set(message)
        if status_type == "info":
            self.status_label.config(fg="green")
        elif status_type == "warning":
            self.status_label.config(fg="orange")
        elif status_type == "error":
            self.status_label.config(fg="red")


class ExpenseSharingGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Expense Sharing App")
        self.geometry("500x500")
        self.configure(bg="#f0f0f0")
        self.app = ExpenseSharingApp()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Expense Sharing App", font=("Arial", 20), bg="#f0f0f0").pack(pady=20)

        button_frame = tk.Frame(self, bg="#f0f0f0")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Add Friend", command=self.add_friend, width=20, height=2).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(button_frame, text="Remove Friend", command=self.remove_friend, width=20, height=2).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(button_frame, text="View All Friends", command=self.view_all_friends, width=20, height=2).grid(row=1, column=0, padx=10, pady=5)
        tk.Button(button_frame, text="Add Expense", command=self.add_expense, width=20, height=2).grid(row=1, column=1, padx=10, pady=5)
        tk.Button(button_frame, text="Show Balances", command=self.show_balances, width=20, height=2).grid(row=2, column=0, padx=10, pady=5)
        tk.Button(button_frame, text="Show Expense Report", command=self.show_expenses, width=20, height=2).grid(row=2, column=1, padx=10, pady=5)
        tk.Button(button_frame, text="Settle Up", command=self.settle_up, width=20, height=2).grid(row=3, column=0, padx=10, pady=5)
        tk.Button(button_frame, text="Clear All Data", command=self.clear_all, width=20, height=2).grid(row=3, column=1, padx=10, pady=5)
        tk.Button(button_frame, text="Exit", command=self.quit, width=20, height=2, bg="#d9534f", fg="white").grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.status_var = tk.StringVar()
        self.status_label = tk.Label(self, textvariable=self.status_var, font=("Arial", 12), bg="#f0f0f0")
        self.status_label.pack(pady=10)
        self.app.status_label = self.status_label
        self.app.status_var = self.status_var

    def add_friend(self):
        name = simpledialog.askstring("Add Friend", "Enter the friend's name:")
        if name:
            self.app.add_friend(name)

    def remove_friend(self):
        name = simpledialog.askstring("Remove Friend", "Enter the friend's name:")
        if name:
            self.app.remove_friend(name)

    def view_all_friends(self):
        self.app.view_all_friends()

    def add_expense(self):
        description = simpledialog.askstring("Add Expense", "Enter the expense description:")
        amount = simpledialog.askfloat("Add Expense", "Enter the total amount:")
        paid_by = simpledialog.askstring("Add Expense", "Who paid for this expense?")

        if description and amount and paid_by:
            self.app.add_expense(description, amount, paid_by)

    def show_balances(self):
        self.app.show_balances()

    def show_expenses(self):
        self.app.show_expenses()

    def settle_up(self):
        name = simpledialog.askstring("Settle Up", "Enter the friend's name to settle up:")
        if name:
            self.app.settle_up(name)

    def clear_all(self):
        confirmation = messagebox.askyesno("Clear All Data", "Are you sure you want to clear all data?")
        if confirmation:
            self.app.clear_all()


if __name__ == "__main__":
    app = ExpenseSharingGUI()
    app.mainloop()
