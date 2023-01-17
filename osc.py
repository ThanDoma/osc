import matplotlib.pyplot as plt
import numpy as np

from Design import raisedCosineDesign
from qpsk_mode import qpsk_mod


def osc(y_1, r):
# input
    y1 = y_1

    plt.subplot(4,1,1)

    x = len(y1)//2
    t = np.arange(0,x,0.5)
    plt.plot(t,y1,drawstyle='steps-post')

    plt.xlim(0,x)
    plt.ylim(-0.5,1.5)
    plt.title('Input Signal')

    # I Signal
    plt.subplot(4,1,2)
    a = 1
    b = np.sqrt(2)
    tI = np.arange(0,x,1)
    yI, y_I = [], []
    check = []
    ch = ''
    l = int(len(y1))

    for i in range(0, l, 2):
        
        ch = str(y1[i]) + str(y1[i+1])
        check.append(ch)

    l = int(len(y1)/2)
    yI.append(a)
    y_I.append(a)

    for i in range(1, l):

        if (check[i]=='00' and check[i-1]=='11'):
            if len(yI)%2==0:
                yI.append(b)
            else: yI.append(-b)
        elif (check[i]=='00' and check[i-1]!='11'):
            if len(yI)%2==0:
                yI.append(a)
            else: yI.append(-a)
        
        if (check[i]=='11' and check[i-1]=='00'):
            if len(yI)%2==0:
                yI.append(b)
            else: yI.append(-b)
        elif (check[i]=='11' and check[i-1]!='00'):
            if len(yI)%2==0:
                yI.append(a)
            else: yI.append(-a)
            
        if (check[i]=='01' and check[i-1]=='10'):
            if len(yI)%2==0:
                yI.append(b)
            else: yI.append(-b)
        elif (check[i]=='01' and check[i-1]!='10'):
            if len(yI)%2==0:
                yI.append(a)
            else: yI.append(-a)
        
        if (check[i]=='10' and check[i-1]=='01'):
            if len(yI)%2==0:
                yI.append(b)
            else: yI.append(-b)
        elif (check[i]=='10' and check[i-1]!='01'):
            if len(yI)%2==0:
                yI.append(a)
            else: yI.append(-a)

    for i in range(1, l):

        if (check[i]=='00' and check[i-1]=='11'):
            if len(y_I)%2==0:
                y_I.append(a)
            else: y_I.append(-a)
        elif (check[i]=='00' and check[i-1]!='11'):
            if len(y_I)%2==0:
                y_I.append(a)
            else: y_I.append(-a)
        
        if (check[i]=='11' and check[i-1]=='00'):
            if len(y_I)%2==0:
                y_I.append(a)
            else: y_I.append(-a)
        elif (check[i]=='11' and check[i-1]!='00'):
            if len(y_I)%2==0:
                y_I.append(a)
            else: y_I.append(-a)
            
        if (check[i]=='01' and check[i-1]=='10'):
            if len(y_I)%2==0:
                y_I.append(a)
            else: y_I.append(-a)
        elif (check[i]=='01' and check[i-1]!='10'):
            if len(y_I)%2==0:
                y_I.append(a)
            else: y_I.append(-a)
        
        if (check[i]=='10' and check[i-1]=='01'):
            if len(y_I)%2==0:
                y_I.append(a)
            else: y_I.append(-a)
        elif (check[i]=='10' and check[i-1]!='01'):
            if len(y_I)%2==0:
                y_I.append(a)
            else: y_I.append(-a)

    plt.plot(tI,y_I,drawstyle='steps-post')
    plt.xlim(0,x)
    plt.ylim(-2,2)
    plt.title('I signal')
    # Q signal
    plt.subplot(4,1,3)
    
    yQ = []
    yq = [a,-a,-a,a]
    s = x%4 #первые s позиции шаблона
    f = x//4 #количество полных шаблонов

    for _ in range(f):
        yQ = yQ+yq

    yQ = yQ+yq[:s]

    plt.plot(tI,yQ,drawstyle='steps-post')
    plt.xlim(0,x)
    plt.ylim(-2,2)
    plt.title('Q Signal')

    # QPSK signal
    plt.subplot(4,1,4)
    t = np.arange(0,x,0.01)#Граница, шаг

    def outputwave(I,Q,t):
        rectwav = []
        for i in range(len(I)):
            t_tmp = t[((i)*100):((i+1)*100)]
            yI_tmp = yI[i]*np.ones(100)
            yQ_tmp = yQ[i]*np.ones(100)
            wav_tmp = yI_tmp*np.cos(2*np.pi*5*t_tmp)-yQ_tmp*np.sin(2*np.pi*5*t_tmp)
            rectwav.append(wav_tmp)
        return rectwav

    rectwav = outputwave(yI,yQ,t)
    plt.plot(t,np.array(rectwav).flatten(),'r')
    plt.xlim(0,x)#от 0 до 4 по X
    plt.ylim(-2,2)# -2 до 2 по Y
    plt.title('QPSK Signal')
    plt.tight_layout()

    N=len(check) # Количество передаваемых символов должно быть небольшим и адекватным

    fc=1; L=8 # несущая частота и коэффициент передискретизации

    a = np.array(y1) # однородные случайные символы от 0 до 1
    # модулируйте исходные символы с помощью QPSK
    qpsk_result= qpsk_mod(a,fc,L)
        # Импульсная форма модулированных сигналов путем свертки с помощью RC-фильтра
    alpha = r; span =  10 # Альфа-фильтр RC и диапазон фильтрации в символ
    b = raisedCosineDesign(alpha,span, L) # Формирователь RC-импульсов 

    iRC_qpsk=np.convolve(qpsk_result['I(t)'],b,mode='valid') #RC - QPSK I(t)
    qRC_qpsk= np.convolve(qpsk_result['Q(t)'],b,mode='valid') #RC - QPSK Q(t)
    
    # iRC_qpsk=np.convolve(1, b, mode='valid')
    # qRC_qpsk= np.convolve(1, b, mode='valid')
    fig1, axs = plt.subplots(1, 1)

    axs.plot(iRC_qpsk/10,qRC_qpsk/10)# RC-образный QPSK

    axs.set_title(r"QPSK, $\alpha$="+str(alpha))
    axs.set_xlabel('I(t)');axs.set_ylabel('Q(t)')

    plt.show()