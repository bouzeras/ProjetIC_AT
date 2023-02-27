import tkinter as tk
from tkinter import messagebox


class Group:
    def __init__(self, name, size):
        self.name = name
        self.max_size = size
        self.users = []

    def add_user(self, user):
        if len(self.users) < self.max_size:
            self.users.append(user)
            return True
        else:
            return False

    def remove_user(self, user):
        if user in self.users:
            self.users.remove(user)
            return True
        else:
            return False


class AdminAccount:
    def __init__(self):
        self.groups = []
        self.users = []

    def create_group(self, name, size, last_group_config):
        if size <= 0:
            raise ValueError("The group size must be greater than 0.")

        # Create groups with the specified configuration
        num_users = len(self.users)
        num_groups = num_users // size + int(num_users % size > 0)
        last_group_size = num_users % size if last_group_config == 'LAST_MIN' else size - num_users % size
        for i in range(num_groups):
            group_size = last_group_size if i == num_groups - 1 else size
            group_name = f"{name}-{i+1}"
            group = Group(group_name, group_size)
            self.groups.append(group)

        # Assign users to groups
        remaining_users = list(self.users)
        for group in self.groups:
            for user in remaining_users:
                if group.add_user(user):
                    remaining_users.remove(user)
                if len(group.users) == group.max_size:
                    break

    def list_users_without_group(self):
        users_without_group = []
        for user in self.users:
            if not any(user in group.users for group in self.groups):
                users_without_group.append(user)
        return users_without_group

    def create_user(self, name):
        self.users.append(name)

    def remove_user(self, name):
        if name in self.users:
            self.users.remove(name)
            for group in self.groups:
                group.remove_user(name)
            return True
        else:
            return False


class GUI:
    def __init__(self, admin_account):
        self.admin_account = admin_account
        self.root = tk.Tk()
        self.root.title("Group Manager")
        self.root.geometry("400x300")

        # Labels and input boxes for creating a group
        tk.Label(self.root, text="Create a new group").pack(pady=10)
        tk.Label(self.root, text="Group name:").pack()
        self.group_name_entry = tk.Entry(self.root)
        self.group_name_entry.pack()
        tk.Label(self.root, text="Group size:").pack()
        self.group_size_entry = tk.Entry(self.root)
        self.group_size_entry.pack()
        tk.Label(self.root, text="Last group configuration:").pack()
        self.last_group_config_var = tk.StringVar(self.root, "LAST_MIN")
        last_group_min_rb = tk.Radiobutton(self.root, text="LAST_MIN", variable=self.last_group_config_var,
                                           value="LAST_MIN")
        last_group_max_rb = tk.Radiobutton(self.root, text="LAST_MAX", variable=self.last_group_config_var,
                                           value="LAST_MAX")
        last_group_min_rb.pack()
        last_group_max_rb.pack()
        tk.Button(self.root, text="Create group", command=self.create_group).pack(pady=10)