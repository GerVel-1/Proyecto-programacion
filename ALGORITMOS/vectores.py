import numpy as np

class AnomalyDetector:
    def __init__(self, history_size=10, z_threshold=3.0):
        self.history_size = history_size
        self.z_threshold = z_threshold

    def evaluate_sensor(self, current_val, history, neighbor_vals):
        """
        Detecta: Stuck-at, Ruido Alto, Picos Falsos, NaN.
        """
        # 1. Manejo de NaN / Valores Faltantes
        if current_val is None or np.isnan(current_val):
            return False, "NaN_DETECTED"
        
        # 2. Detección de Valor Congelado (Stuck-at)
        if len(history) >= self.history_size:
            if len(set(history[-self.history_size:])) == 1 and history[-1] != 0:
                return False, "STUCK_AT_DETECTED"

        # 3. Detección de Picos Falsos y Ruido Alto (Z-Score Temporal)
        if len(history) >= 5:
            mean = np.mean(history)
            std = np.std(history) + 1e-5
            z_score = abs(current_val - mean) / std
            if z_score > self.z_threshold and current_val > 50: # Pico no físico
                return False, "SPURIOUS_SPIKE"

        # 4. Consistencia Espacial con Vecinos
        if neighbor_vals:
            valid_neighbors = [v for v in neighbor_vals if v is not None and not np.isnan(v)]
            if valid_neighbors:
                avg_neighbor = np.mean(valid_neighbors)
                if current_val > 3 * avg_neighbor + 10: # Desconexión severa con flujo aguas arriba
                    return False, "SPATIAL_INCONSISTENCY"

        return True, "HEALTHY"