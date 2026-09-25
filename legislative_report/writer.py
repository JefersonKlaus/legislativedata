import csv
from pathlib import Path
from typing import Dict, List

from legislative_report.constants import (
    BILLS_REPORT_FILENAME,
    LEGISLATORS_REPORT_FILENAME,
    UNKNOWN_SPONSOR_LABEL,
)
from legislative_report.models import BillTally, Legislator, LegislatorTally


class ReportWriter:
    """Serializa LegislatorTally e BillTally em arquivos CSV."""

    def __init__(self, output_dir: Path):
        self._output_dir = output_dir
        self._output_dir.mkdir(parents=True, exist_ok=True)

    def write_legislator_report(
        self,
        tallies: Dict[int, LegislatorTally],
        filename: str = LEGISLATORS_REPORT_FILENAME,
    ) -> Path:
        rows = [
            {
                "id": tally.legislator.id,
                "name": tally.legislator.name,
                "num_supported_bills": tally.supported_bills,
                "num_opposed_bills": tally.opposed_bills,
            }
            for tally in sorted(tallies.values(), key=lambda t: t.legislator.id)
        ]
        return self._write_csv(
            filename=filename,
            fieldnames=["id", "name", "num_supported_bills", "num_opposed_bills"],
            rows=rows,
        )

    def write_bill_report(
        self,
        tallies: Dict[int, BillTally],
        legislators: Dict[int, Legislator],
        filename: str = BILLS_REPORT_FILENAME,
    ) -> Path:
        rows = [
            {
                "id": tally.bill.id,
                "title": tally.bill.title,
                "supporter_count": tally.supporter_count,
                "opposer_count": tally.opposer_count,
                "primary_sponsor": self._resolve_sponsor_name(
                    tally.bill.sponsor_id, legislators
                ),
            }
            for tally in sorted(tallies.values(), key=lambda t: t.bill.id)
        ]
        return self._write_csv(
            filename=filename,
            fieldnames=[
                "id",
                "title",
                "supporter_count",
                "opposer_count",
                "primary_sponsor",
            ],
            rows=rows,
        )

    @staticmethod
    def _resolve_sponsor_name(
        sponsor_id: int, legislators: Dict[int, Legislator]
    ) -> str:
        sponsor = legislators.get(sponsor_id)
        return sponsor.name if sponsor else UNKNOWN_SPONSOR_LABEL

    def _write_csv(
        self, filename: str, fieldnames: List[str], rows: List[dict]
    ) -> Path:
        output_path = self._output_dir / filename
        with output_path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        return output_path
