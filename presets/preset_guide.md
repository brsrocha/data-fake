# Guia de Presets

Este guia mostra como criar presets JSON para o gerador de datasets `data-fake`.

---

## Estrutura do Arquivo

Cada preset é um arquivo `.json` dentro da pasta `presets/`. Exemplo:

```json
{
  "name": "Geográfico",
  "description": "Dataset com dados climáticos e ambientais.",
  "supported_analyses": ["EDA", "Classificacao", "Regressao"],
  "columns": [...],
  "target_columns": [...]
}
```

---

## Campos Principais

### 🔹 `name`
Nome do preset (aparece na interface).

### 🔹 `description`
Descrição resumida (opcional).

### 🔹 `supported_analyses`
Lista com os tipos de análise permitidos:
- `"EDA"`
- `"Classificacao"`
- `"Regressao"`
- `"Clusterizacao"`
- `"Inferencia"`

---

## Lista de Colunas

### 🔸 `columns`
Colunas comuns (não-target). Ordem define prioridade.

Cada coluna possui:

| Campo         | Tipo      | Obrigatório | Exemplo                        |
|---------------|-----------|-------------|--------------------------------|
| `name`        | string    | ✅          | `"Cidade"`                     |
| `data_type`   | string    | ✅          | `"numeric"`, `"text"`, `"categorical"` |
| `value_type`  | string    | ✅          | `"int"`, `"float"`, `"string"` |
| `generation`  | string    | ⬅️ ou ↓    | `"cidade"`, `"latitude"`       |
| `fixed_value` | string    | opcional    | `"Brasil"`                     |
| `range`       | array     | opcional    | `[0, 100]`                     |
| `categories`  | array     | opcional    | `["A", "B", "C"]`              |

---

### 🔸 `target_columns`
Colunas que podem ser usadas como target.

| Campo         | Tipo      | Obrigatório | Exemplo                        |
|---------------|-----------|-------------|--------------------------------|
| `name`        | string    | ✅          | `"Temperatura Média"`         |
| `data_type`   | string    | ✅          | `"numeric"`                   |
| `value_type`  | string    | ✅          | `"float"`                     |
| `target_type` | string    | ✅          | `"classificacao"` ou `"regressao"` |
| `generation`  | objeto    | ✅          | `{ "depends_on": ..., "logic": ... }` |
| `categories`  | array     | se categórica | `["Baixo", "Médio", "Alto"]` |

---

## Regras

- A **ordem das colunas** define a **prioridade**.
- Se o usuário pedir menos colunas que o total do preset, as últimas serão removidas.
- Basta adicionar o `.json` em `/presets/` para aparecer na interface.

---

## Exemplo Rápido

```json
{
  "name": "Geográfico",
  "columns": [
    {
      "name": "Cidade",
      "data_type": "text",
      "value_type": "string",
      "generation": "cidade"
    },
    {
      "name": "Altitude (m)",
      "data_type": "numeric",
      "value_type": "int",
      "range": [0, 3000]
    }
  ],
  "target_columns": [
    {
      "name": "Temperatura Média (°C)",
      "data_type": "numeric",
      "value_type": "float",
      "target_type": "regressao",
      "generation": {
        "depends_on": "Altitude (m)",
        "logic": "if Altitude > 2000 → [10.0, 20.0], else [20.0, 35.0]"
      }
    }
  ]
}
```

---

## Pronto!
Salve seu preset como `nome.json` dentro da pasta `presets/`.
