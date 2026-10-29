"""
Projeto de portfólio: Análise exploratória de inadimplência
============================================================
Objetivo: investigar como score, renda e idade se relacionam com
a inadimplência (atraso de pagamento) em uma carteira de clientes.

Os dados são FICTÍCIOS, gerados no próprio script, para que o projeto
rode em qualquer computador sem depender de arquivos externos.

Bibliotecas: pandas, numpy, matplotlib
Instalação:  pip install pandas numpy matplotlib
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------------
# 1. GERAÇÃO DOS DADOS FICTÍCIOS
# ---------------------------------------------------------------
np.random.seed(42)  # garante que o resultado seja sempre o mesmo
N = 1000            # número de clientes

df = pd.DataFrame({
    "idade": np.random.randint(18, 75, N),
    "renda_mensal": np.random.normal(4500, 2000, N).round(2),
    "score": np.random.randint(0, 1001, N),
    "estado": np.random.choice(["MG", "SP", "RJ", "BA", "RS"], N),
})

# Quanto menor o score, maior a chance de inadimplência (regra simulada)
probabilidade = 1 - (df["score"] / 1000)
df["inadimplente"] = np.random.rand(N) < (probabilidade * 0.6)

# Inserindo alguns problemas de propósito, para praticar a limpeza
df.loc[np.random.choice(N, 30, replace=False), "renda_mensal"] = np.nan
df.loc[np.random.choice(N, 10, replace=False), "renda_mensal"] = -100

# ---------------------------------------------------------------
# 2. PRIMEIRO OLHAR NOS DADOS
# ---------------------------------------------------------------
print("=== Primeiras linhas ===")
print(df.head())

print("\n=== Informações gerais ===")
df.info()

print("\n=== Estatísticas descritivas ===")
print(df.describe().round(2))

print("\n=== Valores ausentes por coluna ===")
print(df.isna().sum())

# ---------------------------------------------------------------
# 3. LIMPEZA
# ---------------------------------------------------------------
# Renda negativa não faz sentido: trato como valor ausente
df.loc[df["renda_mensal"] < 0, "renda_mensal"] = np.nan

# Preencho os ausentes com a mediana (menos sensível a valores extremos)
mediana_renda = df["renda_mensal"].median()
df["renda_mensal"] = df["renda_mensal"].fillna(mediana_renda)

print(f"\nRenda ausente preenchida com a mediana: R$ {mediana_renda:.2f}")

# ---------------------------------------------------------------
# 4. NOVAS COLUNAS (faixas)
# ---------------------------------------------------------------
df["faixa_score"] = pd.cut(
    df["score"],
    bins=[0, 300, 500, 700, 1000],
    labels=["Baixo", "Regular", "Bom", "Excelente"],
    include_lowest=True,
)

df["faixa_etaria"] = pd.cut(
    df["idade"],
    bins=[17, 25, 35, 50, 75],
    labels=["18-25", "26-35", "36-50", "51+"],
)

# ---------------------------------------------------------------
# 5. ANÁLISES
# ---------------------------------------------------------------
taxa_geral = df["inadimplente"].mean() * 100
print(f"\nTaxa geral de inadimplência: {taxa_geral:.1f}%")

# Taxa de inadimplência por faixa de score
por_score = (df.groupby("faixa_score", observed=True)["inadimplente"]
               .mean().mul(100).round(1))
print("\n=== Inadimplência (%) por faixa de score ===")
print(por_score)

# Taxa de inadimplência por faixa etária
por_idade = (df.groupby("faixa_etaria", observed=True)["inadimplente"]
               .mean().mul(100).round(1))
print("\n=== Inadimplência (%) por faixa etária ===")
print(por_idade)

# Taxa de inadimplência por estado
por_estado = (df.groupby("estado")["inadimplente"]
                .mean().mul(100).round(1).sort_values(ascending=False))
print("\n=== Inadimplência (%) por estado ===")
print(por_estado)

# Renda média: adimplentes x inadimplentes
renda_media = df.groupby("inadimplente")["renda_mensal"].mean().round(2)
print("\n=== Renda média (False = adimplente, True = inadimplente) ===")
print(renda_media)

# ---------------------------------------------------------------
# 6. GRÁFICOS
# ---------------------------------------------------------------
fig, eixos = plt.subplots(1, 3, figsize=(16, 4.5))

por_score.plot(kind="bar", ax=eixos[0], color="#1f4e79")
eixos[0].set_title("Inadimplência por faixa de score")
eixos[0].set_ylabel("% de inadimplentes")
eixos[0].set_xlabel("")
eixos[0].tick_params(axis="x", rotation=0)

por_idade.plot(kind="bar", ax=eixos[1], color="#2e8b57")
eixos[1].set_title("Inadimplência por faixa etária")
eixos[1].set_ylabel("% de inadimplentes")
eixos[1].set_xlabel("")
eixos[1].tick_params(axis="x", rotation=0)

por_estado.plot(kind="bar", ax=eixos[2], color="#b8860b")
eixos[2].set_title("Inadimplência por estado")
eixos[2].set_ylabel("% de inadimplentes")
eixos[2].set_xlabel("")
eixos[2].tick_params(axis="x", rotation=0)

plt.tight_layout()
plt.savefig("grafico_inadimplencia.png", dpi=150)
print("\nGráfico salvo em grafico_inadimplencia.png")

# ---------------------------------------------------------------
# 7. EXPORTAÇÃO
# ---------------------------------------------------------------
df.to_csv("base_tratada.csv", index=False, encoding="utf-8-sig")
print("Base tratada salva em base_tratada.csv")

# ---------------------------------------------------------------
# 8. CONCLUSÕES (edite com a sua interpretação!)
# ---------------------------------------------------------------
print("""
=== CONCLUSÕES ===
1. A inadimplência cai conforme o score aumenta, o que é coerente
   com o papel do score como indicador de risco.
2. As diferenças entre estados e faixas etárias são pequenas nestes
   dados simulados; em uma base real valeria testar se são relevantes.
3. Próximos passos: aplicar um teste estatístico e construir um
   modelo simples de classificação (regressão logística).
""")
