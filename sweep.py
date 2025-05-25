import math
import pandas as pd


df = pd.read_excel('cleaned_locations.xlsx')
client_coords = [(row['Latitude'], row['Longitude']) for _, row in df.iterrows()]
depot = (56.91736, 23.98759)

# Lenķa rēķināšana katram klientam no noliktavas
angles = []
for idx, (lat, lon) in enumerate(client_coords, start=1):
    dy = lat - depot[0]
    dx = lon - depot[1]
    angle = math.degrees(math.atan2(dy, dx))
    if angle < 0:
        angle += 360 
    angles.append((angle, idx))
# Kartot lenķus pēc secībai (no 0 līdz 360)
angles.sort(key=lambda x: x[0])

# Dalīt visu lenķu sarakstu uz klasteriem pēc ietilpības
vehicle_capacity = 856.0
package_weight_per_client = 80.0
routes = []
current_route = []
current_load = 0.0

for angle, client in angles:
    if current_load + package_weight_per_client <= vehicle_capacity:
        # Pievienot klientu tekošā maršrūtā
        current_route.append(client)
        current_load += package_weight_per_client
    else:
        # Kad ietilpība beidzās - saglābat maršrūtu un sākt jaunu
        routes.append(current_route)
        current_route = [client]
        current_load = package_weight_per_client
# Pievinot jaunu maršrūtu, ja tas nav tukšs
if current_route:
    routes.append(current_route)

for idx, route in enumerate(routes, start=1):
    route_points = ['DC'] + [f'{c}' for c in route] + ['DC']
    print(f"Route {idx}: {' - '.join(route_points)}")
