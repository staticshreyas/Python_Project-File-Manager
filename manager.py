import os
from tkinter import *
from shutil import copy2, copytree, move, rmtree


class Manager:

    def __init__(self):
        self.current_root = os.getcwd()
        self.current_root_1 = os.getcwd()
        self.current_root_2 = os.getcwd()
        self.parts = self.current_root.split('/')
        self.dirs = None
        self.files = None
        self.new_name = None

    def get_tree(self, lb):
        self.lb = lb
        self.current_root = self.get_active_lb_root()
        self.lb.delete(0, END)
        for self.root, self.dirs, self.files in os.walk(self.current_root):
            self.lb.insert(END, '..')
            for d in self.dirs:
                self.lb.insert(END, d)
            for f in self.files:
                self.lb.insert(END, f)
            break

    def rename_file(self, *args):
        lb, new_name, del_edit_spot, refresh_lb, old_name = args
        self.get_tree(lb)
        self.current_root = self.get_active_lb_root()
        os.chdir(self.current_root)
        if old_name != new_name: os.rename(old_name, new_name)
        del_edit_spot()
        refresh_lb()

    def get_selected(self):
        i = self.lb.curselection()[0]
        self.selected_item = self.lb.get(i)
        return self.selected_item

    def double_click(self, lb):
        self.lb = lb
        self.get_selected()
        self.get_tree(lb)
        self.current_root = self.check_lb_to_path_edit(self.edit_path())
        os.chdir(self.current_root)
        self.get_tree(self.lb)

    def edit_path(self):
        if self.selected_item == '..':
            parts = self.current_root.split('/')
            last_part = f'/{parts[-1]}'
            self.current_root = self.current_root.replace(last_part, '')
            return self.current_root
        elif self.selected_item in self.dirs:
            self.current_root = f'{self.current_root}/{self.selected_item}'
            return self.current_root
        elif self.selected_item in self.files:
            return self.current_root

    def check_lb_to_path_edit(self, p):
        if self.lb.__str__()[-1] == "2":
            self.current_root_2 = p
            return self.current_root_2
        else:
            self.current_root_1 = p
            return self.current_root_1

    def get_active_lb_root(self, **kwargs):
        if kwargs: self.lb = kwargs['lb']
        if self.lb.__str__()[-1] == "2":
            self.current_root = self.current_root_2
            return self.current_root_2
        else:
            self.current_root = self.current_root_1
            return self.current_root_1

    def do_copy_name(self, name):
        if re.search(r'\(\d\)', name):
            if name in self.dirs:  # w lb_copy_here
                to_change = re.findall(r'\(\d+\)', name)[-1]
                nr_copy = int(to_change[1:-1]) + 1
                no_change = name[0:-len(to_change)]
                self.new_name = no_change + to_change.replace(to_change, f'({nr_copy})')
            elif name in self.files:
                to_change = re.findall(r'\(\d+\).*\.', name)[-1]
                string_slices = name.rpartition(to_change)
                first_bracket = to_change[0]
                last_bracet = to_change.index(')')
                nr = to_change[1:last_bracet]
                end = to_change[last_bracet:]
                to_change = f'{first_bracket}{1 + int(nr)}{end}'
                self.new_name = string_slices[0] + to_change + string_slices[-1]
            else:
                self.new_name = name
            if os.path.isdir(f'{self.current_root}/{self.new_name}') or \
                    os.path.isfile(f'{self.current_root}/{self.new_name}'):
                return self.do_copy_name(self.new_name)
            return self.new_name
        elif os.path.isdir(name):
            self.new_name = name + '(1)'
            if os.path.isdir(f'{self.current_root}/{self.new_name}'):
                return self.do_copy_name(self.new_name)
            return self.new_name
        elif os.path.isfile(name):
            self.new_name = re.sub(r'(\.)', r'(1)\1', name)
            if os.path.isfile(f'{self.current_root}/{self.new_name}'):
                return self.do_copy_name(self.new_name)
            return self.new_name

    def subject_copy(self, name, lb_copy_here, refresh_lb):
        self.lb = lb_copy_here
        self.current_root = self.get_active_lb_root()
        if self.current_root == self.current_root_1:
            os.chdir(self.current_root_2)
        else:
            os.chdir(self.current_root_1)
        self.get_tree(lb_copy_here)
        new_name = self.do_copy_name(name)
        if os.path.isdir(name):
            copytree(name, f'{self.current_root}/{new_name}')
        elif os.path.isfile(name):
            copy2(name, f'{self.current_root}/{new_name}')
        refresh_lb()

    def delete_subject(self, item, lb, refresh_lb):
        self.get_tree(lb)
        os.chdir(self.current_root)
        if item in self.dirs:
            rmtree(item)
        elif item in self.files:
            os.remove(item)
        refresh_lb()

    def paste_subject(self, cuted, lb, refresh_lb):
        self.lb = lb
        path = cuted['path']
        item = cuted['item']
        cut_it = path + '/' + item
        self.current_root = self.get_active_lb_root()
        os.chdir(self.current_root)
        if path != self.current_root:
            move(cut_it, self.current_root)
            refresh_lb()

    def add_dir(self, *args):
        lb, name, del_edit_spot, refresh_lb, item = args
        self.refresh_when_add(lb)
        try:
            os.mkdir(name)
            del_edit_spot()
            refresh_lb()
        except FileExistsError:
            print(f'Katalog {name} istnieje')

    def add_file(self, *args):
        lb, name, del_edit_spot, refresh_lb, item = args
        self.refresh_when_add(lb)
        try:
            os.mknod(name)
            del_edit_spot()
            refresh_lb()
        except FileExistsError:
            print(f'Plik {name} istnieje')

    def refresh_when_add(self, lb):
        self.get_tree(lb)
        self.current_root = self.get_active_lb_root()
        os.chdir(self.current_root)
