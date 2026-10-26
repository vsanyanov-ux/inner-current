import re
import os
import sys

if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8')

FILES = [
    r"c:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Инструкция к человеку (Техпаспорт сверхпроводника и 25 побед цепи).md",
    r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\wiki\Брошюра — Инструкция к человеку (Техпаспорт сверхпроводника и 25 побед цепи).md",
]

def clean_file(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # Direct substring replacements
    replacements = [
        # Table 1
        (r"(\(\mathcal{E}_{\text{тандэн}} = d\Phi/dt\))", "(E_тандэн = dΦ/dt)"),
        (r"\(\mathcal{E}_{\text{тандэн}} = d\Phi/dt\)", "E_тандэн = dΦ/dt"),
        (r"\(\mathcal{E}_{\text{тандэн}}\)", "E_тандэн"),
        (r"\(B \sim I = dq/dt\)", "B ~ I = dq/dt"),
        (r"\((B \sim I = dq/dt)\)", "(B ~ I = dq/dt)"),
        (r"\((R_{\text{ego}}):", "(R_ego:"),
        (r"\(R_{\text{ego}}\)", "R_ego"),
        (r"\(Q = I^2 \cdot R \cdot t\)", "Q = I²·R·t"),
        (r"(\(Q = I^2 \cdot R \cdot t\))", "(Q = I²·R·t)"),
        (r"\(Z_{\text{нагрузки}}\)", "Z_нагрузки"),
        
        # General math expressions
        (r"\(I = dq/dt\)", "I = dq/dt"),
        (r"\(B \sim I\)", "B ~ I"),
        (r"\(Q = I^2 \cdot R \cdot t\)", "Q = I²·R·t"),
        (r"\(Q = I^2 R t\)", "Q = I²·R·t"),
        (r"\(R_{\text{ego}} \to 0\)", "R_ego → 0"),
        (r"\(R_{\text{ego}} \gg 0\)", "R_ego ≫ 0"),
        (r"\(R_{\text{ego}} > 0\)", "R_ego > 0"),
        (r"\(R_{\text{ego}} > 100 \ \Omega\)", "R_ego > 100 Ом"),
        (r"\(R_{\text{ego}} \to 0 \ \Omega\)", "R_ego → 0 Ом"),
        (r"\(R = 0\)", "R = 0"),
        (r"\(I > 0\)", "I > 0"),
        (r"\(I = 0\)", "I = 0"),
        (r"\(I \uparrow\uparrow\)", "I ↑↑"),
        (r"\(I_{\text{вх}} = I_{\text{вых}}\)", "I_вх = I_вых"),
        (r"\(I_{\text{attn}}\)", "I_attn"),
        (r"\(U_{\text{бат}}\)", "U_бат"),
        (r"\(P_{\text{load}}\)", "P_load"),
        (r"\(P_{\text{load}} = I^2 Z_{\text{load}}\)", "P_load = I²·Z_load"),
        (r"\(M > 0\)", "M > 0"),
        (r"\(\sum I_k = 0\)", "Σ I_k = 0"),
        (r"\(Z_{\text{load}}\)", "Z_load"),
        (r"\(Z_{\text{микро}}\)", "Z_микро"),
        (r"\(Z_{\text{внутр}} = Z_{\text{нагрузки}}\)", "Z_внутр = Z_нагрузки"),
        (r"\(Z_{\text{load}} \approx R_{\text{внутр}}\)", "Z_load ≈ R_внутр"),
        (r"\(Z_{\text{load}} \to \infty\)", "Z_load → ∞"),
        (r"\(Z \to 0\)", "Z → 0"),
        (r"\(\infty\)", "∞"),
        (r"\(R_{\text{шунта}} \ll Z_{\text{нагрузки}}\)", "R_шунта ≪ Z_нагрузки"),
        (r"\(R_{\text{посредника}}\)", "R_посредника"),
        (r"\(\Delta t > 0\)", "Δt > 0"),
        (r"\(\Delta t\)", "Δt"),
        (r"\(\ge 250\text{--}350 \text{ мс}\)", "≥ 250–350 мс"),
        (r"\(\Delta t = 0 \text{ мс}\)", "Δt = 0 мс"),
        (r"\(t_{\text{overheat}}\)", "t_overheat"),
        (r"\(\text{DC}\)", "DC"),
        (r"\(\text{ERR-01}\)", "ERR-01"),
        (r"\(\text{ERR-02}\)", "ERR-02"),
        (r"\(\text{ERR-03}\)", "ERR-03"),
        (r"\(\text{ERR-04}\)", "ERR-04"),
        (r"\(\text{ERR-01}\)–\(\text{ERR-04}\)", "ERR-01…04"),
        (r"\(U\)", "U"),
        (r"\(B\)", "B"),
        (r"\(I\)", "I"),
        (r"\(R\)", "R"),
        (r"> 180 \text{ мин без заземления}", "> 180 мин без заземления"),
        (r"Z_{\text{нагрузки}} = \infty", "Z_нагрузки = ∞"),
        (r"Z_{\text{load}} \to 0", "Z_load → 0"),
        (r"\to", "→"),
        (r"\infty", "∞"),
        (r"\text{ мин без заземления}", " мин без заземления"),
    ]

    for old, new in replacements:
        text = text.replace(old, new)

    # Any lingering \( or \)
    text = text.replace(r"\(", "").replace(r"\)", "")
    
    # Clean double parentheses like ((...))
    text = re.sub(r"\(\(([^\(\)]+)\)\)", r"(\1)", text)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Cleaned {path}")

for f in FILES:
    clean_file(f)
