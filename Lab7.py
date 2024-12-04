import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import numpy as np
from itertools import combinations

class ComprehensiveVisualizationApp:
    def __init__(self, master):
        self.master = master
        master.title("Comprehensive Visualization and Analysis App")
        master.geometry("1400x900")

        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill='both')

        # Create tabs
        self.vertex_cover_tab = ttk.Frame(self.notebook)
        self.reordering_tab = ttk.Frame(self.notebook)
        self.advanced_vertex_cover_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.vertex_cover_tab, text="Vertex Cover")
        self.notebook.add(self.reordering_tab, text="Reordering")
        self.notebook.add(self.advanced_vertex_cover_tab, text="Advanced Vertex Cover")

        # Setup Tabs
        self.setup_vertex_cover_tab()
        self.setup_reordering_tab()
        self.setup_advanced_vertex_cover_tab()

    def setup_vertex_cover_tab(self):
        # Input Frame
        input_frame = tk.Frame(self.vertex_cover_tab)
        input_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Nodes Input
        tk.Label(input_frame, text="Nodes:").pack(side=tk.LEFT)
        self.nodes_entry = tk.Entry(input_frame, width=30)
        self.nodes_entry.pack(side=tk.LEFT, padx=5)
        self.nodes_entry.insert(0, "P1,P2,P3,P4,P5")

        # Edges Input
        tk.Label(input_frame, text="Edges:").pack(side=tk.LEFT)
        self.edges_entry = tk.Entry(input_frame, width=30)
        self.edges_entry.pack(side=tk.LEFT, padx=5)
        self.edges_entry.insert(0, "P1-P2,P1-P3,P2-P4,P3-P5,P4-P5")

        # Vertex Cover Methods Frame
        methods_frame = tk.Frame(self.vertex_cover_tab)
        methods_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Buttons for Different Methods
        tk.Button(methods_frame, text="Brute Force", 
                  command=self.brute_force_vertex_cover).pack(side=tk.LEFT, padx=5)
        tk.Button(methods_frame, text="Greedy", 
                  command=self.greedy_vertex_cover).pack(side=tk.LEFT, padx=5)
        tk.Button(methods_frame, text="Animated Cover", 
                  command=self.animated_vertex_cover).pack(side=tk.LEFT, padx=5)

        # Result Label
        self.vertex_cover_result = tk.Label(self.vertex_cover_tab, text="")
        self.vertex_cover_result.pack(side=tk.TOP, padx=10, pady=10)

        # Matplotlib Figure for Graph Visualization
        self.vc_fig, self.vc_ax = plt.subplots(figsize=(10, 7))
        self.vc_canvas = FigureCanvasTkAgg(self.vc_fig, master=self.vertex_cover_tab)
        self.vc_canvas_widget = self.vc_canvas.get_tk_widget()
        self.vc_canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def create_graph(self):
        # Parse nodes and edges
        nodes = [n.strip() for n in self.nodes_entry.get().split(',')]
        edges = [tuple(e.strip().split('-')) for e in self.edges_entry.get().split(',')]
        
        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        return G

    def brute_force_vertex_cover(self):
        G = self.create_graph()
        nodes = list(G.nodes())
        
        def is_vertex_cover(subset):
            return all(u in subset or v in subset for u, v in G.edges())
        
        min_cover = None
        for k in range(1, len(nodes) + 1):
            for subset in combinations(nodes, k):
                if is_vertex_cover(subset):
                    min_cover = set(subset)
                    break
            if min_cover:
                break
        
        if min_cover:
            self.visualize_vertex_cover(G, min_cover, "Brute Force")
        else:
            messagebox.showinfo("Result", "No vertex cover found")

    def greedy_vertex_cover(self):
        G = self.create_graph().copy()
        cover = set()
        edges = set(G.edges())
        
        while edges:
            degrees = {node: len(list(G.neighbors(node))) for node in G.nodes}
            max_degree_node = max(degrees, key=degrees.get)
            
            cover.add(max_degree_node)
            for neighbor in list(G.neighbors(max_degree_node)):
                edges.discard((max_degree_node, neighbor))
                edges.discard((neighbor, max_degree_node))
            
            G.remove_node(max_degree_node)
        
        self.visualize_vertex_cover(self.create_graph(), cover, "Greedy")

    def animated_vertex_cover(self):
        G = self.create_graph()
        pos = nx.spring_layout(G)
        edges = list(G.edges())
        
        covered_edges = []
        vertex_cover = []
        
        def update(frame):
            if frame < len(edges):
                edge = edges[frame]
                if edge[0] not in vertex_cover and edge[1] not in vertex_cover:
                    vertex_cover.append(edge[0])
                    
                covered_edges.append(edge)
            
            self.vc_ax.clear()
            nx.draw(G, pos, ax=self.vc_ax, with_labels=True, 
                    node_color="lightblue", edge_color="gray", 
                    node_size=1000, font_size=12)
            
            nx.draw_networkx_nodes(G, pos, ax=self.vc_ax, 
                                   nodelist=vertex_cover, 
                                   node_color="orange", node_size=1200)
            
            nx.draw_networkx_edges(G, pos, ax=self.vc_ax, 
                                   edgelist=covered_edges, edge_color="red")
            
            self.vc_ax.set_title(f"Step {frame + 1}: Vertex Cover: {vertex_cover}")
            self.vc_canvas.draw()
        
        # Animate
        ani = FuncAnimation(self.vc_fig, update, 
                            frames=len(edges), interval=1000, 
                            repeat=False, cache_frame_data=False)
        
        plt.tight_layout()
        self.vc_canvas.draw()

    def visualize_vertex_cover(self, G, cover, method):
        self.vc_ax.clear()
        pos = nx.spring_layout(G)
        
        nx.draw(G, pos, ax=self.vc_ax, with_labels=True, 
                node_color=['orange' if node in cover else 'lightblue' for node in G.nodes()])
        
        self.vc_ax.set_title(f"{method} Vertex Cover")
        self.vc_canvas.draw()
        self.vertex_cover_result.config(text=f"{method} Vertex Cover: {cover}")

    def setup_reordering_tab(self):
        # Reordering Frame
        input_frame = tk.Frame(self.reordering_tab)
        input_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Sequence Input
        tk.Label(input_frame, text="Enter Sequence:").pack(side=tk.LEFT)
        self.sequence_entry = tk.Entry(input_frame, width=50)
        self.sequence_entry.pack(side=tk.LEFT, padx=5)
        self.sequence_entry.insert(0, "7,2,5,3,8,1,4,6")

        # Sorting Method Buttons
        methods_frame = tk.Frame(self.reordering_tab)
        methods_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        tk.Button(methods_frame, text="Bar Visualization", 
                  command=self.bar_sort_visualization).pack(side=tk.LEFT, padx=5)
        tk.Button(methods_frame, text="Circular Visualization", 
                  command=self.circular_sort_visualization).pack(side=tk.LEFT, padx=5)
        tk.Button(methods_frame, text="Animated Bubble Sort", 
                  command=self.animated_bubble_sort).pack(side=tk.LEFT, padx=5)

        # Matplotlib Figure for Reordering Visualization
        self.reorder_fig, self.reorder_ax = plt.subplots(figsize=(10, 7))
        self.reorder_canvas = FigureCanvasTkAgg(self.reorder_fig, master=self.reordering_tab)
        self.reorder_canvas_widget = self.reorder_canvas.get_tk_widget()
        self.reorder_canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def bar_sort_visualization(self):
        realidad = [int(x) for x in self.sequence_entry.get().split(',')]
        deseo = sorted(realidad)
        
        self.reorder_ax.clear()
        self.reorder_ax.bar(range(len(realidad)), realidad, color='lightblue', label='Reality')
        self.reorder_ax.plot(range(len(deseo)), deseo, color='orange', marker='o', linestyle='-', label='Desired')
        
        self.reorder_ax.set_title("Sequence Transformation")
        self.reorder_ax.set_xlabel("Index")
        self.reorder_ax.set_ylabel("Value")
        self.reorder_ax.legend()
        
        self.reorder_canvas.draw()

    def circular_sort_visualization(self):
        realidad = [int(x) for x in self.sequence_entry.get().split(',')]
        deseo = sorted(realidad)
        
        n = len(realidad)
        angulos = np.linspace(0, 2 * np.pi, n, endpoint=False)
        
        self.reorder_ax.clear()
        self.reorder_ax.set_theta_direction(-1)
        self.reorder_ax.set_theta_offset(np.pi / 2)
        
        self.reorder_ax.scatter(angulos, deseo, color="orange", label="Desired", s=100)
        self.reorder_ax.scatter(angulos, realidad, color="blue", label="Current", s=100)
        
        for i in range(n):
            self.reorder_ax.plot([angulos[i], angulos[i]], 
                                  [realidad[i], deseo[i]], 
                                  color="gray", linestyle="--", alpha=0.5)
        
        self.reorder_ax.set_title("Circular Representation of Sequence")
        self.reorder_ax.legend(loc="upper right")
        self.reorder_canvas.draw()

    def animated_bubble_sort(self):
        realidad = [int(x) for x in self.sequence_entry.get().split(',')]
        
        n = len(realidad)
        
        def update(frame):
            nonlocal realidad
            
            swapped = False
            for i in range(n-1):
                if realidad[i] > realidad[i+1]:
                    realidad[i], realidad[i+1] = realidad[i+1], realidad[i]
                    swapped = True

            # Visualization (only if swapped for efficiency)
            if swapped:
                self.reorder_ax.clear()
                self.reorder_ax.bar(range(len(realidad)), realidad, color='lightblue', label='Current')
                self.reorder_ax.set_title(f"Step {frame + 1}: Bubble Sort")
                self.reorder_ax.set_xlabel("Index")
                self.reorder_ax.set_ylabel("Value")
                self.reorder_ax.legend()
                self.reorder_canvas.draw()
            
            return swapped # Stop animation when sorted

        # Animate - using a generator for frames
        ani = FuncAnimation(self.reorder_fig, update, 
                            frames=lambda:itertools.count(), interval=500, 
                            repeat=False, blit=False) #blit=False as we redraw the entire plot

        plt.tight_layout()
        self.reorder_canvas.draw()

    def setup_advanced_vertex_cover_tab(self):
        # Input Frame
        input_frame = tk.Frame(self.advanced_vertex_cover_tab)
        input_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Nodes Input
        tk.Label(input_frame, text="Nodes:").pack(side=tk.LEFT)
        self.adv_nodes_entry = tk.Entry(input_frame, width=30)
        self.adv_nodes_entry.pack(side=tk.LEFT, padx=5)
        self.adv_nodes_entry.insert(0, "A,B,C,D,E")

        # Edges Input
        tk.Label(input_frame, text="Edges:").pack(side=tk.LEFT)
        self.adv_edges_entry = tk.Entry(input_frame, width=30)
        self.adv_edges_entry.pack(side=tk.LEFT, padx=5)
        self.adv_edges_entry.insert(0, "A-B,A-C,B-D,C-D,C-E")

        # Advanced Vertex Cover Method
        methods_frame = tk.Frame(self.advanced_vertex_cover_tab)
        methods_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        tk.Button(methods_frame, text="Approximation", 
                  command=self.approximation_vertex_cover).pack(side=tk.LEFT, padx=5)
        tk.Button(methods_frame, text="Compare Methods", 
                  command=self.compare_vertex_cover_methods).pack(side=tk.LEFT, padx=5)

        # Result Label
        self.adv_vertex_cover_result = tk.Label(self.advanced_vertex_cover_tab, text="")
        self.adv_vertex_cover_result.pack(side=tk.TOP, padx=10, pady=10)

        # Matplotlib Figure for Advanced Visualization
        self.adv_vc_fig, self.adv_vc_ax = plt.subplots(figsize=(10, 7))
        self.adv_vc_canvas = FigureCanvasTkAgg(self.adv_vc_fig, master=self.advanced_vertex_cover_tab)
        self.adv_vc_canvas_widget = self.adv_vc_canvas.get_tk_widget()
        self.adv_vc_canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    def create_adv_graph(self):
        nodes = [n.strip() for n in self.adv_nodes_entry.get().split(',')]
        edges = [tuple(e.strip().split('-')) for e in self.adv_edges_entry.get().split(',')]
        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        return G

    def approximation_vertex_cover(self):
        G = self.create_adv_graph()
        cover = self.greedy_vertex_cover_helper(G) #reuse greedy algorithm for approximation
        self.visualize_vertex_cover(G, cover, "Approximation")

    def greedy_vertex_cover_helper(self,G): #Helper to reuse greedy logic.
        cover = set()
        edges = set(G.edges())
        while edges:
            degrees = {node: len(list(G.neighbors(node))) for node in G.nodes}
            max_degree_node = max(degrees, key=degrees.get)
            cover.add(max_degree_node)
            for neighbor in list(G.neighbors(max_degree_node)):
                edges.discard((max_degree_node, neighbor))
                edges.discard((neighbor, max_degree_node))
            G.remove_node(max_degree_node)
        return cover

    def compare_vertex_cover_methods(self):
        G = self.create_adv_graph()
        greedy_cover = self.greedy_vertex_cover_helper(G.copy())
        try:
            brute_force_cover = self.brute_force_vertex_cover_helper(G.copy()) #Helper for brute force on advanced tab.
            self.adv_vertex_cover_result.config(text=f"Greedy Cover: {greedy_cover}\nBrute Force Cover: {brute_force_cover}")
        except Exception as e: #Brute force can be slow. Handle potential issues.
            self.adv_vertex_cover_result.config(text=f"Greedy Cover: {greedy_cover}\nBrute Force: {e}")

    def brute_force_vertex_cover_helper(self, G): #Helper to reuse brute force logic.
        nodes = list(G.nodes())

        def is_vertex_cover(subset):
            return all(u in subset or v in subset for u, v in G.edges())

        min_cover = None
        for k in range(1, len(nodes) + 1):
            for subset in combinations(nodes, k):
                if is_vertex_cover(subset):
                    min_cover = set(subset)
                    break
            if min_cover:
                break

        if min_cover:
            return min_cover
        else:
            raise Exception("No vertex cover found (Brute Force)")

import itertools
root = tk.Tk()
app = ComprehensiveVisualizationApp(root)
root.mainloop()
