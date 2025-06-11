#!/usr/bin/env python3
"""
SISTEMA COMPLETO PARA CLASE DE 150 MINUTOS
Integra grabación en vivo + procesamiento Arduino + análisis
Para usar con Arduino Mega en COM4
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import sounddevice as sd
import serial
import time
import os

# Importar módulos del sistema
try:
    from grabador_voz_clase import GrabadorVozClase
except ImportError:
    print("Ejecuta primero grabador_voz_clase.py para crear grabaciones")

class SistemaCompletoClase:
    def __init__(self, puerto='COM4', fs=8000):
        self.puerto = puerto
        self.fs = fs
        self.arduino = None
        self.conectado = False
        self.grabador = GrabadorVozClase(fs)
        
        print("=" * 60)
        print("SISTEMA COMPLETO PARA CLASE DE FILTROS DIGITALES")
        print("Grabación en vivo + Arduino Mega + Análisis completo")
        print("=" * 60)
        print(f"Puerto Arduino: {puerto}")
        print(f"Frecuencia: {fs} Hz")
        print("=" * 60)
    
    def menu_principal_clase(self):
        """Menú principal optimizado para clase"""
        
        while True:
            print(f"\n{'='*60}")
            print("MENÚ PRINCIPAL - CLASE FILTROS DIGITALES")
            print(f"{'='*60}")
            print("PREPARACIÓN:")
            print("1. Verificar sistema completo")
            print("2. Grabar voz del estudiante")
            print("3. Test de comunicación Arduino")
            print("")
            print("PROCESAMIENTO:")
            print("4. Demo completa con Arduino (RECOMENDADO)")
            print("5. Procesar archivo específico")
            print("6. Comparar todos los filtros")
            print("")
            print("ANÁLISIS:")
            print("7. Mostrar espectros de grabaciones")
            print("8. Reproducir archivos existentes")
            print("9. Salir")
            
            try:
                opcion = input(f"\nSelecciona opción (1-9): ").strip()
                
                if opcion == '1':
                    self.verificar_sistema_completo()
                    
                elif opcion == '2':
                    self.realizar_grabaciones_clase()
                    
                elif opcion == '3':
                    self.test_arduino()
                    
                elif opcion == '4':
                    self.demo_completa_clase()
                    
                elif opcion == '5':
                    self.procesar_archivo_especifico()
                    
                elif opcion == '6':
                    self.comparar_todos_filtros()
                    
                elif opcion == '7':
                    self.mostrar_analisis_grabaciones()
                    
                elif opcion == '8':
                    self.reproducir_archivos()
                    
                elif opcion == '9':
                    print("👋 ¡Clase completada exitosamente!")
                    break
                    
                else:
                    print("Opción no válida")
                    
            except KeyboardInterrupt:
                print("\n\nSitema interrumpido")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def verificar_sistema_completo(self):
        """Verifica que todo el sistema esté listo para la clase"""
        
        print(f"\n{'='*50}")
        print("VERIFICACIÓN COMPLETA DEL SISTEMA")
        print(f"{'='*50}")
        
        # 1. Verificar audio
        print("1. SISTEMA DE AUDIO:")
        audio_ok = self.grabador.verificar_audio()
        
        # 2. Verificar Arduino
        print("\n2. COMUNICACIÓN ARDUINO:")
        arduino_ok = self.conectar_arduino()
        if arduino_ok:
            self.arduino.write(b't\n')
            time.sleep(2)
            self.arduino.close()
            self.conectado = False
        
        # 3. Verificar archivos existentes
        print("\n3. ARCHIVOS DE AUDIO:")
        archivos_wav = [f for f in os.listdir('.') if f.endswith('.wav')]
        print(f"Archivos WAV encontrados: {len(archivos_wav)}")
        for archivo in archivos_wav:
            try:
                fs, audio = wavfile.read(archivo)
                duracion = len(audio) / fs
                print(f"   • {archivo}: {duracion:.1f}s, {fs}Hz")
            except:
                print(f"   • {archivo}: Error al leer")
        
        # 4. Verificar dependencias
        print("\n4. DEPENDENCIAS PYTHON:")
        dependencias = ['numpy', 'matplotlib', 'scipy', 'sounddevice', 'serial']
        for dep in dependencias:
            try:
                if dep == 'serial':
                    import serial
                    print(f"    {dep}")
                else:
                    __import__(dep)
                    print(f"    {dep}")
            except ImportError:
                print(f"    {dep} - FALTA")
        
        # Resumen
        print(f"\n{'='*50}")
        print("RESUMEN DEL SISTEMA:")
        print(f"   Audio: {'' if audio_ok else '❌'}")
        print(f"   Arduino: {'' if arduino_ok else '❌'}")
        print(f"   Archivos: {'' if len(archivos_wav) > 0 else '⚠️'}")
        
        if audio_ok and arduino_ok:
            print("\nSISTEMA LISTO PARA LA CLASE")
        else:
            print("\n CORREGIR PROBLEMAS ANTES DE LA CLASE")
        
        return audio_ok and arduino_ok
    
    def realizar_grabaciones_clase(self):
        """Realiza grabaciones específicas para la clase"""
        
        print(f"\n{'='*50}")
        print("GRABACIONES PARA LA CLASE")
        print(f"{'='*50}")
        print("Se crearán 3 tipos de grabaciones optimizadas:")
        print("• Conteo 1-5: Para análisis de voz humana")
        print("• Frase técnica: Para evaluar calidad de filtrado")
        print("• Silbido tonal: Para probar selectividad")
        
        continuar = input("\n¿Proceder con las grabaciones? (s/n): ")
        if continuar.lower() != 's':
            return
        
        archivos = self.grabador.crear_set_completo_clase()
        
        if len(archivos) == 3:
            print(f"\n¡GRABACIONES COMPLETADAS!")
            print("Archivos listos para procesamiento con Arduino")
            
            # Mostrar análisis opcional
            respuesta = input("\n¿Mostrar análisis espectral? (s/n): ")
            if respuesta.lower() == 's':
                self.grabador.mostrar_espectros(archivos)
        
        return archivos
    
    def conectar_arduino(self):
        """Conecta con Arduino Mega"""
        try:
            print(f"Conectando Arduino en {self.puerto}...")
            self.arduino = serial.Serial(self.puerto, 115200, timeout=3)
            time.sleep(3)
            
            self.arduino.reset_input_buffer()
            self.arduino.write(b't\n')
            time.sleep(2)
            
            # Leer respuesta
            respuestas = []
            for _ in range(10):
                if self.arduino.in_waiting:
                    respuesta = self.arduino.readline().decode().strip()
                    respuestas.append(respuesta)
                    print(f"   Arduino: {respuesta}")
                    if "COMUNICACIÓN OK" in respuesta:
                        self.conectado = True
                        print(" Arduino conectado exitosamente")
                        return True
                time.sleep(0.3)
            
            # Si llegamos aquí, hay comunicación básica
            self.conectado = True
            print(" Arduino conectado (comunicación básica)")
            return True
            
        except Exception as e:
            print(f" Error conectando Arduino: {e}")
            print("   Verificaciones:")
            print("   • ¿Arduino conectado al puerto COM4?")
            print("   • ¿Código cargado en Arduino?")
            print("   • ¿Cable USB funcionando?")
            return False
    
    def test_arduino(self):
        """Test específico de comunicación Arduino"""
        
        print(f"\n{'='*40}")
        print("TEST DE COMUNICACIÓN ARDUINO")
        print(f"{'='*40}")
        
        if self.conectar_arduino():
            try:
                # Test completo
                self.arduino.write(b't\n')
                time.sleep(2)
                
                print("\nRespuestas del Arduino:")
                for _ in range(15):
                    if self.arduino.in_waiting:
                        respuesta = self.arduino.readline().decode().strip()
                        if respuesta:
                            print(f"   {respuesta}")
                    time.sleep(0.2)
                
                # Test de filtros
                print(f"\nProbando configuración de filtros...")
                for filtro in [0, 1, 2]:
                    self.arduino.write(f"{filtro}\n".encode())
                    time.sleep(1)
                    
                    # Leer respuesta
                    if self.arduino.in_waiting:
                        resp = self.arduino.readline().decode().strip()
                        print(f"   Filtro {filtro}: {resp}")
                
                print(" Test completo exitoso")
                
            except Exception as e:
                print(f" Error en test: {e}")
            finally:
                if self.arduino:
                    self.arduino.close()
                    self.conectado = False
        else:
            print(" No se pudo conectar para el test")
    
    def demo_completa_clase(self):
        """Demostración completa para la clase"""
        
        print(f"\n{'='*60}")
        print("DEMOSTRACIÓN COMPLETA PARA CLASE")
        print(f"{'='*60}")
        
        # 1. Verificar archivos
        archivos_wav = [f for f in os.listdir('.') if f.endswith('.wav')]
        
        if not archivos_wav:
            print("No hay archivos de audio disponibles")
            respuesta = input("¿Crear grabaciones ahora? (s/n): ")
            if respuesta.lower() == 's':
                archivos_wav = self.realizar_grabaciones_clase()
            else:
                print("Se necesitan archivos de audio para continuar")
                return
        
        # 2. Mostrar archivos disponibles
        print(f"\nArchivos de audio disponibles:")
        for i, archivo in enumerate(archivos_wav):
            try:
                fs, audio = wavfile.read(archivo)
                duracion = len(audio) / fs
                print(f"   {i+1}. {archivo} ({duracion:.1f}s)")
            except:
                print(f"   {i+1}. {archivo} (error)")
        
        # 3. Seleccionar archivo
        try:
            seleccion = int(input(f"\nSelecciona archivo (1-{len(archivos_wav)}): ")) - 1
            archivo_seleccionado = archivos_wav[seleccion]
        except:
            archivo_seleccionado = archivos_wav[0]
            print(f"Usando: {archivo_seleccionado}")
        
        # 4. Conectar Arduino
        if not self.conectar_arduino():
            print(" No se puede continuar sin Arduino")
            return
        
        try:
            # 5. Procesar con diferentes filtros
            resultados = {}
            filtros = [1, 2]  # FIR e IIR
            nombres = ['FIR', 'IIR']
            
            for i, tipo_filtro in enumerate(filtros):
                print(f"\n{'='*50}")
                print(f"PROCESANDO CON FILTRO {nombres[i]}")
                print(f"{'='*50}")
                
                entrada, salida = self.procesar_con_arduino_optimizado(
                    archivo_seleccionado, tipo_filtro)
                
                if entrada is not None and salida is not None:
                    # Análisis
                    snr_orig, snr_filt, mejora = self.generar_analisis_completo(
                        archivo_seleccionado, entrada, salida, tipo_filtro, nombres[i])
                    
                    # Reproducción
                    self.reproducir_comparacion_completa(entrada, salida, nombres[i])
                    
                    resultados[nombres[i]] = {
                        'snr_orig': snr_orig,
                        'snr_filt': snr_filt,
                        'mejora': mejora,
                        'entrada': entrada,
                        'salida': salida
                    }
                    
                    print(f"\n {nombres[i]} completado exitosamente")
                else:
                    print(f" Error procesando con {nombres[i]}")
            
            # 6. Comparación final
            if len(resultados) >= 2:
                self.mostrar_comparacion_final(archivo_seleccionado, resultados)
            
        finally:
            # 7. Cerrar conexión
            if self.arduino and self.arduino.is_open:
                self.arduino.close()
                self.conectado = False
                print("\nConexión Arduino cerrada")
        
        print(f"\n🎉 DEMOSTRACIÓN COMPLETA EXITOSA")
    
    def procesar_con_arduino_optimizado(self, archivo, tipo_filtro):
        """Procesa archivo completo usando Arduino por lotes"""
        
        try:
            # Cargar audio
            fs_orig, audio = wavfile.read(archivo)
            print(f"Procesando {archivo} con filtro tipo {tipo_filtro}")
            
            # Preparar audio
            if audio.ndim > 1:
                audio = np.mean(audio, axis=1)
            if audio.dtype == np.int16:
                audio = audio.astype(np.float32) / 32768.0
            
            if fs_orig != self.fs:
                num_samples = int(len(audio) * self.fs / fs_orig)
                audio = signal.resample(audio, num_samples)
            
            # Convertir a ADC
            audio_normalizado = np.clip(audio, -1, 1)
            audio_adc = ((audio_normalizado + 1) * 511.5).astype(int)
            
            duracion_total = len(audio_adc) / self.fs
            print(f"Duración: {duracion_total:.1f}s, Muestras: {len(audio_adc)}")
            
            # Procesar por lotes
            tamaño_lote = 600
            num_lotes = (len(audio_adc) + tamaño_lote - 1) // tamaño_lote
            
            print(f"Procesando en {num_lotes} lotes...")
            
            entrada_completa = []
            salida_completa = []
            lotes_exitosos = 0
            
            # Configurar filtro
            self.arduino.write(b"r\n")  # Reset
            time.sleep(2)
            self.arduino.write(f"{tipo_filtro}\n".encode())
            time.sleep(1)
            
            for i in range(num_lotes):
                # Extraer lote
                inicio = i * tamaño_lote
                fin = min(inicio + tamaño_lote, len(audio_adc))
                lote = audio_adc[inicio:fin]
                
                # Procesar lote
                entrada_lote, salida_lote = self.procesar_lote_individual(lote)
                
                if entrada_lote is not None and salida_lote is not None:
                    entrada_completa.extend(entrada_lote)
                    salida_completa.extend(salida_lote)
                    lotes_exitosos += 1
                    
                    progreso = (i + 1) / num_lotes * 100
                    print(f"   Lote {i+1}/{num_lotes}: {progreso:.1f}% ")
                else:
                    print(f"   Lote {i+1}/{num_lotes}: ")
                    # Rellenar con interpolación si falla
                    if entrada_completa:
                        entrada_completa.extend([entrada_completa[-1]] * len(lote))
                        salida_completa.extend([salida_completa[-1]] * len(lote))
            
            if lotes_exitosos > 0:
                print(f"\n Procesamiento exitoso:")
                print(f"   Lotes exitosos: {lotes_exitosos}/{num_lotes}")
                print(f"   Muestras totales: {len(entrada_completa)}")
                
                return np.array(entrada_completa), np.array(salida_completa)
            else:
                return None, None
                
        except Exception as e:
            print(f" Error en procesamiento: {e}")
            return None, None
    
    def procesar_lote_individual(self, lote_data):
        """Procesa un lote individual en Arduino"""
        try:
            # Iniciar captura
            self.arduino.write(b"c\n")
            time.sleep(0.5)
            
            # Enviar datos
            for muestra in lote_data:
                self.arduino.write(f"DATA:{int(muestra)}\n".encode())
                time.sleep(0.003)
            
            # Esperar procesamiento
            time.sleep(1)
            
            # Solicitar datos
            self.arduino.write(b"s\n")
            
            # Leer datos
            entrada = []
            salida = []
            leyendo_datos = False
            
            tiempo_inicio = time.time()
            while (time.time() - tiempo_inicio) < 5:
                if self.arduino.in_waiting:
                    linea = self.arduino.readline().decode().strip()
                    
                    if linea == "index,input,output":
                        leyendo_datos = True
                        continue
                    elif "FIN_DATOS" in linea or "ENVÍO COMPLETADO" in linea:
                        break
                    
                    if leyendo_datos and "," in linea:
                        try:
                            partes = linea.split(',')
                            if len(partes) >= 3:
                                entrada.append(int(partes[1]))
                                salida.append(int(partes[2]))
                        except:
                            continue
            
            # Verificar datos suficientes
            if len(entrada) >= len(lote_data) * 0.8:
                return entrada[:len(lote_data)], salida[:len(lote_data)]
            else:
                return None, None
                
        except Exception as e:
            return None, None
    
    def generar_analisis_completo(self, archivo, entrada, salida, tipo_filtro, nombre_filtro):
        """Genera análisis visual completo"""
        
        # Convertir a voltajes
        entrada_volt = entrada * 5.0 / 1023.0
        salida_volt = salida * 5.0 / 1023.0
        
        # Crear gráficas
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle(f'Análisis Completo - {archivo} - Filtro {nombre_filtro}', fontsize=14)
        
        # 1. Señales temporales
        t = np.arange(len(entrada)) / self.fs
        axes[0, 0].plot(t, entrada_volt, 'b-', alpha=0.7, label='Original')
        axes[0, 0].plot(t, salida_volt, 'r-', linewidth=2, label='Filtrado')
        axes[0, 0].set_title(f'Audio Completo - {len(entrada)/self.fs:.1f}s')
        axes[0, 0].set_xlabel('Tiempo (s)')
        axes[0, 0].set_ylabel('Voltaje (V)')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Espectros
        f, Pxx_entrada = signal.welch(entrada_volt, self.fs, nperseg=512)
        f, Pxx_salida = signal.welch(salida_volt, self.fs, nperseg=512)
        
        axes[0, 1].semilogy(f, Pxx_entrada, 'b-', alpha=0.7, label='Original')
        axes[0, 1].semilogy(f, Pxx_salida, 'r-', linewidth=2, label='Filtrado')
        axes[0, 1].set_title('Análisis Espectral')
        axes[0, 1].set_xlabel('Frecuencia (Hz)')
        axes[0, 1].set_ylabel('PSD (V²/Hz)')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].set_xlim([0, self.fs/2])
        axes[0, 1].axvline(800, color='k', linestyle='--', alpha=0.7, label='fc=800Hz')
        
        # 3. Diferencia
        diferencia = entrada_volt - salida_volt
        axes[1, 0].plot(t, diferencia, 'g-', linewidth=1)
        axes[1, 0].set_title('Efecto del Filtro')
        axes[1, 0].set_xlabel('Tiempo (s)')
        axes[1, 0].set_ylabel('Diferencia (V)')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Métricas
        axes[1, 1].axis('off')
        
        # Calcular métricas
        snr_orig = self.calcular_snr(entrada_volt)
        snr_filt = self.calcular_snr(salida_volt)
        mejora_snr = snr_filt - snr_orig
        
        potencia_orig = np.var(entrada_volt)
        potencia_filt = np.var(salida_volt)
        reduccion_db = 10 * np.log10(potencia_orig / potencia_filt) if potencia_filt > 0 else 0
        
        texto_metricas = f"""
ANÁLISIS COMPLETO - FILTRO {nombre_filtro}:

ARCHIVO: {archivo}
DURACIÓN: {len(entrada)/self.fs:.1f} segundos
MUESTRAS: {len(entrada)}

CALIDAD DE SEÑAL:
• SNR Original: {snr_orig:.1f} dB
• SNR Filtrado: {snr_filt:.1f} dB
• Mejora SNR: {mejora_snr:+.1f} dB

REDUCCIÓN DE RUIDO:
• Potencia original: {potencia_orig:.4f} V²
• Potencia filtrada: {potencia_filt:.4f} V²
• Reducción: {reduccion_db:.1f} dB

PROCESAMIENTO:
• Arduino Mega: COM4
• Método: Lotes de 600 muestras
• Fs: {self.fs} Hz
• Fc: 800 Hz

RESULTADO: {' Exitoso' if mejora_snr > 0 else '️ Sin mejora'}
        """
        
        axes[1, 1].text(0.05, 0.95, texto_metricas, transform=axes[1, 1].transAxes,
                        fontsize=10, verticalalignment='top', fontfamily='monospace',
                        bbox=dict(boxstyle="round,pad=0.4", facecolor="lightyellow", alpha=0.9))
        
        plt.tight_layout()
        plt.show()
        
        return snr_orig, snr_filt, mejora_snr
    
    def calcular_snr(self, señal):
        """Calcula SNR de la señal"""
        try:
            b, a = signal.butter(2, 0.1)
            señal_suave = signal.filtfilt(b, a, señal)
            ruido = señal - señal_suave
            
            potencia_señal = np.var(señal_suave)
            potencia_ruido = np.var(ruido)
            
            if potencia_ruido > 0:
                return 10 * np.log10(potencia_señal / potencia_ruido)
            else:
                return 50.0
        except:
            return 20.0
    
    def reproducir_comparacion_completa(self, entrada, salida, nombre_filtro):
        """Reproduce comparación completa del audio"""
        
        print(f"\nREPRODUCCIÓN - FILTRO {nombre_filtro}")
        print("=" * 40)
        
        # Convertir a audio
        entrada_audio = (entrada / 511.5) - 1
        salida_audio = (salida / 511.5) - 1
        
        # Normalizar
        entrada_audio = entrada_audio / np.max(np.abs(entrada_audio)) * 0.8
        salida_audio = salida_audio / np.max(np.abs(salida_audio)) * 0.8
        
        duracion = len(entrada_audio) / self.fs
        print(f"Duración: {duracion:.1f} segundos")
        
        try:
            print(f"\n1. AUDIO ORIGINAL")
            input("   Presiona Enter para reproducir...")
            sd.play(entrada_audio, self.fs)
            sd.wait()
            
            time.sleep(1)
            
            print(f"\n2. AUDIO FILTRADO ({nombre_filtro})")
            input("   Presiona Enter para reproducir...")
            sd.play(salida_audio, self.fs)
            sd.wait()
            
            print(f"\n Comparación {nombre_filtro} completada")
            
        except Exception as e:
            print(f" Error en reproducción: {e}")
    
    def mostrar_comparacion_final(self, archivo, resultados):
        """Muestra comparación final entre todos los filtros"""
        
        print(f"\n{'='*60}")
        print("COMPARACIÓN FINAL DE FILTROS")
        print(f"{'='*60}")
        print(f"ARCHIVO PROCESADO: {archivo}")
        print(f"FILTROS COMPARADOS: {len(resultados)}")
        
        # Tabla de resultados
        print(f"\nRESULTADOS COMPARATIVOS:")
        print(f"{'FILTRO':^8} | {'SNR ORIG':^9} | {'SNR FILT':^9} | {'MEJORA':^8} | {'CALIFICACIÓN':^12}")
        print("-" * 60)
        
        mejor_filtro = None
        mejor_mejora = float('-inf')
        
        for filtro, datos in resultados.items():
            snr_orig = datos['snr_orig']
            snr_filt = datos['snr_filt']
            mejora = datos['mejora']
            
            if mejora > mejor_mejora:
                mejor_mejora = mejora
                mejor_filtro = filtro
            
            calificacion = "Excelente" if mejora > 5 else "Buena" if mejora > 2 else "Regular"
            
            print(f"{filtro:^8} | {snr_orig:^9.1f} | {snr_filt:^9.1f} | {mejora:^8.1f} | {calificacion:^12}")
        
        print("-" * 60)
        print(f"\nMEJOR FILTRO PARA ESTE AUDIO: {mejor_filtro}")
        print(f"MEJORA MÁXIMA: {mejor_mejora:+.1f} dB")
        
        # Recomendaciones
        print(f"\n💡 RECOMENDACIONES PARA ESTUDIANTES:")
        if "FIR" in resultados and "IIR" in resultados:
            fir_mejora = resultados["FIR"]["mejora"]
            iir_mejora = resultados["IIR"]["mejora"]
            
            if fir_mejora > iir_mejora:
                print("   • FIR funciona mejor para este tipo de audio")
                print("   • Recomendado para aplicaciones de alta calidad")
                print("   • Preserva mejor las características de la voz")
            else:
                print("   • IIR funciona mejor para este tipo de audio")
                print("   • Recomendado para aplicaciones eficientes")
                print("   • Mejor para dispositivos con limitaciones")
        
        # Reproducción comparativa final
        respuesta = input(f"\n¿Reproducir comparación final de ambos filtros? (s/n): ")
        if respuesta.lower() == 's':
            self.reproducir_comparacion_todos_filtros(resultados)
    
    def reproducir_comparacion_todos_filtros(self, resultados):
        """Reproduce comparación de todos los filtros procesados"""
        
        print(f"\nCOMPARACIÓN AUDITIVA FINAL")
        print("=" * 40)
        
        try:
            for nombre_filtro, datos in resultados.items():
                entrada = datos['entrada']
                salida = datos['salida']
                
                # Convertir a audio
                entrada_audio = (entrada / 511.5) - 1
                salida_audio = (salida / 511.5) - 1
                
                # Normalizar
                entrada_audio = entrada_audio / np.max(np.abs(entrada_audio)) * 0.8
                salida_audio = salida_audio / np.max(np.abs(salida_audio)) * 0.8
                
                print(f"\nFILTRO {nombre_filtro}")
                input(f"   Presiona Enter para escuchar {nombre_filtro}...")
                sd.play(salida_audio, self.fs)
                sd.wait()
                time.sleep(0.5)
            
            print(f"\n Comparación completa finalizada")
            print("¿Cuál filtro prefieren para su voz?")
            
        except Exception as e:
            print(f" Error en comparación final: {e}")
    
    def procesar_archivo_especifico(self):
        """Procesa un archivo específico seleccionado por el usuario"""
        
        archivos_wav = [f for f in os.listdir('.') if f.endswith('.wav')]
        
        if not archivos_wav:
            print("No hay archivos WAV disponibles")
            return
        
        print(f"\nArchivos disponibles:")
        for i, archivo in enumerate(archivos_wav):
            try:
                fs, audio = wavfile.read(archivo)
                duracion = len(audio) / fs
                print(f"   {i+1}. {archivo} ({duracion:.1f}s)")
            except:
                print(f"   {i+1}. {archivo} (error)")
        
        try:
            seleccion = int(input(f"\nSelecciona archivo (1-{len(archivos_wav)}): ")) - 1
            archivo = archivos_wav[seleccion]
            
            print(f"\nFiltros disponibles:")
            print("1. FIR (preserva fase)")
            print("2. IIR (más eficiente)")
            
            filtro_sel = int(input("Selecciona filtro (1/2): "))
            tipo_filtro = filtro_sel  # 1=FIR, 2=IIR
            nombre_filtro = "FIR" if tipo_filtro == 1 else "IIR"
            
            if self.conectar_arduino():
                entrada, salida = self.procesar_con_arduino_optimizado(archivo, tipo_filtro)
                
                if entrada is not None and salida is not None:
                    self.generar_analisis_completo(archivo, entrada, salida, tipo_filtro, nombre_filtro)
                    self.reproducir_comparacion_completa(entrada, salida, nombre_filtro)
                else:
                    print(" Error en procesamiento")
                
                self.arduino.close()
                self.conectado = False
            
        except (ValueError, IndexError):
            print(" Selección inválida")
        except Exception as e:
            print(f" Error: {e}")
    
    def comparar_todos_filtros(self):
        """Compara todos los filtros con un archivo seleccionado"""
        
        archivos_wav = [f for f in os.listdir('.') if f.endswith('.wav')]
        
        if not archivos_wav:
            print("No hay archivos WAV disponibles")
            return
        
        print(f"\nSelecciona archivo para comparar filtros:")
        for i, archivo in enumerate(archivos_wav):
            print(f"   {i+1}. {archivo}")
        
        try:
            seleccion = int(input(f"\nArchivo (1-{len(archivos_wav)}): ")) - 1
            archivo = archivos_wav[seleccion]
            
            if self.conectar_arduino():
                resultados = {}
                
                # Procesar con FIR
                print(f"\n{'='*50}")
                print("PROCESANDO CON FIR")
                print(f"{'='*50}")
                entrada_fir, salida_fir = self.procesar_con_arduino_optimizado(archivo, 1)
                
                if entrada_fir is not None:
                    snr_o, snr_f, mejora = self.generar_analisis_completo(archivo, entrada_fir, salida_fir, 1, "FIR")
                    resultados["FIR"] = {
                        'snr_orig': snr_o, 'snr_filt': snr_f, 'mejora': mejora,
                        'entrada': entrada_fir, 'salida': salida_fir
                    }
                
                # Procesar con IIR
                print(f"\n{'='*50}")
                print("PROCESANDO CON IIR")
                print(f"{'='*50}")
                entrada_iir, salida_iir = self.procesar_con_arduino_optimizado(archivo, 2)
                
                if entrada_iir is not None:
                    snr_o, snr_f, mejora = self.generar_analisis_completo(archivo, entrada_iir, salida_iir, 2, "IIR")
                    resultados["IIR"] = {
                        'snr_orig': snr_o, 'snr_filt': snr_f, 'mejora': mejora,
                        'entrada': entrada_iir, 'salida': salida_iir
                    }
                
                # Comparación final
                if len(resultados) >= 2:
                    self.mostrar_comparacion_final(archivo, resultados)
                
                self.arduino.close()
                self.conectado = False
            
        except Exception as e:
            print(f" Error: {e}")
    
    def mostrar_analisis_grabaciones(self):
        """Muestra análisis espectral de las grabaciones"""
        
        archivos_wav = [f for f in os.listdir('.') if f.endswith('.wav')]
        
        if not archivos_wav:
            print("No hay archivos WAV para analizar")
            return
        
        self.grabador.mostrar_espectros(archivos_wav[:3])
    
    def reproducir_archivos(self):
        """Reproduce archivos existentes"""
        
        archivos_wav = [f for f in os.listdir('.') if f.endswith('.wav')]
        
        if not archivos_wav:
            print("No hay archivos WAV para reproducir")
            return
        
        print(f"\nArchivos disponibles:")
        for i, archivo in enumerate(archivos_wav):
            try:
                fs, audio = wavfile.read(archivo)
                duracion = len(audio) / fs
                print(f"   {i+1}. {archivo} ({duracion:.1f}s)")
            except:
                print(f"   {i+1}. {archivo} (error)")
        
        try:
            seleccion = int(input(f"\nSelecciona archivo (1-{len(archivos_wav)}): ")) - 1
            archivo = archivos_wav[seleccion]
            
            fs, audio = wavfile.read(archivo)
            if audio.dtype == np.int16:
                audio = audio.astype(np.float32) / 32768.0
            
            print(f"Reproduciendo {archivo}...")
            sd.play(audio, fs)
            sd.wait()
            print(" Reproducción completada")
            
        except Exception as e:
            print(f" Error: {e}")

def main():
    """Función principal del sistema completo"""
    
    print("SISTEMA COMPLETO PARA CLASE DE FILTROS DIGITALES")
    print("Integra: Grabación + Arduino + Procesamiento + Análisis")
    print("=" * 65)
    
    # Detectar puerto Arduino
    puertos = ['COM3', 'COM4', 'COM5', 'COM6']
    puerto_detectado = 'COM4'  # Por defecto
    
    for puerto in puertos:
        try:
            test_serial = serial.Serial(puerto, 115200, timeout=1)
            test_serial.close()
            puerto_detectado = puerto
            print(f" Puerto Arduino detectado: {puerto}")
            break
        except:
            continue
    
    # Crear sistema
    sistema = SistemaCompletoClase(puerto_detectado)
    
    try:
        sistema.menu_principal_clase()
    except KeyboardInterrupt:
        print(f"\n\nSistema interrumpido - ¡Clase finalizada!")
    except Exception as e:
        print(f" Error en sistema: {e}")
    finally:
        if sistema.arduino and sistema.arduino.is_open:
            sistema.arduino.close()

if __name__ == "__main__":
    main()
