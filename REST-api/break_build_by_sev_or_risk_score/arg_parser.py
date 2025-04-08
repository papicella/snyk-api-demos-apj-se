# arg_parser.py
import argparse

SEVERITY_LEVELS = ["low", "medium", "high", "critical"]

def parse_command_line_args():
    parser = argparse.ArgumentParser(description="Snyk API Examples")
    parser.add_argument(
        "--orgId", type=str, help="The Snyk Organisation Id", required=True
    )
    parser.add_argument(
        "--snykToken", type=str, help="Snyk Token", required=True
    )
    parser.add_argument(
        "--scmRepo", type=str, help="SCM Repo name", required=True
    )
    parser.add_argument(
        "--scmRepoBranch", type=str, help="SCM Repo branch name", required=True
    )
    parser.add_argument(
        "--snykIntId", type=str, help="Snyk SCM Integration ID", required=True
    )
    parser.add_argument(
        "--projId", type=str, help="Snyk Project ID", required=False
    )
    parser.add_argument(
        "--severityThreshold", type=str, help="Severity threshold (low, medium, high, critical)", required=False
    )
    parser.add_argument(
        "--riskScoreThreshold", type=int, help="Break the build by risk score instead of severity on the given threshold", required=False
    )

    args = parser.parse_args()

    # Sanitize and validate arguments
    if args.severityThreshold:
        args.severityThreshold = args.severityThreshold.strip().lower()
        if args.severityThreshold not in SEVERITY_LEVELS:
            raise ValueError(f"Invalid severity threshold: {args.severityThreshold}. Must be one of {SEVERITY_LEVELS}.")

    if args.riskScoreThreshold:
        if args.riskScoreThreshold < 0 or args.riskScoreThreshold > 1000:
            raise ValueError("Risk score threshold must be a positive integer between 0 and 1000.")

    args.orgId = args.orgId.strip()
    args.snykToken = args.snykToken.strip()
    args.scmRepo = args.scmRepo.strip()
    args.scmRepoBranch = args.scmRepoBranch.strip()
    args.snykIntId = args.snykIntId.strip()
    if args.projId:
        args.projId = args.projId.strip()

    return args