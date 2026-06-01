import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.ndimage import gaussian_filter

# ==========================================
# 1. MOTOR GRÁFICO E GRELHA (Global)
# ==========================================
u = np.linspace(0, 2 * np.pi, 150) 
v = np.linspace(-1.0, 1.2, 150)    
U, Z_grid = np.meshgrid(u, v)

def ang_dist(a, b):
    return np.pi - np.abs(np.pi - np.abs(a - b))

dist_front = ang_dist(U, np.pi/2)
dist_back  = ang_dist(U, 3*np.pi/2)
dist_right = ang_dist(U, 0)
dist_left  = ang_dist(U, np.pi)

# ==========================================
# 2. FUNÇÕES DE TEMPO E EXPRESSÃO
# ==========================================
def calcular_intensidade(frame_local, duracao=150, frames_transicao=30):
    """ Cria uma transição suave ajustada para blocos de 150 frames """
    if frame_local < frames_transicao:
        return frame_local / float(frames_transicao)
    elif frame_local < duracao - frames_transicao:
        return 1.0
    else:
        return max(0.0, 1.0 - ((frame_local - (duracao - frames_transicao)) / float(frames_transicao)))

def gerar_geometria_facial(frame):
    """ Constrói a cabeça e aplica as expressões exageradas de Ekman """
    
    R_base = np.ones_like(U) * 0.45
    R_details = np.zeros_like(U)
    
    jaw_z = 0.35
    brow_z = 0.25
    brow_intensity = 0.06
    lip_up_z = 0.22
    lip_low_z = 0.26
    lip_corner_z = 0.24
    cheek_intensity = 0.15

    # --- LINHA TEMPORAL (6 Emoções x 150 frames = 900 frames) ---
    t = 0.0
    emocao_atual = "Neutro"

    # 1. ALEGRIA (Mantida igual)
    if 0 <= frame < 150:
        emocao_atual = "Alegria (AU 6+12)"
        t = calcular_intensidade(frame)
        lip_corner_z -= (t * 0.05)       
        cheek_intensity += (t * 0.08)    

    # 2. SURPRESA (Muito mais exagerada)
    elif 150 <= frame < 300:
        emocao_atual = "Surpresa (AU 1+2+5+26)"
        t = calcular_intensidade(frame - 150)
        brow_z += (t * 0.12)             # Sobrancelhas sobem o dobro
        jaw_z -= (t * 0.15)              # Maxilar cai drasticamente
        lip_low_z -= (t * 0.08)          # Boca muito aberta

    # 3. TRISTEZA (Mais exagerada)
    elif 300 <= frame < 450:
        emocao_atual = "Tristeza (AU 1+4+15)"
        t = calcular_intensidade(frame - 300)
        lip_corner_z += (t * 0.08)       # Cantos da boca descem muito mais
        # Centro da sobrancelha sobe e vinca fortemente
        R_details += (t * 0.08) * np.exp(-(dist_front**2) / 0.02) * np.exp(-(Z_grid - 0.32)**2 / 0.01)

    # 4. MEDO (Mais exagerada)
    elif 450 <= frame < 600:
        emocao_atual = "Medo (AU 1+2+4+5+20)"
        t = calcular_intensidade(frame - 450)
        brow_z += (t * 0.08)             # Sobrancelhas bem altas
        jaw_z -= (t * 0.06)              # Maxilar descai e tensa
        lip_corner_z += (t * 0.02)
        # Boca estica horizontalmente de forma extrema
        R_details += (t * 0.05) * np.exp(-(dist_front**2) / 0.15) * np.exp(-(Z_grid + 0.24)**2 / 0.02)

    # 5. RAIVA (Mais exagerada)
    elif 600 <= frame < 750:
        emocao_atual = "Raiva (AU 4+5+7+24)"
        t = calcular_intensidade(frame - 600)
        brow_z -= (t * 0.08)             # Sobrancelhas descem pesadamente sobre os olhos
        brow_intensity += (t * 0.06)     # Ficam extremamente grossas e vincadas
        lip_up_z += (t * 0.025)          # Lábios muito apertados/pressionados
        lip_low_z -= (t * 0.025)
        jaw_z += (t * 0.02)              # Maxilar cerrado (sobe ligeiramente)

    # 6. NOJO (Mais exagerada)
    elif 750 <= frame <= 900:
        emocao_atual = "Nojo (AU 9+10)"
        t = calcular_intensidade(frame - 750)
        lip_up_z -= (t * 0.07)           # Lábio superior sobe agressivamente (esgar)
        # Nariz enruga de forma muito pronunciada
        R_details += (t * 0.12) * np.exp(-(dist_front**2) / 0.02) * np.exp(-(Z_grid - 0.15)**2 / 0.01)
        # Olhos semicerrados (tensão à volta das órbitas)
        R_details += (t * 0.03) * (np.exp(-(ang_dist(U, np.pi/2 - 0.25)**2) / 0.015) + np.exp(-(ang_dist(U, np.pi/2 + 0.25)**2) / 0.015)) * np.exp(-(Z_grid - 0.12)**2 / 0.005)

    # --- APLICAÇÃO DA MATEMÁTICA À MALHA ---
    
    # 1. Crânio
    R_base += 0.45 * np.exp(-(dist_back**2) / 1.5) * np.exp(-(Z_grid - 0.4)**2 / 0.8)
    R_base += 0.38 * np.exp(-(dist_front**2) / 1.5) * np.exp(-(Z_grid - 0.5)**2 / 0.5)

    # 2. Maxilar e Bochechas
    R_base += 0.30 * np.exp(-(dist_front**2) / 0.08) * np.exp(-(Z_grid + jaw_z)**2 / 0.05)
    jaw_side = np.exp(-(ang_dist(U, np.pi/2 - 0.6)**2) / 0.1) + np.exp(-(ang_dist(U, np.pi/2 + 0.6)**2) / 0.1)
    R_base += 0.20 * jaw_side * np.exp(-(Z_grid + 0.15)**2 / 0.08)
    R_base += cheek_intensity * jaw_side * np.exp(-(Z_grid - 0.05)**2 / 0.05)

    R_smooth = gaussian_filter(R_base, sigma=(3.0, 3.0), mode=('nearest', 'wrap'))

    # 3. Olhos e Cavidades Oculares
    olho_esq_pos = np.exp(-(ang_dist(U, np.pi/2 - 0.25)**2) / 0.015)
    olho_dir_pos = np.exp(-(ang_dist(U, np.pi/2 + 0.25)**2) / 0.015)
    ambos_olhos = olho_esq_pos + olho_dir_pos

    R_details -= 0.08 * ambos_olhos * np.exp(-(Z_grid - 0.15)**2 / 0.01)
    R_details += 0.03 * ambos_olhos * np.exp(-(Z_grid - 0.15)**2 / 0.005)

    # 4. Nariz
    R_details += 0.10 * np.exp(-(dist_front**2) / 0.01) * np.exp(-(Z_grid - 0.05)**2 / 0.08)
    R_details += 0.15 * np.exp(-(dist_front**2) / 0.02) * np.exp(-(Z_grid + 0.10)**2 / 0.015)

    # 5. Orelhas
    ear_pos = np.exp(-(dist_left**2) / 0.04) + np.exp(-(dist_right**2) / 0.04)
    R_details += 0.15 * ear_pos * np.exp(-(Z_grid - 0.05)**2 / 0.06)
    R_details -= 0.06 * ear_pos * np.exp(-(Z_grid - 0.05)**2 / 0.015)

    # 6. Sobrancelhas
    arco_sobrancelha = np.exp(-(ang_dist(U, np.pi/2 - 0.3)**2) / 0.03) + np.exp(-(ang_dist(U, np.pi/2 + 0.3)**2) / 0.03)
    R_details += brow_intensity * arco_sobrancelha * np.exp(-(Z_grid - brow_z)**2 / 0.008)

    # 7. Lábios
    formato_boca = np.exp(-(dist_front**2) / 0.03)
    z_sup = lip_up_z + (lip_corner_z - lip_up_z) * (dist_front / 0.2)
    z_inf = lip_low_z + (lip_corner_z - lip_low_z) * (dist_front / 0.2)
    R_details += 0.04 * formato_boca * np.exp(-(Z_grid + z_sup)**2 / 0.001)
    R_details += 0.035 * formato_boca * np.exp(-(Z_grid + z_inf)**2 / 0.001)

    R_final = R_smooth + R_details
    R_final = gaussian_filter(R_final, sigma=(0.8, 0.8), mode=('nearest', 'wrap'))

    X = R_final * np.cos(U)
    Y = R_final * np.sin(U)
    Z = Z_grid

    return X, Y, Z, emocao_atual

# ==========================================
# 3. RENDERIZAÇÃO E ANIMAÇÃO
# ==========================================
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
fig.patch.set_facecolor('cyan')

def update(frame):
    ax.clear()
    ax.set_facecolor('cyan')
    ax.set_xlim([-1.2, 1.2]); ax.set_ylim([-1.2, 1.2]); ax.set_zlim([-1.0, 1.2])
    ax.set_box_aspect([1, 1, 1]); ax.set_axis_off()
    
    ax.view_init(elev=10, azim=90)

    X, Y, Z, emocao = gerar_geometria_facial(frame)

    ax.plot_surface(X, Y, Z, color='#f1c27d', alpha=1.0, 
                    rstride=1, cstride=1, linewidth=0, antialiased=True, shade=True)
    
    ax.set_title(f"{emocao} - Frame {frame}/900", color="black")
    print(f"A processar frame {frame}/900 -> {emocao}")
    
    return fig,

# 60 segundos * 15 FPS = 900 frames
FPS = 15
TOTAL_FRAMES = 900

print(f"A iniciar renderização do vídeo (Duração: 60s | {FPS} FPS)...")

# O intervalo ideal para 15 FPS é aproximadamente 66 milissegundos
ani = FuncAnimation(fig, update, frames=TOTAL_FRAMES, interval=66) 
output_file = "ekman_expressoes_exageradas.gif"
ani.save(output_file, writer=PillowWriter(fps=FPS))

print(f"\nOperação concluída com sucesso! Ficheiro final: {output_file}")
plt.close()