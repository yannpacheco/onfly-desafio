"""Testes adicionais para casos de borda do relatório."""

from helpers import run_cli

# Testa que o relatório ordena corretamente os hotéis com o mesmo número de noites, quebrando empates pelo hotel_id
def test_top_hotels_break_ties_by_hotel_id(tmp_path):
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "hotel_id": "H03", "amount": "100.00"},
            {"reservation_id": "R-2", "hotel_id": "H01", "amount": "100.00"},
            {"reservation_id": "R-3", "hotel_id": "H02", "amount": "100.00"},
        ],
        top=2,
    )

    assert [hotel["hotel_id"] for hotel in report["top_hotels"]] == ["H01", "H02"]

# Testa que o relatório arredonda corretamente os valores monetários após a agregação
def test_report_rounds_money_after_aggregation(tmp_path):
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "currency": "USD", "amount": "0.25"},
            {"reservation_id": "R-2", "currency": "USD", "amount": "0.25"},
        ],
    )

    # Cada reserva vale R$ 1,355 antes do arredondamento.
    assert report["summary"]["total_amount_brl"] == "2.71"
    assert report["summary"]["average_nightly_rate_brl"] == "1.36"
