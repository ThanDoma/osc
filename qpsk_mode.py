import numpy as np
import matplotlib.pyplot as plt

def qpsk_mod(a, fc, OF, enable_plot = False):
    """
    Модулируйте входящий двоичный поток, используя обычный QPSK
    Параметры:
        a: входной поток двоичных данных (0 и 1) для модуляции
        fc : несущая частота в герцах
        OF : коэффициент передискретизации - по крайней мере, 4 лучше
        enable_plot : True = отображение сигналов передатчика (по умолчанию False)
    Возвращается:
        результат : Словарь, содержащий следующие записи ключевых слов:
        s(t) : вектор сигнала с модуляцией QPSK с несущей, т.е. s(t)
        I(t): форма сигнала I канала основной полосы частот (без несущей)
        Q(t): форма сигнала Q-канала основной полосы частот (без несущей)
        t : временная база для сигнала с модуляцией несущей
    """
    L = 2*OF # samples in each symbol (QPSK has 2 bits in each symbol)
    I = a[0::2];Q = a[1::2] #even and odd bit streams
    # even/odd streams at 1/2Tb baud
        
    from scipy.signal import upfirdn #NRZ encoder
    I = upfirdn(h=[1]*L, x=2*I-1, up = L)
    Q = upfirdn(h=[1]*L, x=2*Q-1, up = L)
    
    fs = OF*fc # sampling frequency 
    t=np.arange(0,len(I)/fs,1/fs)  #time base    
    
    I_t = I*np.cos(2*np.pi*fc*t);Q_t = -Q*np.sin(2*np.pi*fc*t)
    s_t = I_t + Q_t # QPSK modulated baseband signal
    
    if enable_plot:
        fig = plt.figure(constrained_layout=True)        
    
        from matplotlib.gridspec import GridSpec
        gs = GridSpec(3, 2, figure=fig)
        ax1 = fig.add_subplot(gs[0, 0])
        ax2 = fig.add_subplot(gs[0, 1])
        ax3 = fig.add_subplot(gs[1, 0])
        ax4 = fig.add_subplot(gs[1, 1])
        ax5 = fig.add_subplot(gs[-1,:])  
              
        # show first few symbols of I(t), Q(t)
        ax1.plot(t,I)       
        ax2.plot(t,Q)
        ax3.plot(t,I_t,'r')
        ax4.plot(t,Q_t,'r')
        
        ax1.set_title('I(t)')
        ax2.set_title('Q(t)')
        ax3.set_title('$I(t) cos(2 \pi f_c t)$')
        ax4.set_title('$Q(t) sin(2 \pi f_c t)$')
        
        ax1.set_xlim(0,20*L/fs);ax2.set_xlim(0,20*L/fs)
        ax3.set_xlim(0,20*L/fs);ax4.set_xlim(0,20*L/fs)
        ax5.plot(t,s_t);ax5.set_xlim(0,20*L/fs);fig.show()
        ax5.set_title('$s(t) = I(t) cos(2 \pi f_c t) - Q(t) sin(2 \pi f_c t)$')
    
    result = dict()
    result['s(t)'] =s_t;result['I(t)'] = I;result['Q(t)'] = Q;result['t'] = t           
    return result