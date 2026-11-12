"""Teste adicional: o repositório lê todas as linhas do CSV."""

from helpers import run_cli


def test_reservation_repository_reads_all_rows(tmp_path):
    """Nenhum limite artificial deve omitir reservas de arquivos maiores."""
    report = run_cli(
        tmp_path,
        [{"reservation_id": f"R-{index}"} for index in range(201)],
    )

    assert report["summary"]["total_reservations"] == 201
