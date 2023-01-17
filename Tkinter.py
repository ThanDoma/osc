from tkinter import *

import osc as te
import numpy as np

class Example(Frame):
 
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.parent.title("")
        self.pack(fill=BOTH, expand=1)
        #self.centerWindow()
        global lbl
        lbl = Label(root, width = 100, text="")
        lbl.pack()
        super().__init__()
        self.initUI()
        
    

    def initUI(self):
      frame = Frame(
      root, #Обязательный параметр, который указывает окно для размещения Frame.
      padx = 10, #Задаём отступ по горизонтали.
      pady = 10 #Задаём отступ по вертикали.
      )
      
      frame.pack(fill=BOTH, expand=True)
      
      height_lb = Label(
      frame,
      text="Введите кодовую последовательность "
      )
      height_lb.grid(row=3, column=1)
      
      weight_lb = Label(
      frame,
      text="Коэф. скругления формируещего фильтра  ",
      )
      weight_lb.grid(row=4, column=1)
      
      BIN_tf = Entry(
      frame, #Используем нашу заготовку с настроенными отступами.
      )
      BIN_tf.grid(row=3, column=2)
      
      RC_tf = Entry(
      frame,
      )
      RC_tf.grid(row=4, column=2, pady=5)
      
      def caption(event):
          global t
          alist = [0,1]
          t = BIN_tf.get()
          r = float(RC_tf.get())
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
            te.osc(a, r)
          elif all(check()) and l%4!=0: lbl['text'] = f'ОШИБКА: не хватает {4-fix} символа(ов)'
          


      self.pack(fill=BOTH, expand=True)
      
      BIN_tf.bind('<Return>', caption)
      RC_tf.bind('<Return>', caption)
      
      root.bind('<Control-z>', exit_)

def exit_(event):
        root.destroy()

def main():
  global root
  root = Tk()
  root.geometry('400x300')
  ex = Example(root)
  root.bind('<Control-z>', exit_)
  root.mainloop()

if __name__ == '__main__':
    main()