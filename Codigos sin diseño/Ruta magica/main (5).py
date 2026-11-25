import heapq

PUEBLOS = ("Izamal", "Valladolid", "Sisal", "Mani", "Espita", "Motul", "Tekax")


def crear_grafo_yucatan():
  """Crea un grafo ponderado y no dirigido como lista de adyacencia."""
  grafo = {pueblo: [] for pueblo in PUEBLOS}

  def conectar(origen, destino, km):
    # Grafo no dirigido: conexión en ambos sentidos
    grafo[origen].append((destino, km))
    grafo[destino].append((origen, km))

  conectar("Sisal", "Motul", 88)
  conectar("Motul", "Izamal", 32)
  conectar("Motul", "Espita", 122)
  conectar("Izamal", "Valladolid", 96)
  conectar("Izamal", "Mani", 89)
  conectar("Espita", "Valladolid", 45)
  conectar("Mani", "Tekax", 42)
  conectar("Valladolid", "Tekax", 175)
  conectar("Sisal", "Mani", 125)
  conectar("Izamal", "Espita", 105)

  return grafo


def dijkstra(grafo, inicio, fin):
  """Algoritmo de Dijkstra usando cola de prioridad (heapq)."""
  if inicio not in grafo or fin not in grafo:
    return None, float("inf")

  distancias = {nodo: float("inf") for nodo in grafo}
  distancias[inicio] = 0

  padres = {nodo: None for nodo in grafo}
  cola_prioridad = [(0, inicio)]

  while cola_prioridad:
    dist_actual, nodo_actual = heapq.heappop(cola_prioridad)

    if dist_actual > distancias[nodo_actual]:
      continue

    if nodo_actual == fin:
      break

    for vecino, peso in grafo[nodo_actual]:
      nueva_distancia = dist_actual + peso
      if nueva_distancia < distancias[vecino]:
        distancias[vecino] = nueva_distancia
        padres[vecino] = nodo_actual
        heapq.heappush(cola_prioridad, (nueva_distancia, vecino))

  if distancias[fin] == float("inf"):
    return None, float("inf")

  ruta = []
  actual = fin
  while actual is not None:
    ruta.append(actual)
    actual = padres[actual]
  ruta.reverse()

  return ruta, distancias[fin]


def obtener_peso_arista(grafo, nodo_a, nodo_b):
  for vecino, peso in grafo[nodo_a]:
    if vecino == nodo_b:
      return peso
  return 0


def main():
  grafo = crear_grafo_yucatan()
  pueblos = list(grafo)

  while True:
    print("\n" + "=" * 45)
    print("       RUTA MÁGICA")
    print("          YUCATÁN")
    print("  Camino más corto entre Pueblos Mágicos")
    print("=" * 45)
    print("Pueblos Mágicos disponibles:")

    for i, pueblo in enumerate(pueblos, start=1):
      print(f"{i}. {pueblo}")

    try:
      op_origen = int(
          input(f"\nSeleccione pueblo de ORIGEN (1-{len(pueblos)}): ")
      )
      if not (1 <= op_origen <= len(pueblos)):
        print("[!] Opción fuera de rango. Intente de nuevo.")
        continue
      origen = pueblos[op_origen - 1]
      print(f"-> Origen: {origen}")

      op_destino = int(
          input(f"\nSeleccione pueblo de DESTINO (1-{len(pueblos)}): ")
      )
      if not (1 <= op_destino <= len(pueblos)):
        print("[!] Opción fuera de rango. Intente de nuevo.")
        continue
      destino = pueblos[op_destino - 1]
      print(f"-> Destino: {destino}")

    except ValueError:
      print("[!] Por favor ingrese un número válido.")
      continue

    if origen == destino:
      print("\n[OK] Ya te encuentras en el destino.")
    else:
      print("\nAlgoritmo utilizado: Dijkstra")
      print("Calculando ruta más corta...")

      ruta, distancia_total = dijkstra(grafo, origen, destino)

      if ruta:
        if origen != destino:
          print("\n[OK] RUTA ENCONTRADA")
          for p_actual, p_siguiente in zip(ruta, ruta[1:]):
            km = obtener_peso_arista(grafo, p_actual, p_siguiente)
            print(f"  {p_actual} --({km} km)--> {p_siguiente}")

          print("\nRuta completa:")
          print("  " + " -> ".join(ruta))
          print(f"Distancia total: {distancia_total} km")
          print(f"Tramos: {len(ruta) - 1}")
      else:
        print("\n[X] No existe una ruta conectada entre esos pueblos.")

    while True:
      continuar = input("\n¿Desea consultar otra ruta? (S/N): ").strip().upper()
      if continuar in ("S", "N"):
        break
      print("[!] Responda únicamente S o N.")

    if continuar == "N":
      print("\n¡Gracias por usar Ruta Mágica! Buen viaje.")
      break


if __name__ == "__main__":
  main()