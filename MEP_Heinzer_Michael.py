import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button

# Funktion zur Berechnung und Darstellung
def berechnen():
    # Eingabewerte auslesen
    L1 = float(entry_L1.get())
    L2 = float(entry_L2.get())
    L3 = float(entry_L3.get())
    EI = float(entry_EI.get())
    w = float(entry_w.get())
    P_position = float(entry_P_position.get())
    P_force = float(entry_P_force.get())
    P_angle = float(entry_P_angle.get())

    # Umrechnung des Winkels in rad
    P_angle_rad = np.radians(P_angle)

    # Horizontale und vertikale Komponenten der Einzelkraft
    P_horizontal = P_force * np.cos(P_angle_rad)
    P_vertical = P_force * np.sin(P_angle_rad)

    # Diskretisierung des Balkens
    x = np.linspace(0, L1 + L2 + L3, 500)

    # Berechnung von Momenten, Querkräften und Verformungen
    moment = np.zeros_like(x)
    shear_force = np.zeros_like(x)
    deflection = np.zeros_like(x)

    # Gleichverteilte Last
    shear_force += np.piecewise(
        x,
        [x <= L1, (x > L1) & (x <= L1 + L2), x > L1 + L2],
        [
            lambda x: -w * x,
            lambda x: -w * L1 + w * (x - L1),
            lambda x: -w * (L1 + L2)
        ]
    )

    moment += np.piecewise(
        x,
        [x <= L1, (x > L1) & (x <= L1 + L2), x > L1 + L2],
        [
            lambda x: -w * x**2 / 2,
            lambda x: -w * L1**2 / 2 + w * (x - L1) * L1 - w * (x - L1)**2 / 2,
            lambda x: -w * (L1 + L2)**2 / 2 + w * L1 * (L1 + L2) - w * (x - L1 - L2)**2 / 2
        ]
    )

    # Einzellast berücksichtigen
    for i in range(len(x)):
        if x[i] >= P_position:
            shear_force[i] -= P_vertical
            moment[i] -= P_vertical * (x[i] - P_position)

    # Verformung berechnen
    for i in range(1, len(x)):
        deflection[i] = deflection[i - 1] - moment[i] * (x[i] - x[i - 1]) / EI

    # Werte an spezifischen Punkten
    x_points = [0, L1, L1 + L2, L1 + L2 + L3]
    moment_points = [moment[0], moment[np.argmin(abs(x - L1))], moment[np.argmin(abs(x - (L1 + L2)))], moment[-1]]
    shear_points = [shear_force[0], shear_force[np.argmin(abs(x - L1))], shear_force[np.argmin(abs(x - (L1 + L2)))], shear_force[-1]]
    deflection_points = [deflection[0], deflection[np.argmin(abs(x - L1))], deflection[np.argmin(abs(x - (L1 + L2)))], deflection[-1]]

    # Grafische Darstellung
    fig, axes = plt.subplots(3, 2, figsize=(12, 10))
    fig.suptitle("Balken mit Kragarmen und Einzellast (Grafisch)", fontsize=16, fontweight='bold')

    # Momente M [kNm]
    axes[0, 0].plot(x, moment, 'r-', label='M [kNm]')
    axes[0, 0].scatter(x_points, moment_points, color='red')
    for xi, mi in zip(x_points, moment_points):
        axes[0, 0].text(xi, mi, f"{mi:.1f} kNm", fontsize=9)
    axes[0, 0].set_title("M [kNm]")
    axes[0, 0].grid(True)

    # Normalkraft N [kN] (hier Null)
    axes[0, 1].plot(x, np.zeros_like(x), 'k-', label='N [kN]')
    axes[0, 1].set_title("N [kN]")
    axes[0, 1].grid(True)

    # Querkräfte V [kN]
    axes[1, 0].plot(x, shear_force, 'g-', label='V [kN]')
    axes[1, 0].scatter(x_points, shear_points, color='red')
    for xi, vi in zip(x_points, shear_points):
        axes[1, 0].text(xi, vi, f"{vi:.1f} kN", fontsize=9)
    axes[1, 0].set_title("V [kN]")
    axes[1, 0].grid(True)

    # Balkenskizze
    axes[1, 1].plot(x, np.zeros_like(x), 'k-')
    axes[1, 1].scatter(x_points, np.zeros_like(x_points), color='black', marker='o')
    axes[1, 1].set_title("Balken")
    axes[1, 1].axis('off')

    # Verformung u [mm]
    axes[2, 0].plot(x, deflection * 1e3, 'b-', label='u [mm]')
    axes[2, 0].scatter(x_points, np.array(deflection_points) * 1e3, color='red')
    for xi, di in zip(x_points, deflection_points):
        axes[2, 0].text(xi, di * 1e3, f"{di * 1e3:.1f} mm", fontsize=9)
    axes[2, 0].set_title("u [mm]")
    axes[2, 0].grid(True)

    # Leeres Feld
    axes[2, 1].axis('off')

    # Layout anpassen
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

# Tkinter GUI
root = Tk()
root.title("Balkenanalyse mit Kragarmen und Einzellast")

# Labels und Eingabefelder
Label(root, text="L₁ (Kragarmlänge 1 in m):").grid(row=0, column=0, padx=5, pady=5)
entry_L1 = Entry(root)
entry_L1.grid(row=0, column=1, padx=5, pady=5)
entry_L1.insert(0, "5")

Label(root, text="L₂ (Hauptbalkenlänge in m):").grid(row=1, column=0, padx=5, pady=5)
entry_L2 = Entry(root)
entry_L2.grid(row=1, column=1, padx=5, pady=5)
entry_L2.insert(0, "10")

Label(root, text="L₃ (Kragarmlänge 2 in m):").grid(row=2, column=0, padx=5, pady=5)
entry_L3 = Entry(root)
entry_L3.grid(row=2, column=1, padx=5, pady=5)
entry_L3.insert(0, "5")

Label(root, text="EI (Biegesteifigkeit in kNm²):").grid(row=3, column=0, padx=5, pady=5)
entry_EI = Entry(root)
entry_EI.grid(row=3, column=1, padx=5, pady=5)
entry_EI.insert(0, "25000")

Label(root, text="w (Gleichverteilte Last in kN/m):").grid(row=4, column=0, padx=5, pady=5)
entry_w = Entry(root)
entry_w.grid(row=4, column=1, padx=5, pady=5)
entry_w.insert(0, "5")

Label(root, text="P (Position der Einzellast in m):").grid(row=5, column=0, padx=5, pady=5)
entry_P_position = Entry(root)
entry_P_position.grid(row=5, column=1, padx=5, pady=5)
entry_P_position.insert(0, "7.5")

Label(root, text="F (Kraft der Einzellast in kN):").grid(row=6, column=0, padx=5, pady=5)
entry_P_force = Entry(root)
entry_P_force.grid(row=6, column=1, padx=5, pady=5)
entry_P_force.insert(0, "10")

Label(root, text="\u03B8 (Einwirkungswinkel der Einzellast in Grad):").grid(row=7, column=0, padx=5, pady=5)
entry_P_angle = Entry(root)
entry_P_angle.grid(row=7, column=1, padx=5, pady=5)
entry_P_angle.insert(0, "90")

# Berechnen-Button
Button(root, text="Berechnen", command=berechnen).grid(row=8, column=0, columnspan=2, pady=10)

# GUI starten
root.mainloop()
