from tkinter import *
import osc as te
import numpy as np

class Example(Frame):
 
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.parent.title("Окно по центру экрана")
        self.pack(fill=BOTH, expand=1)
        self.centerWindow()
        global lbl
        lbl = Label(root, width = 100, text="")
        lbl.pack()
        super().__init__()
        self.initUI()
        
 
    def centerWindow(self):
        w = 290
        h = 150
 
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
 
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))
    

    def initUI(self):
      frame = Frame(self, relief=RAISED, borderwidth=1)
      frame.pack(fill=BOTH, expand=True)
      
      def caption(event):
          global t
          alist = [0,1]
          t = ent.get()
          l = len(t)
          fix = l%4

          def check():
            b = []
            ch = []
            for i in range(l):
              b.append(int(t[i]))
            for i in range(l):
              if b[i] in alist: ch.append(True)
              else: ch.append(False)
            return ch

          if not all(check()): lbl['text'] = 'ОШИБКА: неизвестный(ые) символ(ы)'
          elif  all(check()) and l%4==0:
            a = []
            for i in range(l):
                a.append(int(t[i]))
            lbl['text'] = ''
            te.osc(a)
          elif all(check()) and l%4!=0: lbl['text'] = f'ОШИБКА: не хватает {4-fix} символа(ов)'
          


      self.pack(fill=BOTH, expand=True)
      global ent
      
      ent = Entry(root, width = 100)
      ent.pack(expand=1)
      ent.bind('<Return>', caption)
      root.bind('<Control-z>', exit_)

def exit_(event):
        root.destroy()

def main():
  global root
  root = Tk()
  ex = Example(root)
  root.bind('<Control-z>', exit_)
  root.mainloop()

if __name__ == '__main__':
    main()