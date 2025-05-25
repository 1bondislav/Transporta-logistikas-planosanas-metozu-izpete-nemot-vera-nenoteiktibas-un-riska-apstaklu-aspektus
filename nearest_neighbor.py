import math
import pandas as pd


df = pd.read_excel('cleaned_locations.xlsx')
client_coords = []
for _, row in df.iterrows():
    lat = row['Latitude']   
    lon = row['Longitude']    
    client_coords.append((lat, lon))
warehouse = (56.91736, 23.98759)
# Apvienot noliktavu un klientus vienā koordinātu sarakstā
coords = [warehouse] + client_coords

n_clients = len(client_coords)        # klienta skaits
vehicle_capacity = 856.0             # transporta ietilpība
package_weight_per_client = 80.0     

# Attāluma apreķināšana starp punktiem ar Haversina formulu (2.1)
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Matricas izveidošāna (attālums starp punktiem)
n_points = n_clients + 1  
dist_matrix = [[0.0] * n_points for _ in range(n_points)]
for i in range(n_points):
    lat_i, lon_i = coords[i]
    for j in range(n_points):
        if i == j:
            dist_matrix[i][j] = 0.0
        else:
            lat_j, lon_j = coords[j]
            dist_matrix[i][j] = haversine_distance(lat_i, lon_i, lat_j, lon_j)

# Maršrutu veidošana
routes_nn = []                     # maršruta saraksts
visited = [False] * n_points       # apmeklējuma karogs katram klientam
visited[0] = True                  # noliktava jau 'visited'
remaining = n_clients              # brīvie klienti
while remaining > 0:
    current_route = [0]   
    load = 0.0            
    current_node = 0      
    while True:
        nearest_node = None
        nearest_dist = float('inf')
        # tuvāko neapmeklēto klientu no pašreizējā punkta meklēšana
        for j in range(1, n_points):    
            if not visited[j]:
                # parbaudam attālumu un transporta ietilpību 
                if dist_matrix[current_node][j] < nearest_dist and load + package_weight_per_client <= vehicle_capacity:
                    nearest_node = j
                    nearest_dist = dist_matrix[current_node][j]
        if nearest_node is None:
            # vai nu visi klienti ir apmeklēti, vai arī nav iespējams pievienot nākamo klientu (pēc transporta ietilpības).
            break
        # Pievienojam tuvāko klientu maršrutā
        visited[nearest_node] = True
        remaining -= 1
        current_route.append(nearest_node)
        load += package_weight_per_client
        current_node = nearest_node
        # Ja nav ietilpības transportā beidzam maršrutu
        if load + package_weight_per_client > vehicle_capacity:
            break
    # Atgriezties uz noliktavu
    current_route.append(0)
    routes_nn.append(current_route)

# Saņemto maršrutu izvade (klientu indeksi)
for idx, route in enumerate(routes_nn, start=1):
    route_points = ['DC' if i == 0 else f'{i}' for i in route]
    print(f"Route {idx}: {' - '.join(route_points)}")
