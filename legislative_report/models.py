from dataclasses import dataclass


@dataclass(frozen=True)
class Legislator:
    id: int
    name: str


@dataclass(frozen=True)
class Bill:
    id: int
    title: str
    sponsor_id: int


@dataclass(frozen=True)
class Vote:
    id: int
    bill_id: int


@dataclass(frozen=True)
class VoteResult:
    id: int
    legislator_id: int
    vote_id: int
    vote_type: int


@dataclass
class LegislatorTally:
    legislator: Legislator
    supported_bills: int = 0
    opposed_bills: int = 0


@dataclass
class BillTally:
    bill: Bill
    supporter_count: int = 0
    opposer_count: int = 0
