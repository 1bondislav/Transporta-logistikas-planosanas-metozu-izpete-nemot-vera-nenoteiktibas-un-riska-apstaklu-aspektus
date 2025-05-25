import math
import pandas as pd


df = pd.read_excel('cleaned_locations.xlsx')
client_coords = [(row['Latitude'], row['Longitude']) for _, row in df.iterrows()]
depot = (56.91736, 23.98759)
# Apvienot noliktavu un klientus vienā koordinātu sarakstā
coords = [depot] + client_coords
n_clients = len(client_coords)        # klienta skaits   
vehicle_capacity = 856.0              # transporta ietilpība
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
dist_matrix = [[0.0]*n_points for _ in range(n_points)]
for i in range(n_points):
    lat_i, lon_i = coords[i]
    for j in range(n_points):
        if i == j:
            dist_matrix[i][j] = 0.0
        else:
            lat_j, lon_j = coords[j]
            dist_matrix[i][j] = haversine_distance(lat_i, lon_i, lat_j, lon_j)


# Atrast vistālāko klientu
farthest_client = None
max_dist = -1
for client in range(1, n_points):
    d = dist_matrix[0][client]
    if d > max_dist:
        max_dist = d
        farthest_client = client

# Starta maršrūts ar vistālāko klientu
routes = [[farthest_client]]
route_loads = [package_weight_per_client]
used_vehicles = 1

# Saraksts ar brīviem klientiem
unrouted_clients = set(range(1, n_points))
unrouted_clients.remove(farthest_client)

# Pievinojam klientus pa vienam
while unrouted_clients:
    best_increase = float('inf')
    best_route_idx = None
    best_position = None
    best_client = None

    # Novērtēt katru atlikušo klientu un katru ievietošanas vietu
    for client in list(unrouted_clients):
        # Mēģināt ievietot šo klientu katrā esošajā maršrutā optimālā vietā.
        for r_idx, route in enumerate(routes):
            # Ietilpības parbaude 
            if route_loads[r_idx] + package_weight_per_client > vehicle_capacity:
                continue
            # Iespējamās klienta ievietošanas pozīcijas maršrutā (starp jebkuriem diviem secīgiem punktiem, ieskaitot sākuma un beigu punktu)
            # Pārveidosim maršrutu šādi: 0 -> A1 -> A2 -> ... -> Ak -> 0 (kur 0 ir noliktava, Ai ir klienti).
            # Maršrutu saglabājam kā sarakstu [A1, A2, ..., Ak] (klienti bez noliktavas).
            # Pārbaudīsim visas X (klienta) ievietošanas pozīcijas šajā secībā.
            # Pozīcija p=0 nozīmē, ka X ievieto sākumā (starp noliktavu un pirmo klientu),
            # p=len(maršruts) nozīmē X ievietošanu beigās (pirms atgriešanās noliktavā),
            # 0 < p < len(maršruts) nozīmē ievietot starp maršrutu[p-1] un maršrutu[p].
            for p in range(len(route) + 1):
                # nosaka iepriekšējo un nākamo mezglu attiecībā pret ievietošanas pozīciju
                if p == 0:
                    prev_node = 0  # noliktava pirms pirmājā klienta
                    next_node = route[0]
                elif p == len(route):
                    prev_node = route[-1]
                    next_node = 0   # noliktava pēc pēdējā klienta
                else:
                    prev_node = route[p-1]
                    next_node = route[p]
                # saskaitīt attāluma palielinājumu, ievietojot klientu starp prev_node un next_node.
                extra_dist = (dist_matrix[prev_node][client] 
                              + dist_matrix[client][next_node] 
                              - dist_matrix[prev_node][next_node])
                # ja tas ir mazākais pieaugums no visiem aplūkotajiem, saglabāt to
                if extra_dist < best_increase:
                    best_increase = extra_dist
                    best_route_idx = r_idx
                    best_position = p
                    best_client = client
        # Parbadām arī iespēju sākt jaunu maršrutu ar šo klientu, ja vēl ir pieejamas automašīnas.
        if used_vehicles < 9:
            new_route_increase = 2 * dist_matrix[0][client]  # ceļš noliktava -> klients -> noliktava
            if new_route_increase < best_increase:
                best_increase = new_route_increase
                best_route_idx = None    # signalizē, ka jauns maršruts ir izdevīgāks
                best_position = None
                best_client = client
    # Pēc visu klientu un pozīciju pārbaudes pievienot labāko atrasto kandidātu.
    if best_route_idx is None:
        # Izveidot jaunu maršrutu ar best_client
        routes.append([best_client])
        route_loads.append(package_weight_per_client)
        used_vehicles += 1
    else:
        # Ievietot best_client esošajā best_route_idx maršrutā best_position
        routes[best_route_idx].insert(best_position, best_client)
        route_loads[best_route_idx] += package_weight_per_client
    # Noņemt šo klientu no brīvu klientu saraksta
    unrouted_clients.remove(best_client)


for idx, route in enumerate(routes, start=1):
    route_points = ['DC'] + [f'{c}' for c in route] + ['DC']
    print(f"Route {idx}: {' - '.join(route_points)}")
