import argparse
from pathlib import Path
from typing import Tuple

from legislative_report.reader import LegislativeDataReader
from legislative_report.report_builder import LegislativeReportBuilder
from legislative_report.writer import ReportWriter


def generate_reports(data_dir: Path, output_dir: Path) -> Tuple[Path, Path]:
    reader = LegislativeDataReader(data_dir)

    legislators = reader.read_legislators()
    bills = reader.read_bills()
    votes = reader.read_votes()
    vote_results = reader.read_vote_results()

    builder = LegislativeReportBuilder(legislators, bills, votes, vote_results)
    legislator_tallies, bill_tallies = builder.build()

    writer = ReportWriter(output_dir)
    legislators_report_path = writer.write_legislator_report(legislator_tallies)
    bills_report_path = writer.write_bill_report(bill_tallies, legislators)

    return legislators_report_path, bills_report_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generates support/opposition reports from legislative data in CSV format."
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data"),
        help="Directory containing bills.csv, legislators.csv, votes.csv, and vote_results.csv (default: ./data)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output"),
        help="Directory where the output CSVs will be saved (default: ./output)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    legislators_path, bills_path = generate_reports(args.data_dir, args.output_dir)
    print(f"Report by legislators generated in: {legislators_path}")
    print(f"Report by bills generated in: {bills_path}")
