import requests
import pandas as pd

# Cabezeras para el requests
headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
    "format": "json",
}

# Url para buscar el catalogo en cada slider atravez de una id
url_base = 'https://mfwkweb-api.clarovideo.net/services/content/list?quantity=50&order_way=ASC&order_id=50&level_id=GPS&from=0&filter_id={}&region=argentina&device_id=web&device_category=web&device_model=web&device_type=web&device_so=Chrome&format=json&device_manufacturer=generic&authpn=webclient&authpt=tfg1h3j4k6fd7&api_version=v5.92&region=argentina&HKS=d41gs2tf68bvu3fds02uhk9661'


url_deatail = 'https://mfwkweb-api.clarovideo.net/services/content/data?device_id=web&device_category=web&device_model=web&device_type=web&device_so=Chrome&format=json&device_manufacturer=generic&authpn=webclient&authpt=tfg1h3j4k6fd7&api_version=v5.92&region=argentina&HKS=d41gs2tf68bvu3fds02uhk9661&group_id={}'

# Lista de id de cada slider
links_ids = ['38973', '40503', '38527', '16088', '31815', '16151', '30128', '31130', '35732', '31530', '36662', '39994', '35091', '38468', '38572', '16152', '16090', '16091', '15622', '16154', '16114', '9463', '16111', '16099', '16118', '31451', '31254', '16115', '16117', '16096', '20322', '16121'
             ]

# Lista vacia a la cual agregar las series y peliculas del catalogo
product = []

# comienza el recorriendo cada una de las ids
for link in links_ids:
    # concate las url base con la id
    enlase = url_base.format(link)
    # respuesta del elemento que contiene las peliculas y series por paquete
    response = requests.get(enlase, headers=headers)
    # convierte la respuesta en un json
    data = response.json()
    # aisla la parte del json que contien infomacion sobre las peliculas y series
    movies = data["response"]["groups"]
    for movie in movies:
        # Mensaje en consola para desterminar que producto se esta cargando
        print("cargando {}".format(movie["title"]))
        # consulta a elemento "season_number" para determinar si se trata de una Película o una serie
        if movie["season_number"] is None:
            type_product = 'Película'
        else:
            type_product = 'Serie'
        # Llamada por medio de la id del producto para obtener informacion extra (Reparto y generos)
        unique_link = url_deatail.format(movie['id'])
        response_deatail = requests.get(unique_link, headers=headers)
        # convertimos la info extra en un  json
        detail_data = response_deatail.json()
        # aislamos la parte donde se encuentra la información deseada
        extra_data = detail_data["response"]["group"]["common"]["extendedcommon"]
        # creamos la lista de generos, en caso de no contar con este atributo se vuelve un atributo nula
        try:
            genres = []
            genres_list = extra_data["genres"]["genre"]
            for genre in genres_list:
                genres.append(genre['desc'])
        except:
            genres = None
        # creamos la lista de el reparto, en caso de no contar con este atributo se vuelve un atributo nula
        try:
            talents = extra_data["roles"]["role"]
        except:
            genres = None

        # Agrega a la lista products los elementos de la serie o pelicula
        product.append({'product': {
            'id': movie["id"],
            'title': movie["title"],
            'year': movie["year"],
            'descrition': movie["description"],
            'type': type_product,
            'genres': genres,
            'talents': talents,
        }})

# mensaje en consolo que notifica que la búsqueda terminó
print("cargado completo")

# creamos un archivo json con todo el catalogo con panda
df = pd.DataFrame(product)
df.to_json('catalogo.json')
