import math
import tkinter as tk
from tkinter import Label, Entry, Button
import customtkinter as ctk

# Constants for the 1976 U.S. Standard Atmosphere model
R_E = 6371000  # Earth's radius (m)
T_0 = 288.15  # Standard temperature at sea level (K)
P_0 = 101325  # Standard pressure at sea level (Pa)
a = -0.0065  # Temperature lapse rate in the troposphere (K/m)
g = 9.80665  # Acceleration due to gravity (m/s²)
R = 287.05  # Gas constant for dry air (J/(kg·K))
gamma = 1.4  # Ratio of specific heats for air (dimensionless)
mu_0 = 1.716e-5  # Dynamic viscosity at sea level (kg/(m·s))
C = 110.4  # Sutherland's constant (K)

# Additional constants for the stratosphere (11-20 km)
h_11 = 11000  # Geopotential altitude at the top of the troposphere (m)
T_11 = 216.65  # Temperature at the top of the troposphere (K)
R_T_11 = R * T_11  # Precomputed value for convenience
P_11 = 22632.1  # Pressure at the top of the troposphere (Pa)


def standard_atmosphere(h):
    """
    Computes atmospheric properties at a given geopotential altitude (h) using the 1976 U.S. Standard Atmosphere model.

    Parameters:
    - h: Geopotential altitude (m)

    Returns:
    - Dictionary containing atmospheric properties:
      - 'Temperature': Temperature at the given altitude (K)
      - 'Pressure': Pressure at the given altitude (Pa)
      - 'Density': Density of air at the given altitude (kg/m³)
      - 'Speed of Sound': Speed of sound at the given altitude (m/s)
      - 'Dynamic Viscosity': Dynamic viscosity of air at the given altitude (kg/(m·s))
    """
    H_G = R_E * h / (R_E + h)  # Geopotential altitude calculation
    T_Hg = None  # Initialize T_Hg to None

    if 0 < H_G < h_11:
        # Troposphere calculation (0-11 km)
        T_Hg = T_0 + a * H_G  # Temperature calculation
        P_Hg = P_0 * (T_Hg / T_0) ** ((-g) / (a * R))  # Pressure calculation
        p_Hg = P_Hg / (R * T_Hg)  # Density calculation
        C_Hg = math.sqrt(gamma * R * T_Hg)  # Speed of sound calculation
        mu_h = mu_0 * (T_Hg ** 1.5) * (T_0 + C) / (T_Hg + C) / (T_0 ** 1.5)  # Dynamic viscosity calculation

    elif h_11 < H_G < 20000:
        # Stratosphere calculation (11-20 km)
        T_Hg = T_11
        P_Hg = P_11 * math.exp((-g) * (h - h_11) / R_T_11)  # Pressure calculation
        p_Hg = P_Hg / (R * T_11)  # Density calculation
        C_Hg = math.sqrt(gamma * R * T_11)  # Speed of sound calculation
        mu_h = mu_0 * (T_11 ** 1.5) * (T_0 + C) / (T_11 + C) / (T_0 ** 1.5)  # Dynamic viscosity calculation

    else:
        raise ValueError("Altitude is outside the valid range (0-20 km) for the 1976 U.S. Standard Atmosphere model.")

    # Return atmospheric properties as a dictionary
    return {
        "Temperature": T_Hg,
        "Pressure": P_Hg,
        "Density": p_Hg,
        "Speed of Sound": C_Hg,
        "Dynamic Viscosity": mu_h
    }


def calculate_standard_atmosphere():
    h = float(entry_altitude.get())
    atmosphere_props = standard_atmosphere(h)
    label_temperature.configure(text=f"Temperature: {atmosphere_props['Temperature']:.2f} K")
    label_pressure.configure(text=f"Pressure: {atmosphere_props['Pressure']:.2f} Pa")
    label_density.configure(text=f"Density: {atmosphere_props['Density']:.4f} kg/m³")
    label_speed_of_sound.configure(text=f"Speed of Sound: {atmosphere_props['Speed of Sound']:.2f} m/s")
    label_dynamic_viscosity.configure(text=f"Dynamic Viscosity: {atmosphere_props['Dynamic Viscosity']:.6f} kg/(m·s)")


# Create the main application window
# root = tk.Tk()
root = ctk.CTk()
root.geometry('420x400')
root.title('1976 Standard Atmosphere')
root.resizable(False, False)
font_tuple = ("Comic Sans MS", 16, "bold")

frame=ctk.CTkFrame(root,fg_color='#2E236C',border_color='#17153B',border_width=2,width=400)
frame.place(x=10,y=170)

frame_value=ctk.CTkFrame(root,fg_color='#C8ACD6',border_color='#17153B',border_width=2,width=400,height=80)
frame_value.place(x=10,y=60)

# Widgets
label_title = ctk.CTkLabel(root, text="1976 Standard Atmosphere", font=('Arial',30),text_color='#17153B')
label_title.place(x=10, y=10)

label_altitude = ctk.CTkLabel(frame_value, text="Altitude(m):", font=('Arial',20),text_color='#17153B')
label_altitude.place(x=80, y=10)

entry_altitude = ctk.CTkEntry(frame_value, width=150, font=('arial', 20), height=5)
entry_altitude.place(x=190, y=10)

button_calculate = ctk.CTkButton(frame_value, text='Calculate', font=('calibre', 13), corner_radius=32,
                                 command=calculate_standard_atmosphere, width=320)
button_calculate.place(x=50, y=45)

label_temperature = ctk.CTkLabel(frame, text="", font=('Arial',20),text_color='#6C946F')
label_temperature.place(x=10, y=10)

label_pressure = ctk.CTkLabel(frame, text="", font=('Arial',20),text_color='#6C946F')
label_pressure.place(x=10, y=40)

label_density = ctk.CTkLabel(frame, text="", font=('Arial',20),text_color='#6C946F')
label_density.place(x=10, y=70)

label_speed_of_sound = ctk.CTkLabel(frame, text="", font=('Arial',20),text_color='#6C946F')
label_speed_of_sound.place(x=10, y=100)

label_dynamic_viscosity = ctk.CTkLabel(frame, text="", font=('Arial',20),text_color='#6C946F')
label_dynamic_viscosity.place(x=10, y=130)

root.mainloop()
