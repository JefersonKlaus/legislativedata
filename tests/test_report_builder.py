import unittest

from legislative_report.models import Bill, Legislator, Vote, VoteResult
from legislative_report.report_builder import LegislativeReportBuilder


class LegislativeReportBuilderTest(unittest.TestCase):
    def setUp(self):
        self.legislators = {
            1: Legislator(id=1, name="Rep. Jane Doe"),
            2: Legislator(id=2, name="Rep. John Roe"),
        }
        self.bills = {10: Bill(id=10, title="Some Act", sponsor_id=1)}
        self.votes = {100: Vote(id=100, bill_id=10)}

    def _build(self, vote_results):
        builder = LegislativeReportBuilder(
            self.legislators, self.bills, self.votes, vote_results
        )
        return builder.build()

    def test_yea_vote_increments_supporter_counts(self):
        vote_results = [VoteResult(id=1, legislator_id=1, vote_id=100, vote_type=1)]

        legislator_tallies, bill_tallies = self._build(vote_results)

        self.assertEqual(legislator_tallies[1].supported_bills, 1)
        self.assertEqual(legislator_tallies[1].opposed_bills, 0)
        self.assertEqual(bill_tallies[10].supporter_count, 1)
        self.assertEqual(bill_tallies[10].opposer_count, 0)

    def test_nay_vote_increments_opposer_counts(self):
        vote_results = [VoteResult(id=1, legislator_id=2, vote_id=100, vote_type=2)]

        legislator_tallies, bill_tallies = self._build(vote_results)

        self.assertEqual(legislator_tallies[2].opposed_bills, 1)
        self.assertEqual(legislator_tallies[2].supported_bills, 0)
        self.assertEqual(bill_tallies[10].opposer_count, 1)
        self.assertEqual(bill_tallies[10].supporter_count, 0)

    def test_every_legislator_appears_even_without_votes(self):
        legislator_tallies, _ = self._build(vote_results=[])

        self.assertIn(1, legislator_tallies)
        self.assertIn(2, legislator_tallies)
        self.assertEqual(legislator_tallies[1].supported_bills, 0)
        self.assertEqual(legislator_tallies[2].opposed_bills, 0)

    def test_every_bill_appears_even_without_votes(self):
        _, bill_tallies = self._build(vote_results=[])

        self.assertIn(10, bill_tallies)
        self.assertEqual(bill_tallies[10].supporter_count, 0)
        self.assertEqual(bill_tallies[10].opposer_count, 0)

    def test_vote_result_with_unknown_vote_id_is_ignored_safely(self):
        vote_results = [VoteResult(id=1, legislator_id=1, vote_id=999, vote_type=1)]

        legislator_tallies, bill_tallies = self._build(vote_results)

        self.assertEqual(legislator_tallies[1].supported_bills, 0)
        self.assertEqual(bill_tallies[10].supporter_count, 0)

    def test_vote_result_from_unknown_legislator_still_counts_for_bill(self):
        vote_results = [VoteResult(id=1, legislator_id=999, vote_id=100, vote_type=1)]

        _, bill_tallies = self._build(vote_results)

        self.assertEqual(bill_tallies[10].supporter_count, 1)

    def test_unknown_vote_type_is_ignored(self):
        vote_results = [VoteResult(id=1, legislator_id=1, vote_id=100, vote_type=3)]

        legislator_tallies, bill_tallies = self._build(vote_results)

        self.assertEqual(legislator_tallies[1].supported_bills, 0)
        self.assertEqual(legislator_tallies[1].opposed_bills, 0)
        self.assertEqual(bill_tallies[10].supporter_count, 0)
        self.assertEqual(bill_tallies[10].opposer_count, 0)

    def test_multiple_votes_are_tallied_independently(self):
        vote_results = [
            VoteResult(id=1, legislator_id=1, vote_id=100, vote_type=1),
            VoteResult(id=2, legislator_id=2, vote_id=100, vote_type=2),
        ]

        legislator_tallies, bill_tallies = self._build(vote_results)

        self.assertEqual(legislator_tallies[1].supported_bills, 1)
        self.assertEqual(legislator_tallies[2].opposed_bills, 1)
        self.assertEqual(bill_tallies[10].supporter_count, 1)
        self.assertEqual(bill_tallies[10].opposer_count, 1)


if __name__ == "__main__":
    unittest.main()
