import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider

# Grid resolution
W, H = 150, 150
x = np.linspace(-1, 1, W)
y = np.linspace(-1, 1, H)
X, Y = np.meshgrid(x, y)

# Wave frequency
omega = 2 * np.pi * 2

# Default parameters
default_slits = 2
default_spacing = 0.2
default_lambda = 0.05

# Safe colormap list (no dynamic creation)
colormaps = ['cool', 'winter', 'viridis', 'plasma', 'hot', 'spring', 'autumn']

# Set up plot
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.35)
initial = np.zeros((H, W))
img = ax.imshow(initial, extent=(-1, 1, -1, 1), cmap='viridis', vmin=-1.5, vmax=1.5)
ax.set_title("N-Slit Interference")

# Sliders
ax1 = plt.axes([0.1, 0.25, 0.8, 0.03])
ax2 = plt.axes([0.1, 0.2, 0.8, 0.03])
ax3 = plt.axes([0.1, 0.15, 0.8, 0.03])
s_slits = Slider(ax1, 'Slits', 1, 10, valinit=default_slits, valstep=1)
s_spacing = Slider(ax2, 'Spacing', 0.05, 0.5, valinit=default_spacing)
s_lambda = Slider(ax3, 'Wavelength', 0.01, 0.2, valinit=default_lambda)

# Wave calculator
def wave_pattern(n, spacing, k, t):
    field = np.zeros_like(X)
    offset = -(n - 1) * spacing / 2
    for i in range(n):
        y0 = offset + i * spacing
        R = np.sqrt((X + 1.1)**2 + (Y - y0)**2)
        field += np.sin(k * R - omega * t) / (R + 0.1)
    return np.clip(field, -1.5, 1.5)

# Animation update
def update(frame):
    t = frame * 0.1
    n = int(s_slits.val)
    spacing = s_spacing.val
    lam = s_lambda.val
    k = 2 * np.pi / lam

    Z = wave_pattern(n, spacing, k, t)
    img.set_data(Z)

    # Change colormap based on wavelength
    index = int(np.interp(lam, [0.01, 0.2], [0, len(colormaps)-1]))
    img.set_cmap(colormaps[index])

    return img,

# Animation (no blit)
ani = animation.FuncAnimation(fig, update, interval=30, blit=False)
plt.show()
