"""
Prototipo del modelo de dispersión de derrames de hidrocarburos.
Modelo: advección (arrastre por corriente/viento) + difusión (random walk).

Nada de esto usa FastAPI todavía -- es solo para validar que el
output (coordenadas por partícula por paso de tiempo) tiene sentido
antes de envolverlo en un endpoint.
"""

import random
import math

def simulate_spill(
    origin,          # (lat, lon) del punto de origen del derrame
    current,          # (u, v) velocidad de la corriente en m/s (este, norte)
    wind,              # (u, v) velocidad del viento en m/s (este, norte)
    hours,             # cuántas horas simular
    dt_hours=1,        # tamaño de cada paso de tiempo, en horas
    n_particles=50,    # cuántas partículas representan la mancha
    diffusion_m=200,   # magnitud del desplazamiento aleatorio por paso, en metros
    wind_factor=0.03,  # el viento no arrastra 1:1 -- ~3% de su velocidad se transfiere al agua
):
    """
    Devuelve una lista de snapshots, uno por paso de tiempo.
    Cada snapshot es una lista de (lat, lon), una por partícula.
    """
    lat0, lon0 = origin
    u_current, v_current = current
    u_wind, v_wind = wind

    # velocidad total = corriente + una fracción del viento
    u_total = u_current + wind_factor * u_wind  # m/s hacia el este
    v_total = v_current + wind_factor * v_wind  # m/s hacia el norte

    # todas las partículas arrancan en el mismo punto
    particles = [(lat0, lon0) for _ in range(n_particles)]

    dt_seconds = dt_hours * 3600
    n_steps = int(hours / dt_hours)

    # conversión aproximada metros -> grados (válida para distancias chicas)
    METERS_PER_DEG_LAT = 111_320
    meters_per_deg_lon = 111_320 * math.cos(math.radians(lat0))

    snapshots = [list(particles)]

    for _ in range(n_steps):
        new_particles = []
        for (lat, lon) in particles:
            # --- advección: desplazamiento por corriente + viento ---
            dx_m = u_total * dt_seconds
            dy_m = v_total * dt_seconds

            # --- difusión: paso aleatorio, distinto para cada partícula ---
            dx_m += random.uniform(-diffusion_m, diffusion_m)
            dy_m += random.uniform(-diffusion_m, diffusion_m)

            new_lat = lat + dy_m / METERS_PER_DEG_LAT
            new_lon = lon + dx_m / meters_per_deg_lon
            new_particles.append((new_lat, new_lon))

        particles = new_particles
        snapshots.append(list(particles))

    return snapshots


if __name__ == "__main__":
    # Ejemplo: derrame frente a la costa de Campeche
    resultado = simulate_spill(
        origin=(19.85, -90.55),
        current=(0.3, -0.1),   # 0.3 m/s hacia el este, 0.1 m/s hacia el sur
        wind=(2.0, 1.0),
        hours=12,
        dt_hours=1,
        n_particles=20,
    )

    for hora, snapshot in enumerate(resultado):
        lat_prom = sum(p[0] for p in snapshot) / len(snapshot)
        lon_prom = sum(p[1] for p in snapshot) / len(snapshot)
        print(f"hora {hora:2d} -> centro de la mancha: ({lat_prom:.5f}, {lon_prom:.5f})")
