# Entrega 

## Objetivo

Identificar e corrigir erros presentes no projeto sobre as orientações do README.md

## Alterações realizadas

### 1. Conversão cambial

- **Arquivo:** `src/onfly_report/services/currency_converter.py`
- **Antes:** dividia o valor pela taxa e convertia `Decimal` para `float`.
- **Depois:** multiplica diretamente dois valores `Decimal`.
- **Por quê:** a regra define `amount * rate_to_brl` e exige exatidão decimal.
- **Impacto:** valores em BRL, USD e EUR passam a ser calculados corretamente sem perda binária de precisão.

### 2. Cálculo de noites

- **Arquivo:** `src/onfly_report/services/stay_calculator.py`
- **Antes:** subtraía apenas os dias do mês.
- **Depois:** subtrai os objetos `date` e usa `.days`, multiplicando pelos quartos.
- **Por quê:** a diferença civil precisa considerar mês e ano.
- **Impacto:** viradas de mês e ano produzem a quantidade correta de noites.

### 3. Regra de faturamento por status

- **Arquivo:** `src/onfly_report/services/status_policy.py`
- **Antes:** qualquer status diferente de `CANCELLED` era faturável.
- **Depois:** somente `CONFIRMED` é faturável.
- **Por quê:** `NO_SHOW` deve ser contado, mas não pode entrar em noites, valores, meses ou ranking.
- **Impacto:** os totais financeiros e operacionais respeitam a regra de negócio.

### 4. Ranking de hotéis

- **Arquivo:** `src/onfly_report/services/report_builder.py`
- **Antes:** ordenava o valor total em ordem crescente.
- **Depois:** ordena o valor em ordem decrescente e mantém `hotel_id` crescente no empate.
- **Por quê:** `top_hotels` deve apresentar os maiores totais primeiro.
- **Impacto:** o ranking e o limite `--top` retornam os hotéis corretos.

### 5. Leitura completa do CSV

- **Arquivo:** `src/onfly_report/repositories/csv_reservation_repository.py`
- **Antes:** interrompia a leitura após 200 linhas.
- **Depois:** lê todas as linhas disponíveis após validar o cabeçalho.
- **Por quê:** o arquivo principal possui 300 reservas e o contrato não define limite.
- **Impacto:** nenhuma reserva é omitida dos totais e agregações.

### 6. Teste adicional

- **Arquivo:** `tests/test_reservation_repository.py`
- **Alteração:** adiciona um teste com 201 linhas para proteger contra a reintrodução de limite artificial.
- **Justificativa:** os testes fornecidos cobriam o comportamento do relatório, mas não verificavam diretamente a leitura acima de 200 registros.

## Como validar

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r .github/instructions/requirements-dev.txt
.venv/bin/pytest -q
.venv/bin/ruff check src tests
PYTHONPATH=src .venv/bin/python -m onfly_report \
  --input data/exemplo-validacao.csv \
  --rates data/taxas_cambio.csv \
  --output output/exemplo.json
```

## Resultado

- Suíte de testes: **6 passed**.
- Lint Ruff: **sem problemas**.
- Amostra documentada: `12` reservas, `9` confirmadas, `28` noites, `7566.00` BRL.
- O relatório da alteração em formato PDF está em `entrega/relatorio-fase2.pdf`.