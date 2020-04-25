from tkinter import *
from manager import Manager
from gui import Interface


root = Tk()
pm = Manager()

interface = Interface(root, pm)
pm.get_tree(interface.lb_1)

'''pm.get_tree(interface.lb_2)'''


root.mainloop()