# Entrega do desafio Onfly

## Correções
1. **Status de faturamento** (`status_policy.py`). O filtro excluía apenas `CANCELLED` e incluía `NO_SHOW` nos totais financeiros e de noites. A regra passou a aceitar somente `CONFIRMED`. Todas as reservas continuam entrando nas contagens por status.
2. **Noites de quarto** (`stay_calculator.py`). O cálculo subtraía os números dos dias do mês, o que gerava resultados incorretos quando a estadia atravessava um mês ou ano. A diferença agora usa as datas completas e é multiplicada pelo número de quartos.
3. **Conversão para reais** (`currency_converter.py`). O conversor dividia o valor pela taxa e usava `float`, o que invertia a operação e podia perder precisão. A conversão agora multiplica `amount` por `rate_to_brl` com `Decimal`, e o arredondamento ocorre na serialização do relatório.
4. **Ranking de hotéis** (`report_builder.py`). A chave de ordenação original colocava os menores valores primeiro. O ranking agora prioriza o maior valor acumulado e usa o `hotel_id` em ordem crescente para desempatar.

## Investigação
Comparei as regras do enunciado com os testes fornecidos e acompanhei o fluxo do CLI (ler → converter tipos → contar status → filtrar CONFIRMED → agregar) até a geração do JSON. Conferi primeiro quais reservas entravam na agregação, depois como as noites e os valores eram calculados e depois, como o ranking era ordenado. Os testes adicionais verificam o desempate no ranking, o relatório sem reservas confirmadas e o arredondamento após a soma.

## Validação
Rode os comandos abaixo na raiz do projeto, com Python 3.11 ou superior e o ambiente virtual ativo.

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

O comando abaixo reproduz a validação com a amostra.

```bash
PYTHONPATH=src python -m onfly_report --input data/exemplo-validacao.csv --rates data/taxas_cambio.csv --output output/exemplo.json
```

A execução da amostra retornou 12 reservas, 9 confirmadas, 28 noites de quarto e R$ 7.566,00 de total, conforme o enunciado.
O comando abaixo gera o relatório da base completa.

```bash
PYTHONPATH=src python -m onfly_report --input data/reservas_hoteis.csv --rates data/taxas_cambio.csv --output output/report.json
```

### Resultado do pytest
A suíte reúne cinco testes fornecidos e dois adicionais (adicionadas em tests/test_report_edge_cases.py). Os dois testes adicionados tem como objetivo testar se o relatório ordena corretamente os hotéis com a mesma quantidade de noites usando o hotel_id como critério de desempate e se os valores em BRL são arredondados corretamente após a agregação dos dados.
```bash
.......                                                                                                                                                                  [100%]
7 passed in 0.94s
```
