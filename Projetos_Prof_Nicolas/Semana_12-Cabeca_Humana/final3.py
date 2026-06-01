import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.ndimage import gaussian_filter # NOVA BIBLIOTECA: O segredo para pele realista!

# ==========================================
# MOTOR GRÁFICO: MALHA CONTÍNUA DE ALTA RESOLUÇÃO
# ==========================================
# Grelha super densa (200x200) para suportar o filtro de suavização
u = np.linspace(0, 2 * np.pi, 200) 
v = np.linspace(-1.0, 1.2, 200)    
U, Z_grid = np.meshgrid(u, v)

# Função para calcular distância circular (evita cortes na nuca)
def ang_dist(a, b):
    return np.pi - np.abs(np.pi - np.abs(a - b))

# Mapeamento Direcional
dist_front = ang_dist(U, np.pi/2)   # Rosto
dist_back  = ang_dist(U, 3*np.pi/2) # Nuca
dist_right = ang_dist(U, 0)         # Orelha Direita
dist_left  = ang_dist(U, np.pi)     # Orelha Esquerda

# ==========================================
# FASE 1: ESCULTURA DA BASE (Argila Bruta)
# ==========================================
R_base = np.ones_like(U) * 0.45 # Raio inicial (Pescoço mais grosso)

# 1. Crânio (Formato de Cérebro - Volumoso no topo e atrás)
R_base += 0.45 * np.exp(-(dist_back**2) / 1.5) * np.exp(-(Z_grid - 0.5)**2 / 0.8)
R_base += 0.35 * np.exp(-(dist_front**2) / 2.0) * np.exp(-(Z_grid - 0.6)**2 / 0.5)

# 2. Maxilar Definido (Jawline)
# Queixo proeminente
R_base += 0.35 * np.exp(-(dist_front**2) / 0.15) * np.exp(-(Z_grid + 0.35)**2 / 0.05)
# Cantos do maxilar (ângulos da mandíbula)
jaw_corners = np.exp(-(ang_dist(U, np.pi/4)**2) / 0.15) + np.exp(-(ang_dist(U, 3*np.pi/4)**2) / 0.15)
R_base += 0.25 * jaw_corners * np.exp(-(Z_grid + 0.25)**2 / 0.08)

# 3. Maçãs do Rosto
R_base += 0.15 * jaw_corners * np.exp(-(Z_grid - 0.05)**2 / 0.08)

# Aplicar o primeiro "Gaussian Blur" (Modo 'wrap' para a malha dar a volta à cabeça sem costuras)
# Isto transforma os blocos numa estrutura óssea/muscular perfeitamente lisa
R_smooth = gaussian_filter(R_base, sigma=(4.0, 4.0), mode=('nearest', 'wrap'))

# ==========================================
# FASE 2: INJEÇÃO DE DETALHES FACIAIS
# ==========================================
R_details = np.zeros_like(U)

# 4. Nariz (Ponte definida + Ponta redonda e projetada)
bridge = 0.12 * np.exp(-(dist_front**2) / 0.015) * np.exp(-(Z_grid - 0.05)**2 / 0.1)
tip = 0.22 * np.exp(-(dist_front**2) / 0.03) * np.exp(-(Z_grid + 0.12)**2 / 0.02)
R_details += bridge + tip

# 5. Orelhas (Formato em C com cavidade interior)
ear_pos = np.exp(-(dist_left**2) / 0.04) + np.exp(-(dist_right**2) / 0.04)
ear_outer = 0.18 * ear_pos * np.exp(-(Z_grid - 0.05)**2 / 0.08)  # Borda externa
ear_inner = -0.08 * ear_pos * np.exp(-(Z_grid - 0.05)**2 / 0.02) # Cavidade do ouvido
R_details += ear_outer + ear_inner

# 6. Lábios (Superior e Inferior)
lip_upper = 0.05 * np.exp(-(dist_front**2) / 0.04) * np.exp(-(Z_grid + 0.22)**2 / 0.001)
lip_lower = 0.04 * np.exp(-(dist_front**2) / 0.03) * np.exp(-(Z_grid + 0.26)**2 / 0.001)
R_details += lip_upper + lip_lower

# 7. Arco das Sobrancelhas
R_details += 0.06 * np.exp(-(dist_front**2) / 0.2) * np.exp(-(Z_grid - 0.25)**2 / 0.01)

# Somar os detalhes à base e aplicar uma suavização final leve para fundir na pele
R_final = R_smooth + R_details
R_final = gaussian_filter(R_final, sigma=(1.0, 1.0), mode=('nearest', 'wrap'))

# ==========================================
# FASE 3: CONVERSÃO 3D E ESTÚDIO
# ==========================================

# Matemática para Coordenadas XYZ
X = R_final * np.cos(U)
Y = R_final * np.sin(U) # O Rosto está a apontar para o eixo Y
Z = Z_grid

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Fundo Ciano
ax.set_facecolor('cyan')
fig.patch.set_facecolor('cyan')

# Tom de Pele
skin_color = '#f1c27d'

print("A aplicar o filtro Scipy Gaussian_Filter. A gerar maxilar orgânico e detalhes finos...")

# Superfície Única e Sólida (Opaca)
ax.plot_surface(X, Y, Z, color=skin_color, alpha=1.0, 
                rstride=1, cstride=1, linewidth=0, antialiased=True, shade=True)

# Limites da Câmara
ax.set_xlim([-1.2, 1.2])
ax.set_ylim([-1.2, 1.2])
ax.set_zlim([-1.0, 1.2])
ax.set_box_aspect([1, 1, 1])
ax.set_axis_off()

def update(frame):
    # Rotação total em 1 segundo (36 graus * 10 frames)
    ax.view_init(elev=10, azim=frame * 36 - 90) # -90 alinha o início com a câmara
    return fig,

FPS = 10
frames_list = list(range(10)) 

print(f"A exportar o scanner 3D: 1 segundo a {FPS} FPS...")

ani = FuncAnimation(fig, update, frames=frames_list, interval=100)
output_file = "rosto_esculpido_2.gif"
ani.save(output_file, writer=PillowWriter(fps=FPS))

print(f"Operação concluída com sucesso! Ficheiro final: {output_file}")
plt.close()