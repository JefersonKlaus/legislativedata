from typing import Dict, Iterable, Optional, Tuple

from legislative_report.constants import VOTE_TYPE_NAY, VOTE_TYPE_YEA
from legislative_report.models import (
    Bill,
    BillTally,
    Legislator,
    LegislatorTally,
    Vote,
    VoteResult,
)


class LegislativeReportBuilder:
    def __init__(
        self,
        legislators: Dict[int, Legislator],
        bills: Dict[int, Bill],
        votes: Dict[int, Vote],
        vote_results: Iterable[VoteResult],
    ):
        self._legislators = legislators
        self._bills = bills
        self._votes = votes
        self._vote_results = vote_results

    def build(self) -> Tuple[Dict[int, LegislatorTally], Dict[int, BillTally]]:
        legislator_tallies = self._initialize_legislator_tallies()
        bill_tallies = self._initialize_bill_tallies()

        for vote_result in self._vote_results:
            bill_id = self._resolve_bill_id(vote_result.vote_id)
            if bill_id is None:
                continue

            self._apply_vote(vote_result, bill_id, legislator_tallies, bill_tallies)

        return legislator_tallies, bill_tallies

    def _initialize_legislator_tallies(self) -> Dict[int, LegislatorTally]:
        return {
            legislator_id: LegislatorTally(legislator=legislator)
            for legislator_id, legislator in self._legislators.items()
        }

    def _initialize_bill_tallies(self) -> Dict[int, BillTally]:
        return {bill_id: BillTally(bill=bill) for bill_id, bill in self._bills.items()}

    def _resolve_bill_id(self, vote_id: int) -> Optional[int]:
        vote = self._votes.get(vote_id)
        return vote.bill_id if vote else None

    def _apply_vote(
        self,
        vote_result: VoteResult,
        bill_id: int,
        legislator_tallies: Dict[int, LegislatorTally],
        bill_tallies: Dict[int, BillTally],
    ) -> None:
        legislator_tally = legislator_tallies.get(vote_result.legislator_id)
        bill_tally = bill_tallies.get(bill_id)

        if vote_result.vote_type == VOTE_TYPE_YEA:
            if legislator_tally:
                legislator_tally.supported_bills += 1
            if bill_tally:
                bill_tally.supporter_count += 1
        elif vote_result.vote_type == VOTE_TYPE_NAY:
            if legislator_tally:
                legislator_tally.opposed_bills += 1
            if bill_tally:
                bill_tally.opposer_count += 1
        # 1 (Yea) and 2 (Nay) only
