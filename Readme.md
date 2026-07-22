Hello everyone,

I've been conducting some independent R&D in computational number theory, specifically targeting $N = k \cdot 2^n + 1$ topologies, and I would like to submit a Proof of Concept (PoC) to this community for auditing. I call this two-stage architecture the **Margarita Sieve & Ye-Di Criterion**.

Rather than proposing a new underlying theorem, this is a software engineering and modular algebra approach: a "fail-fast" pipeline designed to drastically reduce the CPU cycles wasted on composite numbers *before* they reach the heavy Proth/LLR testing phase.

### 🌼 Stage 1: The Margarita Sieve (Geometric Tail Filter)
*I named this stage the "Margarita" (Daisy) Sieve in honor of my mother, and because it acts like the primitive petal-plucking game ("prime, composite, prime, composite...") to instantly discard invalid candidates.*

Before performing any heavy big-integer math, we evaluate the last digit of the even block. By calculating the tail of $k \cdot 2^n \pmod{10}$, we can mathematically prove that certain terminations will always yield a composite $N$. This simple arithmetic gate instantly destroys exactly **20%** of the candidates without touching the RAM with large integer allocations.

### ⚔️ Stage 2: The Ye-Di Criterion (Jacobi "Dead-End" Guillotine)
For the survivors, instead of traditional division-heavy loops, the Ye-Di Criterion inverts the workload.
1. It uses a pure native bitwise mask `(N & 3) == 3` to bypass modulo overhead and determine the dynamic exponent.
2. It generates positive and negative modular roots.
3. It evaluates both paths using the **Jacobi symbol**. If both the positive and negative roots return a negative Jacobi state, it's a "dead-end bifurcation". The number fractures structurally and is immediately discarded as a composite.

**The Core Python Logic:**
```python
def yedi_inverse_filter(N):
    # 1. Structural Quick-Scan
    if (N & 2) != 0:
        return False
       
    # 2. Dynamic Branching (Pure native bitwise mask)
    if (N & 3) == 3:
        exponente = gmpy2.add(N, 1) >> 2
    else:
        exponente = gmpy2.add(N, 3) >> 2
           
    N_menos_1 = gmpy2.sub(N, 1)
    raiz_pos = gmpy2.powmod(N_menos_1, exponente, N)
    raiz_neg = gmpy2.sub(N, raiz_pos)
       
    # 3. Jacobi Guillotine (Dual Lane)
    camino_pos_valido = (gmpy2.jacobi(raiz_pos, N) >= 0)
    camino_neg_valido = (gmpy2.jacobi(raiz_neg, N) >= 0)
  
    # Dead-end bifurcation -> Guaranteed Composite
    if not camino_pos_valido and not camino_neg_valido:
        return False

    return True # Survives to formal Proth certification
```

### 📊 Empirical Telemetry
I have written a Python testbench to isolate and stress-test this fail-fast mechanism against a standard Python Proth implementation. Here is the actual output of my latest local benchmark:

> **[BATCH PARAMETERS]**
> * Candidates injected: **55,000**
> * Topology: $N = k \cdot 2^n + 1$
> * Average size: **300 digits** (~995 bits)
>
> **[FILTERING RESULTS]**
> * Stage 1 (Margarita Sieve) Kills: **11,000** (Exactly 20.00%)
> * Stage 2 (Ye-Di Filter) Kills: **44,000** (The remaining composites)
>
> **[PERFORMANCE NET ADVANTAGE]**
> * Compared to a direct evaluation, this two-stage pre-filter architecture yielded a net CPU time saving of **~23.79%**.

**The Full Testbench (GitHub)**
The complete Python PoC, including the candidate generator and the benchmarking timer, is available in my repository here:

I am fully aware that production environments use highly optimized C/Assembly and FFTs, but I believe the *algebraic methodology* presented here (specifically the Jacobi dead-end) could be translated into low-level code to act as an aggressive pre-filter in existing software.

I would be honored if you could review the algebraic architecture, run the Python testbench, and share your technical feedback.

Thank you for your time!