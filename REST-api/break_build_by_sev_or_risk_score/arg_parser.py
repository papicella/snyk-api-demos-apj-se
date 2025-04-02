# arg_parser.py
import argparse

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
        "--riskScoreThreshold", type=int, help="Break the build by risk score instead of severity on the given threashold", required=False
    )

    return parser.parse_args()