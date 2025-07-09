import pandas as pd

# Carregar o CSV
df = pd.read_csv("dados_supervisionados.csv", sep=';')
df = df.replace(',', '.', regex=True).astype(float)

# Mostrar máximos e mínimos das colunas de entrada
colunas = ['distancia', 'altura', 'velocidade', 'tipo']
print("📊 Máximos e mínimos das entradas:\n")
for coluna in colunas:
    minimo = df[coluna].min()
    maximo = df[coluna].max()
    print(f"{coluna:10}: mínimo = {minimo:.2f} | máximo = {maximo:.2f}")

# Criar dicionário de alturas únicas por tipo
print("\n📌 Dicionário de tipos e suas alturas únicas:")
dicionario_alturas_por_tipo = (
    df.groupby('tipo')['altura']
    .apply(lambda x: sorted(set(x)))
    .to_dict()
)

for tipo, alturas in dicionario_alturas_por_tipo.items():
    alturas_str = ', '.join(f"{a:.1f}" for a in alturas)
    print(f"Tipo {int(tipo)}: Alturas → [{alturas_str}]")

