import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


# Função para atualizar a animação
def update(frame):
    ax.clear()
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    ax.set_axis_off()


    angle = frame * np.pi / 180
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle), 0],
                                [np.sin(angle), np.cos(angle), 0],
                                [0, 0, 1]])
    
    # Definir vértices do cubo
    vertices = np.array([[1, 1, 1],
                         [-1, 1, 1],
                         [-1, -1, 1],
                         [1, -1, 1],
                         [1, 1, -1],
                         [-1, 1, -1],
                         [-1, -1, -1],
                         [1, -1, -1]])

    # Rotacionar o cubo
    rotated_vertices = np.dot(vertices, rotation_matrix)

    # Definir faces do cubo
    faces = [[rotated_vertices[j] for j in [0, 1, 2, 3]],
             [rotated_vertices[j] for j in [0, 1, 5, 4]],
             [rotated_vertices[j] for j in [1, 2, 6, 5]],
             [rotated_vertices[j] for j in [2, 3, 7, 6]],
             [rotated_vertices[j] for j in [3, 0, 4, 7]],
             [rotated_vertices[j] for j in [4, 5, 6, 7]]]

    # Plotar as faces do cubo
    ax.add_collection3d(Poly3DCollection(faces, color='cyan', alpha=0.3))

# Configurar a figura e o eixo 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Configurar animação
ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 2), interval=50)

plt.show()
