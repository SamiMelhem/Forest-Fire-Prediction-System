import numpy as np
from shapely.geometry import Polygon
from joblib import load

# Load Lasso model
lasso_model = load("ml/lasso_model.joblib")

def resample_polygon(poly, n_points=50):
    coords = np.array(poly.exterior.coords)
    perimeter = sum(
        np.hypot(coords[i + 1, 0] - coords[i, 0], coords[i + 1, 1] - coords[i, 1])
        for i in range(len(coords) - 1)
    )
    spacing = perimeter / (n_points - 1)

    resampled = []
    segment_start = 0.0
    current_segment = 0

    for i in range(n_points):
        target_dist = i * spacing
        while True:
            p1 = coords[current_segment]
            p2 = coords[current_segment + 1]
            seg_len = np.hypot(p2[0] - p1[0], p2[1] - p1[1])

            if segment_start + seg_len >= target_dist or current_segment == len(coords) - 2:
                ratio = (target_dist - segment_start) / seg_len if seg_len else 0
                lon = p1[0] + ratio * (p2[0] - p1[0])
                lat = p1[1] + ratio * (p2[1] - p1[1])
                resampled.append([lon, lat])
                break
            else:
                segment_start += seg_len
                current_segment += 1

    return np.array(resampled).flatten()


def predict_polygon(temp, wind_speed, wind_direction, coordinates, n_points=50):
    try:
        if coordinates is None:
            raise ValueError("Input coordinates are None. Please provide a valid list of coordinates.")

        # 1) Validate and convert the input coordinates to a Shapely polygon
        if not isinstance(coordinates, list):
            raise TypeError("Expected coordinates to be a list of lists.")
        if not all(isinstance(coord, list) and len(coord) == 2 for coord in coordinates):
            raise ValueError("Each coordinate should be a list of two numbers [x, y].")

        current_poly = Polygon(coordinates)

        # 3) Resample polygon
        resampled_current = resample_polygon(current_poly, n_points=n_points)

        # 4) Prepare features for Lasso
        X_new = np.concatenate(([wind_direction, temp, wind_speed], resampled_current)).reshape(1, -1)

        # 5) Predict next-day polygon
        y_pred_lasso = lasso_model.predict(X_new)
        lasso_coords = y_pred_lasso[0].reshape(-1, 2)
        lasso_poly = Polygon(lasso_coords)

        # Return the predicted polygon as a list of [x, y] lists
        return [list(coord) for coord in lasso_poly.exterior.coords]

    except Exception as e:
        print(f"An error occurred: {e}")
        return None