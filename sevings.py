import math
import pandas as pd


df = pd.read_excel('cleaned_locations.xlsx')
client_coords = []
for _, row in df.iterrows():
    lat = row['Latitude']
    lon = row['Longitude']
    client_coords.append((lat, lon))
depot = (56.91736, 23.98759)
# Apvienot noliktavu un klientus vienā koordinātu sarakstā
coords = [depot] + client_coords
n_clients = len(client_coords)       # klienta skaits    
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
dist_matrix = [[0.0]*n_points for _ in range(n_points)]
for i in range(n_points):
    lat_i, lon_i = coords[i]
    for j in range(n_points):
        if i == j:
            dist_matrix[i][j] = 0.0
        else:
            lat_j, lon_j = coords[j]
            dist_matrix[i][j] = haversine_distance(lat_i, lon_i, lat_j, lon_j)

# Izveidot atsevišķu maršrutu katram klientam (maršruts i: Noliktava -> i -> Noliktava)
routes = [[i] for i in range(1, n_points)]            # maršrutu saraksts (neskaitot noliktavu, tikai klientus)
route_load = {i: package_weight_per_client for i in range(1, n_points)}  # katra maršruta ielāde

# Aprēķināt “ietaupījumu” sarakstu katram klientu pārim (i, j)
savings_list = []
for i in range(1, n_points):
    for j in range(i+1, n_points):
        saving = dist_matrix[0][i] + dist_matrix[0][j] - dist_matrix[i][j]
        savings_list.append((saving, i, j))
# Ietaupījumu sakārtošana dilstošā secībā (lielie ietaupījumi ir pirmie)
savings_list.sort(reverse=True, key=lambda x: x[0])

# Informācijas saglabāšana par to, kuram maršrutam pieder katrs klients.
route_index_of = {i: i-1 for i in range(1, n_points)}  # sākotnēji klients i maršrutā ar indeksu i-1

# Veikt maršrutu apvienošanu, izmantojot ietaupījumu algoritmu
for saving, i, j in savings_list:
    # Noskaidrosim to maršrutu indeksus, kuros atrodas i un j
    if i not in route_index_of or j not in route_index_of:
        continue  # ja kāds jau ir apvienots un dati ir novecojuši
    route_i_idx = route_index_of[i]
    route_j_idx = route_index_of[j]
    if route_i_idx == route_j_idx:
        continue  # jau vienā maršrutā
    # Maršruti, kuros atrodas i un j
    route_i = routes[route_i_idx]
    route_j = routes[route_j_idx]
    # Pirms apvienošanas pārbaudīt nosacījumu “i un j jābūt galējiem maršrutiem”
    # (i ir viena maršruta beigās, bet j - cita maršruta sākumā vai otrādi)
    if (route_i[-1] == i and route_j[0] == j) or (route_i[0] == i and route_j[-1] == j):
        # Ietilpības pārbaude
        if route_load.get(i, 0) + route_load.get(j, 0) <= vehicle_capacity:
            # Apvienot maršrutus route_i un route_j
            new_route = []
            # Izlemt, kā apvienot: ja i ir pēdējais route_i un j ir pirmais route_j
            if route_i[-1] == i and route_j[0] == j:
                new_route = route_i + route_j
            elif route_i[0] == i and route_j[-1] == j:
                # ja i ir pirmais un j ir pēdējais, apgriezt route_i un pievienot route_j
                new_route = route_i[::-1] + route_j
            elif route_i[-1] == i and route_j[-1] == j:
                # ja abi ir pēdējie, apgriezt route_j tā, lai j būtu pirmais
                new_route = route_i + route_j[::-1]
            elif route_i[0] == i and route_j[0] == j:
                # ja abi ir pirmie, apgriezt route_i tā, lai i būtu pēdējais, un pievienot route_j
                new_route = route_i[::-1] + route_j
            else:
                continue  # ja i vai j nav galēji, izlaidīt (nesavienot)
            # Jauna maršruta ietilpības atjaunināšana
            new_load = route_load.get(i, 0) + route_load.get(j, 0)
            # Izveidot jaunu maršruta ierakstu
            routes.append(new_route)
            new_idx = len(routes) - 1
            # Atzīmēt visus klientus no apvienotā maršruta kā piederīgus jaunajam maršrutam
            for cust in new_route:
                route_index_of[cust] = new_idx
                # atjaunot ietilpību glabātuvi katram jaunā maršruta klientam
                route_load[cust] = new_load
            # “Dzēst” vecos maršrutus (atzīmēt tos kā neaktīvus)
            routes[route_i_idx] = []
            routes[route_j_idx] = []
# Tukšo maršrutu, kas palikuši pēc apvienošanas, noņemšana
final_routes = [route for route in routes if route]


for idx, route in enumerate(final_routes, start=1):
    route_points = ['DC'] + [f'{cust}' for cust in route] + ['DC']
    print(f"Route {idx}: {' - '.join(route_points)}")
