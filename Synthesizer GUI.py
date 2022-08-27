@@ -0,0 +1,210 @@
import tkinter as tk
import Eardrum_Destroyer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
import numpy as np 

## Defining window
root = tk.Tk()
root.title('Synthesizer')
#root.geometry('900x900')

## Lowest frequency of octave

current_wave = ()


def genWaveform(frequency, amplitude, osc_type):
    global current_wave
    
    if hash((frequency, amplitude, osc_type)) == current_wave:
        return
    
    
    plt.close()
    
    anim_running = False
    def animate(i):
        #fig.canvas.draw()
        
        if osc_type == 0:
            line.set_ydata(amplitude * np.sin( (frequency/(100) * x+i/10)))  # update the data
        
        elif osc_type == 1:
            line.set_ydata(amplitude * np.sign(np.sin( (frequency/(100) * x+i/10))))
        
        elif osc_type == 2:
            line.set_ydata(amplitude * np.arcsin(np.sin( (frequency/(100) * x+i/10))))
            
        return line,
    
    def onClick(event):
        nonlocal anim_running
        if anim_running:
            ani.event_source.stop()
            anim_running = False
        else:
            ani.event_source.start()
            anim_running = True
    
    fig = plt.figure()
    x = np.arange(0, 10, 0.1); 
    y = (amplitude * np.sin(x * frequency)) + amplitude

    canvas = FigureCanvasTkAgg(fig, master=wave_frame)
    
    ax = fig.add_subplot(111)
    ax.set_ylim(-amplitude-0.5, amplitude+0.5)
    ax.set_ylabel('Amplitude')
    ax.set_xlabel('Time')
    

    if osc_type == 0:    
        line, = ax.plot(x, (np.sin(frequency/100*x)))
    
    elif osc_type == 1:
        line, = ax.plot(x, amplitude * np.sign((np.sin(frequency/100*x))))
    
    elif osc_type == 2:
        line, = ax.plot(x, amplitude * np.arcsin(np.sin(frequency/100*x)))
    
    fig.canvas.mpl_connect('button_press_event', onClick)

    
    ani = animation.FuncAnimation(fig, animate, np.arange(1, 60), interval=20, blit=True,
                                  repeat=True)
    
    canvas.get_tk_widget().grid(row=0, column=1)
    current_wave = hash((frequency, amplitude, osc_type))
    
    
# =============================================================================
#     p = plot.plot(time, y)
#     plot.xlabel('Time')
#     plot.ylabel('Amplitude')
#     plot.grid(True, which='both')
#     plot.axhline(y=0, color='k')
#     
#     canvas = tk.FigureCanvasTkAgg(p, master=wave_frame)
#     plot_widget = canvas.get_tk_widget()
#     fig.show()
#     plot_widget.pack()
# =============================================================================
    
base_octave_freq = 220
amplitude = 0.2
## 0=sine, 1=sqaure, 2=triangle, 3=bad sawtooth, 4=good sawtooth
WAVE_TYPE = 0

def set_to_sin():
    global WAVE_TYPE
    WAVE_TYPE = 0

def set_to_sqr():
    global WAVE_TYPE
    WAVE_TYPE = 1

def set_to_tri():
    global WAVE_TYPE
    WAVE_TYPE = 2

## Runs when any key is pressed
def keyPress(key):
    ## Displays current key on label on window
    key_label.configure(text=key.char)
    
    ## All keys that play a note
    note_keys = 'zsxdcfvgbhnj'
    
    try:
        ## Finds index of current key in string
        note_index = note_keys.index(key.char) + 1
        
        ## Uses index to calculate frequency
        ## f = base * 2 ^ (n/12)
        f = base_octave_freq * (2**(note_index/12))
        
        waves = ['Sine', 'Square', 'Triangle', 'Good', 'bad']
        
        f_text = 'Frequency:  ' + str(round(f, 2)) + 'Hz'
        a_text = 'Amplitude:  ' + str(amplitude)
        w_text = 'Waveform Type:  ' + waves[WAVE_TYPE]
        
        frequency_label.configure(text=f_text)
        amplitude_label.configure(text=a_text)
        waveform_label.configure(text=w_text)
        
        ## Run oscillator at frequency, amplitude=0.5
        
        Eardrum_Destroyer.oscillator(freq=f, amp=amplitude, osc_type=WAVE_TYPE)
        
        genWaveform(f, amplitude, WAVE_TYPE)
       # animation.TimedAnimation._stop()
        root.bind('<Key>', keyPress)
        root.focus_set()

    except ValueError:
        print ('Invalid key')

## Frames for current key, waveform
key_frame = tk.LabelFrame(root, text='Pressed Key', padx=10, pady=10,
                          font=("System", 16, 'bold'))

wave_frame = tk.LabelFrame(root, text='Waveform', padx=10, pady=10,
                           font=("System", 16, 'bold'))

wave_control_frame = tk.LabelFrame(root, text='Waveform Type', padx=10, pady=10,
                                   font = ('System', 16, 'bold'))

info_panel_frame = tk.LabelFrame(root, text='Data Panel', padx=10, pady=10,
                                 font = ('System', 16, 'bold'))

## Starts listening for keystrokes and binds to callback function
key_frame.bind('<Key>', keyPress)
key_frame.focus_set()

## Labels
key_label = tk.Label(key_frame, text='-', font=("System", 17))
#wave_label = tk.Label(wave_frame, text='WAVE', font=("System", 17))

sin_photo = tk.PhotoImage(file = "sin_wave_icon.png")
sqr_photo = tk.PhotoImage(file = r"square_wave_icon.png")
tri_photo = tk.PhotoImage(file = r"tri_wave_icon.png")

sin_button = tk.Button(wave_control_frame, text='Sine Wave', command=set_to_sin,
                       image = sin_photo)
sqaure_button = tk.Button(wave_control_frame, text='Square Wave', command=set_to_sqr,
                          image = sqr_photo)
triangle_button = tk.Button(wave_control_frame, text='Triangle Wave', command=set_to_tri,
                            image = tri_photo)

frequency_label = tk.Label(info_panel_frame, text='Frequency (Hz):  ',
                           font = ('System', 16))

amplitude_label = tk.Label(info_panel_frame, text='Amplitude:  ',
                           font = ('System', 16, 'bold'))

waveform_label = tk.Label(info_panel_frame, text='Waveform Type:  ',
                           font = ('System', 16, 'bold'))

## Places widgets on  screen
key_frame.grid(row=0, column=0, padx=20, pady=10)
wave_frame.grid(row=0, column=1, padx=20, pady=10)
wave_control_frame.grid(row=0, column=2)
info_panel_frame.grid(row=2, columnspan=3)

sin_button.grid(row=0, column=0)
sqaure_button.grid(row=1, column=0)
triangle_button.grid(row=2, column=0)

frequency_label.pack()
amplitude_label.pack()
waveform_label.pack()

key_label.pack()
#wave_label.pack()

## Starts window mainloop
root.mainloop()