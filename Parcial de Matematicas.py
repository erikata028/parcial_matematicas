import tkinter as tk
from tkinter import ttk
import heapq

# Grafo (puedes ampliarlo si deseas)
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1, 'E': 3},
    'E': {'D': 3, 'F': 2},
    'F': {'E': 2, 'G': 1},
    'G': {'F': 1}
}

# Posiciones de los nodos (ajustadas al canvas grande)
positions = {
    'A': (100, 200),
    'B': (200, 100),
    'C': (200, 300),
    'D': (300, 200),
    'E': (400, 200),
    'F': (500, 150),
    'G': (600, 100)
}

# Algoritmo Dijkstra
def dijkstra(graph, start, end):
    heap = [(0, start, [])]
    visited = set()
    while heap:
        cost, node, path = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)
        path = path + [node]
        if node == end:
            return path, cost
        for neighbor, weight in graph[node].items():
            if neighbor not in visited:
                heapq.heappush(heap, (cost + weight, neighbor, path))
    return None, float('inf')

# Dibuja el grafo y resalta la ruta
def draw_graph(path=[]):
    canvas.delete("all")
    # Aristas
    for node in graph:
        for neighbor, weight in graph[node].items():
            x1, y1 = positions[node]
            x2, y2 = positions[neighbor]
            canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
            mx, my = (x1 + x2) // 2, (y1 + y2) // 2
            canvas.create_text(mx, my, text=str(weight), fill="blue", font=("Arial", 14))

    # Ruta
    if path:
        for i in range(len(path) - 1):
            x1, y1 = positions[path[i]]
            x2, y2 = positions[path[i + 1]]
            canvas.create_line(x1, y1, x2, y2, fill="red", width=4)

    # Nodos
    for node, (x, y) in positions.items():
        canvas.create_oval(x - 25, y - 25, x + 25, y + 25, fill="lightblue", outline="black", width=2)
        canvas.create_text(x, y, text=node, font=("Arial", 18, "bold"))

# Muestra la ruta más corta
def mostrar_ruta():
    inicio = start_var.get()
    fin = end_var.get()
    if inicio and fin:
        ruta, costo = dijkstra(graph, inicio, fin)
        if ruta:
            result_label.config(text=f"Ruta: {' → '.join(ruta)} (Costo: {costo})")
            draw_graph(ruta)
        else:
            result_label.config(text="No se encontró ruta.")
    else:
        result_label.config(text="Selecciona nodos válidos.")

# Interfaz
root = tk.Tk()
root.title("Dijkstra con Canvas (Grafo Grande)")

ttk.Label(root, text="Inicio:").grid(row=0, column=0, padx=5, pady=5)
start_var = tk.StringVar()
ttk.Combobox(root, textvariable=start_var, values=list(graph.keys()), font=("Arial", 12)).grid(row=0, column=1)

ttk.Label(root, text="Fin:").grid(row=1, column=0, padx=5, pady=5)
end_var = tk.StringVar()
ttk.Combobox(root, textvariable=end_var, values=list(graph.keys()), font=("Arial", 12)).grid(row=1, column=1)

ttk.Button(root, text="Calcular Ruta", command=mostrar_ruta).grid(row=2, columnspan=2, pady=10)

result_label = ttk.Label(root, text="", font=("Arial", 14))
result_label.grid(row=3, columnspan=2, pady=5)

canvas = tk.Canvas(root, width=700, height=400, bg="white")
canvas.grid(row=4, columnspan=2, padx=10, pady=10)

draw_graph()

root.mainloop()