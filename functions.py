import cv2
import numpy as np
import matplotlib.pyplot as plt

def process_stellar_spectrum(image_path, p1, l1, p2, l2, output_name="spectrum_plot.png"):
    """
    image_path: Path to your Sirius photo
    p1, p2: Pixel coordinates of your two calibration points (from the CFL bulb)
    l1, l2: Known wavelengths for those points (e.g., 435.8 and 546.1)
    """
    # 1. Load and convert to Grayscale
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Image not found.")
        return
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Select Region of Interest (ROI)
    # We take a horizontal slice of the middle of the image
    h, w = gray.shape
    slice_height = 40 
    roi = gray[int(h/2) - slice_height : int(h/2) + slice_height, :]

    # 3. Collapse 2D image into 1D Signal (Vertical Sum)
    intensity = np.sum(roi, axis=0)

    # 4. Normalize (0 to 1 scale)
    intensity = (intensity - np.min(intensity)) / (np.max(intensity) - np.min(intensity))

    # 5. Wavelength Calibration (Linear Regression: y = mx + c)
    # We calculate the scale: nanometers per pixel
    m = (l2 - l1) / (p2 - p1)
    c = l1 - m * p1
    
    pixels = np.arange(w)
    wavelengths = m * pixels + c

    # 6. Plotting
    plt.figure(figsize=(14, 6))
    plt.plot(wavelengths, intensity, color='black', label='Observed Spectrum')
    
    # Mark expected Balmer Lines for Sirius (A1V Star)
    balmer_lines = {'H-alpha': 656.3, 'H-beta': 486.1, 'H-gamma': 434.0}
    for name, wave in balmer_lines.items():
        plt.axvline(x=wave, color='red', linestyle='--', alpha=0.5)
        plt.text(wave, 0.9, name, color='red', rotation=90)

    plt.title(f"Spectral Analysis of Sirius - {image_path}")
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Relative Intensity")
    plt.xlim(400, 700) # Visible spectrum range
    plt.ylim(0, 1.1)
    plt.grid(True, which='both', linestyle=':', alpha=0.5)
    plt.legend()
    
    plt.savefig(output_name)
    plt.show()

# --- HOW TO USE ---
# 1. Identify your calibration pixels from your CFL bulb photo
# Point 1: Mercury Blue Line (435.8 nm) at Pixel XXX
# Point 2: Mercury Green Line (546.1 nm) at Pixel YYY

# 2. Run the function (example values below)
# process_stellar_spectrum('sirius_telescope.jpg', p1=420, l1=435.8, p2=815, l2=546.1)