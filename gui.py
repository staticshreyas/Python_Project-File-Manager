from tkinter import *



class Interface:

    def __init__(self, root, pm):
        self.cuted = {}
        self.root = root
        self.root.title('File Manager')
        self.root.geometry('545x300')
        self.root.resizable(0,0)

        self.pm = pm
        self.frame_top = Frame(self.root, width=545, height=50, bg='grey').grid(columnspan=8, sticky='we')

        self.bttn1 = Button(self.frame_top, width=5, text='Add Dir', command=lambda: self.lb_trigger(self.add_dir_trigger))
        self.bttn1.grid(row=0, column=1, sticky='w', padx=5)
        self.bttn2 = Button(self.frame_top, width=5, text='New File', command=lambda: self.lb_trigger(self.add_file_trigger))
        self.bttn2.grid(row=0, column=2, sticky='w', padx=5)
        self.bttn3 = Button(self.frame_top, width=5, text='Rename', command=lambda: self.lb_trigger(self.name_change))
        self.bttn3.grid(row=0, column=3, sticky='w', padx=5)
        self.bttn4 = Button(self.frame_top, width=5, text='Delete', command=lambda: self.lb_trigger(self.delete_item))
        self.bttn4.grid(row=0, column=4, sticky='w', padx=5)
        self.bttn5 = Button(self.frame_top, width=5, text='Copy', command=lambda: self.lb_trigger(self.get_copy_item))
        self.bttn5.grid(row=0, column=5, sticky='w', padx=5)
        self.bttn6 = Button(self.frame_top, width=5, text='Cut', command=lambda: self.lb_trigger(self.get_cut_item))
        self.bttn6.grid(row=0, column=6, sticky='w', padx=5)
        self.bttn7 = Button(self.frame_top, width=5, text='Paste', command=lambda: self.lb_trigger(self.paste_item))
        self.bttn7.grid(row=0, column=7, sticky='w', padx=5)

        self.frame_middle = Frame(self.root)
        self.frame_middle.grid(columnspan=8)

        self.lb_1 = Listbox(self.frame_middle, width=60)
        self.lb_1.bind('<Double-Button-1>', lambda _: self.pm.double_click(self.lb_1))
        self.lb_1.grid(row=2, column=0, sticky='w')

        '''self.lb_2 = Listbox(self.frame_middle, width=25)
        self.lb_2.bind('<Double-Button-1>', lambda _: self.pm.double_click(self.lb_2))
        self.lb_2.grid(row=2, column=4, sticky='e')'''

    def lb_trigger(self, f):
        if len(self.lb_1.curselection()) > 0:
            f(self.lb_1, '''self.lb_2''')
        '''elif len(self.lb_2.curselection()) > 0:
            f(self.lb_2, self.lb_1)'''

    def add_dir_trigger(self, *args):
        lb = args[0]
        self.create_edit_spot(lb, self.pm.add_dir)

    def add_file_trigger(self, *args):
        lb = args[0]
        self.create_edit_spot(lb, self.pm.add_file)

    def get_copy_item(self, *args):
        lb_copy_item, lb_copy_here = args[0], args[1]
        item = self.get_selected_item(lb_copy_item)
        self.pm.subject_copy(item, lb_copy_here, self.refresh_lb)

    def name_change(self, *args):
        lb = args[0]
        item = self.get_selected_item(lb)
        self.create_edit_spot(lb, self.pm.rename_file, item)

    def delete_item(self, *args):
        lb = args[0]
        item = self.get_selected_item(lb)
        self.pm.delete_subject(item, lb, self.refresh_lb)

    def get_cut_item(self, *args):
        lb = args[0]
        self.cuted['item'] = self.get_selected_item(lb)
        self.cuted['path'] = self.pm.get_active_lb_root(lb=lb)

    def paste_item(self, *args):
        lb = args[0]
        if self.cuted:
            self.pm.paste_subject(self.cuted, lb, self.refresh_lb)
            self.cuted = {}

    def get_selected_item(self, lb):
        index = lb.curselection()[0]
        if lb.get(index) != '..':
            item = lb.get(index)
        return item

    def create_edit_spot(self, *args):
        item = None
        v = StringVar()
        bottom_frame = Frame(self.root).grid(columnspan=8, sticky='we')
        self.edit_spot = Entry(bottom_frame, textvariable=v, )
        if len(args) == 3:
            item = args[2]
            self.edit_spot.insert(0, item)
        lb, f = args[0], args[1]
        self.edit_spot.grid(row=2, column=2, columnspan=4, padx=50, sticky='e')

        self.bttn_apply = Button(bottom_frame, text='ok',
                                 command=lambda: f(lb, self.edit_spot.get(), self.del_edit_spot, self.refresh_lb, item))
        self.bttn_apply.grid(row=2, column=4, sticky='e', columnspan=2)
        self.bttn_cancel = Button(bottom_frame, text='cancel', command=lambda: self.del_edit_spot())
        self.bttn_cancel.grid(row=2, column=6, sticky='w', columnspan=2)

    def del_edit_spot(self):
        self.edit_spot.destroy()
        self.bttn_apply.destroy()
        self.bttn_cancel.destroy()

    def refresh_lb(self):
        self.pm.get_tree(self.lb_1)
        '''self.pm.get_tree(self.lb_2)'''
