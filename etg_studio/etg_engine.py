"""
ETG-P Engine — Motore computazionale della catena metrica ETG-P.

CLAUSOLA OBBLIGATORIA: Questo NON è ETG. È una modellizzazione di ETG.
I valori ℝ⁺ sono rappresentazioni strumentali, non ontologia del sistema.

Catena implementata:
    Σ_CU →(H_C)→ Z_C →(F_C)→ Δ_ℓ

Fonti canoniche:
    - ETG_P/01_OPERATORI/OPERATORI_INFORMAZIONALI.md
    - ETG_P/02_FRASI/PRIMA_FRASE_ESTESA.md
    - ETG_P/04_VINCOLI/INDIPENDENZA_RISOLUZIONE.md

Data: 2026-02-28
Autore: Opus (Notaio/Assemblatore) + Sub-agente Matematico
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Strutture dati
# ---------------------------------------------------------------------------

@dataclass
class PianoD:
    """
    Piano disciplinare D.
    DH_D = gradiente di tenuta in bit (ETG-P, via Indipendenza di Risoluzione).
    """
    nome: str
    dh_d: float  # bit — capacità sintattica massima del piano

    def __post_init__(self):
        if self.dh_d <= 0:
            raise ValueError(f"DH_D deve essere > 0, ricevuto {self.dh_d}")


@dataclass
class Unita_ell:
    """
    Unità minima di stabilizzazione valutabile (ℓ).
    Esclusivamente inter — VIETATO in intra.
    ℓ := ⟨D, V(D), A(D), DH_ℓ, Δ_ℓ⟩
    """
    piano: PianoD
    v_l: float = 0.0   # valenza linguistica
    a_l: float = 0.0   # attuabilità linguistica
    v_c: float = 0.0   # valenza collocativa
    a_c: float = 0.0   # costo di mantenimento
    dh_ell: float = 0.0  # gradiente di tenuta dell'unità in bit
    delta_ell: float = 0.0  # scarto (calcolato dalla catena)

    def __post_init__(self):
        if self.dh_ell <= 0:
            raise ValueError(f"DH_ℓ deve essere > 0, ricevuto {self.dh_ell}")

    @property
    def stabilizzata(self) -> bool:
        """Δ_ℓ ≤ DH_ℓ ⇒ ℓ ∈ L (Eq. 4)"""
        return self.delta_ell <= self.dh_ell

    @property
    def delta_strutturale(self) -> float:
        """Δ := |V_l − A_l| + |V_c − A_c| (Eq. 5)"""
        return abs(self.v_l - self.a_l) + abs(self.v_c - self.a_c)


@dataclass
class AggregatoCU:
    """
    Σ_CU — Linguaggio aggregato del CU.
    Distribuzione sintattica p_i condizionata a un piano D.
    """
    piano: PianoD
    distribuzione: list[float] = field(default_factory=list)

    def __post_init__(self):
        if self.distribuzione:
            self._valida_distribuzione()

    def _valida_distribuzione(self):
        if any(p < 0 for p in self.distribuzione):
            raise ValueError("p_i deve essere >= 0")
        s = sum(self.distribuzione)
        if not math.isclose(s, 1.0, rel_tol=1e-6):
            raise ValueError(f"Σ p_i deve essere 1.0, ricevuto {s}")


# ---------------------------------------------------------------------------
# Operatori della catena ETG-P
# ---------------------------------------------------------------------------

def h_c(aggregato: AggregatoCU) -> float:
    """
    H_C(Σ_CU | D) = - Σ (p_i · log₂ p_i)  →  ℝ⁺ (bit)

    Operatore di dispersione sintattica (Shannon).
    Opera in regime inter, condizionato a un D specifico.
    Non è cross-D (competenza di K).

    Rif: OPERATORI_INFORMAZIONALI.md sezione 1
    """
    if not aggregato.distribuzione:
        return 0.0

    entropia = 0.0
    for p in aggregato.distribuzione:
        if p > 0:
            entropia -= p * math.log2(p)
    return entropia


def z_c(h_c_val: float, dh_d: float) -> float:
    """
    Z_C(D) = H_C(Σ_CU | D) / (DH_D - H_C(Σ_CU | D))

    Impedenza sintattica — resistenza che il piano oppone al transito.
    Formula candidata (27/02/2026).

    Rif: OPERATORI_INFORMAZIONALI.md sezione 3
    """
    if h_c_val < 0:
        raise ValueError(f"H_C deve essere >= 0, ricevuto {h_c_val}")
    if h_c_val >= dh_d:
        return math.inf  # blocco strutturale (Eq. 16: Δ = Δ_MAX ⇒ STOP)
    if h_c_val == 0:
        return 0.0
    return h_c_val / (dh_d - h_c_val)


def f_c(z_c_val: float, dh_d: float, dh_ell: float) -> float:
    """
    F_C(Z_C, DH_D, DH_ℓ) = Z_C² · (DH_D / DH_ℓ)

    Operatore metrico di variazione (ispirato a Fisher).
    Produce Δ_ℓ — terzo anello della catena.
    Formula candidata (28/02/2026).

    Rif: OPERATORI_INFORMAZIONALI.md sezione 2
    """
    if dh_ell <= 0:
        raise ValueError(f"DH_ℓ deve essere > 0, ricevuto {dh_ell}")
    if math.isinf(z_c_val):
        return math.inf  # blocco strutturale
    return (z_c_val ** 2) * (dh_d / dh_ell)


# ---------------------------------------------------------------------------
# Catena completa
# ---------------------------------------------------------------------------

@dataclass
class RisultatoCatena:
    """Risultato della catena Σ_CU →(H_C)→ Z_C →(F_C)→ Δ_ℓ"""
    h_c: float        # dispersione in bit
    z_c: float        # impedenza
    f_c: float        # scarto metrico (= Δ_ℓ)
    delta_ell: float   # alias di f_c per chiarezza
    dh_ell: float      # soglia di stabilizzazione
    stabilizzata: bool  # Δ_ℓ ≤ DH_ℓ

    def __str__(self):
        stato = "ell in L" if self.stabilizzata else "ell NOT in L (blocco)"
        return (
            f"H_C = {self.h_c:.4f} bit | "
            f"Z_C = {self.z_c:.4f} | "
            f"Delta_ell = {self.delta_ell:.4f} | "
            f"DH_ell = {self.dh_ell:.4f} | "
            f"{stato}"
        )


def catena_etg_p(aggregato: AggregatoCU, ell: Unita_ell) -> RisultatoCatena:
    """
    Esegue la catena completa ETG-P:
        Σ_CU →(H_C)→ Z_C →(F_C)→ Δ_ℓ

    Input:
        aggregato: Σ_CU condizionato a un piano D
        ell: unità ℓ su cui calcolare lo scarto

    Output:
        RisultatoCatena con tutti i valori intermedi

    Rif: PRIMA_FRASE_ESTESA.md
    """
    # Anello 1: dispersione
    val_h_c = h_c(aggregato)

    # Anello 2: impedenza
    val_z_c = z_c(val_h_c, aggregato.piano.dh_d)

    # Anello 3: scarto metrico
    val_f_c = f_c(val_z_c, aggregato.piano.dh_d, ell.dh_ell)

    # Aggiorna ℓ
    ell.delta_ell = val_f_c

    return RisultatoCatena(
        h_c=val_h_c,
        z_c=val_z_c,
        f_c=val_f_c,
        delta_ell=val_f_c,
        dh_ell=ell.dh_ell,
        stabilizzata=ell.stabilizzata
    )


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 70)
    print("ETG-P Engine — Catena metrica")
    print("CLAUSOLA: Questo NON è ETG. È modellizzazione.")
    print("=" * 70)

    # Piano D_Fisica con DH = 8 bit (alta capacità sintattica)
    d_fisica = PianoD("D_Fisica", dh_d=8.0)

    # Piano D_quotidiano con DH = 3 bit (bassa capacità)
    d_quotidiano = PianoD("D_Quotidiano", dh_d=3.0)

    # Caso 1: aggregato coerente (bassa dispersione) su piano rigido
    print("\n--- Caso 1: Aggregato coerente su piano rigido ---")
    agg1 = AggregatoCU(d_fisica, [0.7, 0.2, 0.1])
    ell1 = Unita_ell(d_fisica, dh_ell=4.0)
    r1 = catena_etg_p(agg1, ell1)
    print(f"  Piano: {d_fisica.nome} (DH_D={d_fisica.dh_d})")
    print(f"  p_i = {agg1.distribuzione}")
    print(f"  {r1}")

    # Caso 2: aggregato disperso (alta dispersione) su piano rigido
    print("\n--- Caso 2: Aggregato disperso su piano rigido ---")
    agg2 = AggregatoCU(d_fisica, [0.25, 0.25, 0.25, 0.25])
    ell2 = Unita_ell(d_fisica, dh_ell=4.0)
    r2 = catena_etg_p(agg2, ell2)
    print(f"  Piano: {d_fisica.nome} (DH_D={d_fisica.dh_d})")
    print(f"  p_i = {agg2.distribuzione}")
    print(f"  {r2}")

    # Caso 3: aggregato disperso su piano fragile
    print("\n--- Caso 3: Aggregato disperso su piano fragile ---")
    agg3 = AggregatoCU(d_quotidiano, [0.25, 0.25, 0.25, 0.25])
    ell3 = Unita_ell(d_quotidiano, dh_ell=1.5)
    r3 = catena_etg_p(agg3, ell3)
    print(f"  Piano: {d_quotidiano.nome} (DH_D={d_quotidiano.dh_d})")
    print(f"  p_i = {agg3.distribuzione}")
    print(f"  {r3}")

    # Caso 4: aggregato quasi al limite su piano fragile
    print("\n--- Caso 4: Aggregato al limite su piano fragile ---")
    # H_C max per 8 stati equiprobabili = log2(8) = 3.0 = DH_D
    # Usiamo distribuzione quasi-uniforme su 7 stati -> H_C vicino a log2(7) ≈ 2.807
    agg4 = AggregatoCU(d_quotidiano, [1/7]*7)
    ell4 = Unita_ell(d_quotidiano, dh_ell=1.0)
    r4 = catena_etg_p(agg4, ell4)
    print(f"  Piano: {d_quotidiano.nome} (DH_D={d_quotidiano.dh_d})")
    print(f"  p_i = [1/7]*7  (H_C ≈ {r4.h_c:.3f}, vicino a DH_D={d_quotidiano.dh_d})")
    print(f"  {r4}")

    print("\n" + "=" * 70)
