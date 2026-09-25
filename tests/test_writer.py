import csv
import tempfile
import unittest
from pathlib import Path

from legislative_report.models import Bill, BillTally, Legislator, LegislatorTally
from legislative_report.writer import ReportWriter


class ReportWriterTest(unittest.TestCase):
    def setUp(self):
        self._temp_dir = tempfile.TemporaryDirectory()
        self.output_dir = Path(self._temp_dir.name) / "output"
        self.writer = ReportWriter(self.output_dir)

    def tearDown(self):
        self._temp_dir.cleanup()

    @staticmethod
    def _read_csv_rows(path: Path) -> list:
        with path.open(newline="", encoding="utf-8") as csv_file:
            return list(csv.DictReader(csv_file))

    def test_output_directory_is_created_if_missing(self):
        self.assertTrue(self.output_dir.exists())

    def test_write_legislator_report_has_expected_columns_and_values(self):
        legislator = Legislator(id=1, name="Rep. Jane Doe")
        tally = LegislatorTally(legislator=legislator, supported_bills=3, opposed_bills=2)

        path = self.writer.write_legislator_report({1: tally})
        rows = self._read_csv_rows(path)

        self.assertEqual(
            rows,
            [
                {
                    "id": "1",
                    "name": "Rep. Jane Doe",
                    "num_supported_bills": "3",
                    "num_opposed_bills": "2",
                }
            ],
        )

    def test_write_legislator_report_is_sorted_by_id(self):
        tallies = {
            2: LegislatorTally(legislator=Legislator(id=2, name="Rep. B")),
            1: LegislatorTally(legislator=Legislator(id=1, name="Rep. A")),
        }

        path = self.writer.write_legislator_report(tallies)
        rows = self._read_csv_rows(path)

        self.assertEqual([row["id"] for row in rows], ["1", "2"])

    def test_write_bill_report_resolves_known_sponsor_name(self):
        sponsor = Legislator(id=1, name="Rep. Jane Doe")
        bill = Bill(id=10, title="Some Act", sponsor_id=1)
        tally = BillTally(bill=bill, supporter_count=5, opposer_count=1)

        path = self.writer.write_bill_report({10: tally}, legislators={1: sponsor})
        rows = self._read_csv_rows(path)

        self.assertEqual(rows[0]["primary_sponsor"], "Rep. Jane Doe")

    def test_write_bill_report_uses_unknown_label_for_missing_sponsor(self):
        bill = Bill(id=10, title="Some Act", sponsor_id=999)
        tally = BillTally(bill=bill)

        path = self.writer.write_bill_report({10: tally}, legislators={})
        rows = self._read_csv_rows(path)

        self.assertEqual(rows[0]["primary_sponsor"], "Unknown")

    def test_write_bill_report_has_expected_columns(self):
        bill = Bill(id=10, title="Some Act", sponsor_id=1)
        tally = BillTally(bill=bill, supporter_count=5, opposer_count=1)
        sponsor = Legislator(id=1, name="Rep. Jane Doe")

        path = self.writer.write_bill_report({10: tally}, legislators={1: sponsor})
        rows = self._read_csv_rows(path)

        self.assertEqual(
            rows[0],
            {
                "id": "10",
                "title": "Some Act",
                "supporter_count": "5",
                "opposer_count": "1",
                "primary_sponsor": "Rep. Jane Doe",
            },
        )


if __name__ == "__main__":
    unittest.main()
