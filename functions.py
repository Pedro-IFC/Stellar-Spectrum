import cv2
import numpy as np
import matplotlib.pyplot as plt

def wavelength_to_rgb(wavelength, gamma=1.0): # Gamma 1.0 para cores mais saturadas
    """
    Converte um comprimento de onda (em nanômetros) para uma cor RGB.
    """
    wavelength = float(wavelength)
    if 380 <= wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif 440 <= wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif 490 <= wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif 510 <= wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif 580 <= wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif 645 <= wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    return (R, G, B)

def process_stellar_spectrum(image_path, p1, l1, p2, l2, output_name="spectrum_plot.png"):
    # 1. Carregar imagem
    img = cv2.imread(image_path)
    if img is None:
        print("Erro: Imagem não encontrada.")
        return
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Selecionar ROI e Processar Intensidade
    h, w = gray.shape
    slice_height = 40 
    roi = gray[int(h/2) - slice_height : int(h/2) + slice_height, :]
    intensity = np.sum(roi, axis=0)
    intensity = (intensity - np.min(intensity)) / (np.max(intensity) - np.min(intensity))

    # 3. Calibração
    m = (l2 - l1) / (p2 - p1)
    c = l1 - m * p1
    pixels = np.arange(w)
    wavelengths = m * pixels + c

    # 4. Plotting (Estilo Dark para cores fortes)
    plt.style.use('dark_background') # Isso faz as cores "brilharem"
    plt.figure(figsize=(14, 6))
    
    # Criar a barra de cores
    spectrum_colors = [wavelength_to_rgb(wl) for wl in wavelengths]
    background = np.array([spectrum_colors])
    
    # Aumentamos o alpha para 0.7 para cores mais densas
    plt.imshow(background, extent=[wavelengths.min(), wavelengths.max(), 0, 1.1], 
               aspect='auto', alpha=0.7)

    # Plotar a linha (agora branca para contrastar com o fundo escuro)
    plt.plot(wavelengths, intensity, color='white', linewidth=2, label='Intensidade')
    
    # Linhas de Balmer
    balmer_lines = {'H-alpha': 656.3, 'H-beta': 486.1, 'H-gamma': 434.0}
    for name, wave in balmer_lines.items():
        plt.axvline(x=wave, color='cyan', linestyle=':', alpha=0.8)
        plt.text(wave, 1.02, name, color='cyan', rotation=90, fontsize=10)

    plt.title(f"Espectro de Sirius: {image_path}", fontsize=14, pad=20)
    plt.xlabel("Comprimento de Onda (nm)")
    plt.ylabel("Intensidade Relativa")
    plt.xlim(400, 700)
    plt.ylim(0, 1.1)
    plt.grid(True, linestyle='--', alpha=0.2)
    
    plt.savefig(output_name, dpi=300, bbox_inches='tight')
    plt.show()