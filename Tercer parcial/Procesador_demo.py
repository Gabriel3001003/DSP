# pip install sounddevice ----> descargar la librería para poder reproducir el sonido

# Parte 1 - Importar las librerías 
import numpy as np 
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt 
import time 
import sounddevice as sd 
from scipy import signal
from scipy.io import wavfile

class DemoFiltros:
    def __init__(self, fs=8000):
        self.fs = fs  # Frecuencia de muestreo
        self.nyquist = fs / 2
      
    def cargar_audio(self, archivo):
        try:
            fs_orig, audio = wavfile.read(archivo)
            if audio.ndim > 1:
                audio = np.mean(audio, axis=1)  # Convertir a un solo canal 
            if audio.dtype == np.int16:
                audio = audio.astype(np.float32) / 32768.0
            
            if fs_orig != self.fs:
                num_muestras = int(len(audio) * self.fs / fs_orig)
                audio = signal.resample(audio, num_muestras)

            max_muestras = self.fs * 5 
            if len(audio) > max_muestras:
                audio = audio[:max_muestras]
            elif len(audio) < max_muestras:
                repeticiones = int(np.ceil(max_muestras / len(audio)))
                audio = np.tile(audio, repeticiones)[:max_muestras]
            
            duracion_final = len(audio) / self.fs
            
            return audio
        
        except Exception as e:
            print(f"Error al cargar el archivo de audio: {e}")
    
    def diseñar_filtro(self):
        fc = 800  # Frecuencia de corte en Hz
        fc = fc / self.nyquist  # Normalizar la frecuencia de corte
        h_fir = signal.firwin(41, fc, window='hamming')
        print("Diseñando filtro IIR.....")
        b_iir, a_iir = signal.butter(6, fc, btype='low')

        return h_fir, (b_iir, a_iir)
    
    def aplicar_filtro(self, audio, h_fir, iir_coefs):
        b_iir, a_iir = iir_coefs
        audio_fir = signal.lfilter(h_fir, 1, audio)
        audio_iir = signal.lfilter(b_iir, a_iir, audio)
        return audio_fir, audio_iir

    def reproducir_comparacion(self, audio_orig, audio_fir, audio_iir):
        # Normalizar los audios conservando las diferencias
        def normalizar(audio):
            max_val = np.max(np.abs(audio))
            if max_val > 0:
                return audio / max_val * 0.8
            return audio 
        
        original_norm = normalizar(audio_orig)
        fir_norm = normalizar(audio_fir)
        iir_norm = normalizar(audio_iir)

        duracion = len(original_norm) / self.fs

        try:
            print("Presiona ENTER para escuchar el audio original...")
            sd.play(original_norm, self.fs)
            sd.wait()
            time.sleep(1)  # Esperar un segundo antes de reproducir el siguiente audio
            print("Presiona ENTER para escuchar el audio FIR...")
            sd.play(fir_norm, self.fs)
            sd.wait()
            time.sleep(1)  # Esperar un segundo antes de reproducir el siguiente audio)
            print("Presiona ENTER para escuchar el audio IIR...")
            sd.play(iir_norm, self.fs)
            sd.wait()
            time.sleep(1)  # Esperar un segundo antes de reproducir el siguiente audio

            time.sleep(2)

            sd.play(original_norm, self.fs)
            sd.wait()
            sd.play(fir_norm, self.fs)
            sd.wait()
            sd.play(iir_norm, self.fs)
            sd.wait()

        except Exception as e:
            print(f"Error al reproducir el audio: {e}")
    
    def analizar_espectros(self, audio_orig, audio_fir, audio_iir, h_fir, iir_coefs):
        b_iir, a_iir = iir_coefs
        f, Pxx_orig = signal.welch(audio_orig, fs=self.fs, nperseg=1024)
        f, Pxx_fir = signal.welch(audio_fir, fs=self.fs, nperseg=1024)
        f, Pxx_iir = signal.welch(audio_iir, fs=self.fs, nperseg=1024)

        fig, axes = plt.subplots(2, 2)
        fig.suptitle('Análisis comparativo de Filtros Digitales')
        t = np.arange(len(audio_orig)) // self.fs
        muestras = self.fs * 2
        axes[0, 0].plot(t[:muestras], audio_orig[:muestras], 'b-', label='Original')
        axes[0, 0].plot(t[:muestras], audio_fir[:muestras], 'g-', label='FIR')
        axes[0, 0].plot(t[:muestras], audio_iir[:muestras], 'r-', label='IIR')
        axes[0, 0].set_title('Señales en el dominio del tiempo')
        axes[0, 0].set_xlabel('Tiempo [s]')
        axes[0, 0].set_ylabel('Amplitud')
        axes[0, 0].legend()
        # Espectro comparativo
        axes[0, 1].semilogy(f, Pxx_orig, 'b-', label='Original')
        axes[0, 1].semilogy(f, Pxx_fir, 'g-', label='FIR')
        axes[0, 1].semilogy(f, Pxx_iir, 'r-', label='IIR')
        axes[0, 1].set_title('Espectros de Potencia')
        axes[0, 1].set_xlabel('Frecuencia [Hz]')
        axes[0, 1].set_ylabel('PSD [V/Hz]')
        axes[0, 1].legend()
        axes[0, 1].axvline(800, color='k', linestyle='--', label='fc = 800 Hz')
        # Respuestas en frecuencia de los filtros
        w_fir, h_fir = signal.freqz(h_fir, worN=1024, fs = self.fs)
        w_iir, h_iir = signal.freqz(b_iir, a_iir, worN=1024, fs = self.fs)

        axes[1, 0].plot(w_fir, 20*np.log10(np.abs(h_fir)),'b-', linewidth=3, label='FIR')
        axes[1, 0].plot(w_iir, 20*np.log10(np.abs(h_iir)), 'r-', linewidth=3, label='IIR')
        axes[1, 0].set_title('Respuesta en Frecuencia de los Filtros')
        axes[1, 0].set_xlabel('Frecuencia [Hz]')
        axes[1, 0].set_ylabel('Magnitud [dB]')
        axes[1, 0].legend()
        axes[1, 0].axvline(800, color='k', linestyle='--', label='fc = 800 Hz')
        axes[1, 0].axhline(-3, color='k', linestyle='--', label='-3 dB')

        axes[1, 1].axis('off')

        snr_orig = self.calcular_snr(audio_orig)
        snr_fir = self.calcular_snr(audio_fir)
        snr_iir = self.calcular_snr(audio_iir)

        # Calcular atenuación 
        idx_800_fir = np.argmin(np.abs(w_fir - 800))
        idx_800_iir = np.argmin(np.abs(w_iir - 800))
        atenuacion_fir = 20 * np.log10(np.abs(h_fir[idx_800_fir]))
        atwenuacion_iir = 20 * np.log10(np.abs(h_iir[idx_800_iir]))

        # Reducción del ruido en las señales
        potencia_orig = np.var(audio_orig)
        potencia_fir = np.var(audio_fir)
        potencia_iir = np.var(audio_iir)

        reduccion_fir = 10 * np.log10(potencia_orig / potencia_fir) if potencia_fir > 0 else 0
        reduccion_iir = 10 * np.log10(potencia_orig / potencia_iir) if potencia_iir > 0 else 0

        plt.tight_layout()
        plt.show(block=True)  # <-- Cambia aquí
        return snr_orig, snr_fir, snr_iir
    
    def calcular_snr(self, audio):
        b_suave, a_suave = signal.butter(2, 0.1, btype='low')
        señal_estimada = signal.filtfilt(b_suave, a_suave, audio)
        ruido_estimado = audio - señal_estimada
        potencia_señal = np.var(señal_estimada)  # corregido nombre
        potencia_ruido = np.var(ruido_estimado)

        if potencia_ruido > 0:
            return 10 * np.log10(potencia_señal / potencia_ruido)
        else:
            return float('inf')  # Evitar división por cero
    
    def demo_completa(self,archivo): 
        # 1 - Cargar el audio
        audio_orig = self.cargar_audio(archivo)
        # 2 - Diseñar filtros
        h_fir, iir_coefs = self.diseñar_filtro()
        # 3 - Aplicar filtos
        audio_fir, audio_iir = self.aplicar_filtro(audio_orig, h_fir, iir_coefs)
        # 4 - Analisis visual
        snr_orig,snr_fir, snr_iir = self.analizar_espectros(audio_orig, audio_fir, audio_iir, h_fir, iir_coefs)
        # 5 - Cinparación auditiva 
        respuesta = input('¿Reproducir comparación auditiva de 5 segundos? (s/n): ')
        if respuesta.lower() == 's':
            self.reproducir_comparacion(audio_orig, audio_fir, audio_iir)  
    
    @staticmethod
    def main():
        demo = DemoFiltros()
        import os
        archivos_disponibles = [f for f in os.listdir('.') if f.endswith('.wav')]

        if not archivos_disponibles:
            print("No se encontraron archivos .wav en el directorio actual.")
            return  # Terminar si no hay archivos de audio

        print("\nArchivos disponibles:")
        for i, archivo in enumerate(archivos_disponibles):
            print(f"{i + 1}. {archivo}")

        try:
            opcion = int(input(f'\nSeleccione archivo (1-{len(archivos_disponibles)}): ')) - 1
            if 0 <= opcion < len(archivos_disponibles):
                archivo_seleccionado = archivos_disponibles[opcion]
            else:
                print("Opción fuera de rango. Se seleccionará el primer archivo.")
                archivo_seleccionado = archivos_disponibles[0]
        except Exception as e:
            print(f"Entrada inválida: {e}. Se seleccionará el primer archivo.")
            archivo_seleccionado = archivos_disponibles[0]

        try:
            demo.demo_completa(archivo_seleccionado)
        except Exception as e:
            print(f"Error en la demo: {e}")
            
if __name__ == "__main__":
    DemoFiltros.main()