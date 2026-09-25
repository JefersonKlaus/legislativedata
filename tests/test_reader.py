import csv
import tempfile
import unittest
from pathlib import Path

from legislative_report.models import Bill, Legislator, Vote, VoteResult
from legislative_report.reader import LegislativeDataReader


class LegislativeDataReaderTest(unittest.TestCase):
    def setUp(self):
        self._temp_dir = tempfile.TemporaryDirectory()
        self.data_dir = Path(self._temp_dir.name)
        self.reader = LegislativeDataReader(self.data_dir)

    def tearDown(self):
        self._temp_dir.cleanup()

    def _write_csv(self, filename: str, header: list, rows: list) -> None:
        file_path = self.data_dir / filename
        with file_path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header)
            writer.writerows(rows)

    def test_read_legislators_returns_dict_keyed_by_id(self):
        self._write_csv(
            "legislators.csv",
            ["id", "name"],
            [["1", "Rep. Jane Doe"], ["2", "Rep. John Roe"]],
        )

        legislators = self.reader.read_legislators()

        self.assertEqual(
            legislators,
            {
                1: Legislator(id=1, name="Rep. Jane Doe"),
                2: Legislator(id=2, name="Rep. John Roe"),
            },
        )

    def test_read_bills_parses_sponsor_id_as_int(self):
        self._write_csv(
            "bills.csv",
            ["id", "title", "sponsor_id"],
            [["10", "Some Act", "1"]],
        )

        bills = self.reader.read_bills()

        self.assertEqual(bills, {10: Bill(id=10, title="Some Act", sponsor_id=1)})

    def test_read_votes_returns_dict_keyed_by_id(self):
        self._write_csv("votes.csv", ["id", "bill_id"], [["100", "10"]])

        votes = self.reader.read_votes()

        self.assertEqual(votes, {100: Vote(id=100, bill_id=10)})

    def test_read_vote_results_yields_all_rows(self):
        self._write_csv(
            "vote_results.csv",
            ["id", "legislator_id", "vote_id", "vote_type"],
            [["1", "1", "100", "1"], ["2", "2", "100", "2"]],
        )

        vote_results = list(self.reader.read_vote_results())

        self.assertEqual(
            vote_results,
            [
                VoteResult(id=1, legislator_id=1, vote_id=100, vote_type=1),
                VoteResult(id=2, legislator_id=2, vote_id=100, vote_type=2),
            ],
        )

    def test_read_accepts_custom_filename(self):
        self._write_csv(
            "custom_legislators.csv", ["id", "name"], [["1", "Rep. Jane Doe"]]
        )

        legislators = self.reader.read_legislators(filename="custom_legislators.csv")

        self.assertEqual(legislators, {1: Legislator(id=1, name="Rep. Jane Doe")})


if __name__ == "__main__":
    unittest.main()
