import gmpy2
import time
import math
import os

# =====================================================================
# FASE 1: CRIBA GEOMÉTRICA (La Marcha Atrás Predictiva)
# =====================================================================
def criba_geometrica(k, n):
    bloque_par = gmpy2.mul(k, gmpy2.mpz(1) << n)
    cola = bloque_par % 10
   
    if cola not in (0, 2, 6, 8):
        return False, None
       
    N = gmpy2.add(bloque_par, 1)
    return True, N

# =====================================================================
# FASE 2: FILTRO INVERSO (100% - Máscara Nativa)
# =====================================================================
def filtro_inverso(N):
    # 1. Escáner Rápido Estructural
    if (N & 2) != 0:
        return False, "Filtro Inverso - Nivel 1 (Sin raiz inicial)"
       
    # 2. Ramificación Dinámica (Máscara de bits nativa pura)
    if (N & 3) == 3:
        exponente = gmpy2.add(N, 1) >> 2
    else:
        exponente = gmpy2.add(N, 3) >> 2
           
    N_menos_1 = gmpy2.sub(N, 1)
    raiz_nivel1_pos = gmpy2.powmod(N_menos_1, exponente, N)
    raiz_nivel1_neg = gmpy2.sub(N, raiz_nivel1_pos)
       
    # 3. Guillotina de Jacobi (Doble Carril)
    camino_pos_valido = (gmpy2.jacobi(raiz_nivel1_pos, N) >= 0)
    camino_neg_valido = (gmpy2.jacobi(raiz_nivel1_neg, N) >= 0)
 
    if not camino_pos_valido and not camino_neg_valido:
        return False, "¡CAZADO CARMICHAEL! - Nivel 2 (Bifurcacion muerta)"

    return True, "Posible Primo Confirmado"


# =====================================================================
# FASE 3: TEST ESTRICTO DE PROTH (Certificación Final)
# =====================================================================
def certificar_proth(N):
    exponente = gmpy2.sub(N, 1) // 2
    residuo = gmpy2.powmod(3, exponente, N)
    return residuo == gmpy2.sub(N, 1)

# =====================================================================
# GENERADOR Y CAJA NEGRA
# =====================================================================
def generar_candidatos_a_medida(digitos_objetivo, cantidad_deseada):
    candidatos = []
    k = 1
    while len(candidatos) < cantidad_deseada:
        n_flotante = (digitos_objetivo - 1 - math.log10(k)) / math.log10(2)
        n = int(math.ceil(n_flotante))
        if k < (1 << n):
            candidatos.append((k, n))
        k += 2
    return candidatos

def guardar_primo_caja_negra(k, n, N):
    archivo = "Tus_Primos_Proth.txt"
    modo = 'a' if os.path.exists(archivo) else 'w'
    hora = time.strftime("%Y-%m-%d %H:%M:%S")
   
    with open(archivo, modo) as f:
        if modo == 'w':
            f.write("=== REGISTRO DE PRIMOS ABSOLUTOS ===\n")
        f.write(f"[{hora}] EXITO: k={k}, n={n} | Bits: {N.bit_length()} | Digitos: {len(str(N))}\n")

# =====================================================================
# MOTOR PRINCIPAL DE CAZA
# =====================================================================
def iniciar_caceria(digitos, cantidad):
    print("\n\n\n🚀 INICIANDO CAZADOR SOLITARIO (CRIBA + FILTRO INVERSO)...")
   
    lote = generar_candidatos_a_medida(digitos, cantidad)
    k_demo, n_demo = lote[0]
    N_demo = (k_demo * (1 << n_demo)) + 1
   
    print("\n" + "🔧 CONFIGURACIÓN DE PISTA")
    print(f"🎯 Dígitos exigidos      : {digitos}")
    print(f"📦 Tamaño en Memoria     : ~{N_demo.bit_length()} bits")
    print(f"🏎️  Candidatos en parrilla: {cantidad}")
    print("-" * 50)
   
    t_inicio = time.perf_counter()
    bloqueados_fase1 = 0
    bloqueados_fase2 = 0
    primos_cazados = 0
   
    for i, (k, n) in enumerate(lote, 1):
        print(f"\rAnalizando candidato {i}/{cantidad} (k={k}, n={n})...", end="")
       
        pasa_criba, N = criba_geometrica(k, n)
        if not pasa_criba:
            bloqueados_fase1 += 1
            continue
           
        pasa_inverso, razon = filtro_inverso(N)
        if not pasa_inverso:
            bloqueados_fase2 += 1
            continue
           
        if certificar_proth(N):
            primos_cazados += 1
            guardar_primo_caja_negra(k, n, N)
            #print(f"\n[!] 💾 CAJA NEGRA: ¡PRIMO CAZADO! (k={k}, n={n})")
           
    t_total = time.perf_counter() - t_inicio
   
    print("\n\n" + "=" * 50)
    print("📊 REPORTE DE TELEMETRÍA")
    print("=" * 50)
    print(f"⏱️ Tiempo Total               : {t_total:.2f} segundos")
    print(f"🛑 Destruidos Fase 1 (Criba)  : {bloqueados_fase1}")
    print(f"⚔️ Destruidos Fase 2 (Inverso): {bloqueados_fase2}")
    print(f"💎 PRIMOS ABSOLUTOS CAZADOS   : {primos_cazados}\n")

if __name__ == "__main__":
    DIGITOS_OBJETIVO  = 100
    CANTIDAD_A_BUSCAR = 5000
    iniciar_caceria(DIGITOS_OBJETIVO, CANTIDAD_A_BUSCAR)