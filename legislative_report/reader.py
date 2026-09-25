import csv
from pathlib import Path
from typing import Dict, Iterable, Iterator

from legislative_report.constants import (
    DEFAULT_BILLS_FILENAME,
    DEFAULT_LEGISLATORS_FILENAME,
    DEFAULT_VOTE_RESULTS_FILENAME,
    DEFAULT_VOTES_FILENAME,
)
from legislative_report.models import Bill, Legislator, Vote, VoteResult


class LegislativeDataReader:
    """Reads CSV files from a directory and returns domain objects."""

    def __init__(self, data_dir: Path):
        self._data_dir = data_dir

    def read_legislators(
        self, filename: str = DEFAULT_LEGISLATORS_FILENAME
    ) -> Dict[int, Legislator]:
        legislators = {}
        for row in self._read_rows(filename):
            legislator = Legislator(id=int(row["id"]), name=row["name"])
            legislators[legislator.id] = legislator
        return legislators

    def read_bills(self, filename: str = DEFAULT_BILLS_FILENAME) -> Dict[int, Bill]:
        bills = {}
        for row in self._read_rows(filename):
            bill = Bill(
                id=int(row["id"]),
                title=row["title"],
                sponsor_id=int(row["sponsor_id"]),
            )
            bills[bill.id] = bill
        return bills

    def read_votes(self, filename: str = DEFAULT_VOTES_FILENAME) -> Dict[int, Vote]:
        votes = {}
        for row in self._read_rows(filename):
            vote = Vote(id=int(row["id"]), bill_id=int(row["bill_id"]))
            votes[vote.id] = vote
        return votes

    def read_vote_results(
        self, filename: str = DEFAULT_VOTE_RESULTS_FILENAME
    ) -> Iterable[VoteResult]:
        for row in self._read_rows(filename):
            yield VoteResult(
                id=int(row["id"]),
                legislator_id=int(row["legislator_id"]),
                vote_id=int(row["vote_id"]),
                vote_type=int(row["vote_type"]),
            )

    def _read_rows(self, filename: str) -> Iterator[dict]:
        file_path = self._data_dir / filename
        with file_path.open(newline="", encoding="utf-8") as csv_file:
            yield from csv.DictReader(csv_file)
