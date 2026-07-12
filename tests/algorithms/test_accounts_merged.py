import pytest
import sys
from pathlib import Path

# ensure repository root is on sys.path so top-level packages are importable
root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root))

from Algorithms.graph.traversal.accounts_merged import accountsMerge


def _normalize(accounts):
	"""Normalize accounts list to a set of (name, emails-tuple) for comparison."""
	return {(acc[0], tuple(acc[1:])) for acc in accounts}


def test_example_merge():
	input_accounts = [
		["John", "johnsmith@mail.com", "john_newyork@mail.com"],
		["John", "johnnybravo@mail.com"],
		["John", "johnsmith@mail.com", "john00@mail.com"],
		["Mary", "mary@mail.com"],
	]

	expected = {
		("John", ("john00@mail.com", "john_newyork@mail.com", "johnsmith@mail.com")),
		("John", ("johnnybravo@mail.com",)),
		("Mary", ("mary@mail.com",)),
	}

	assert _normalize(accountsMerge(input_accounts)) == expected


def test_disjoint_same_name():
	input_accounts = [["Alex", "a1@mail.com"], ["Alex", "a2@mail.com"]]

	expected = {
		("Alex", ("a1@mail.com",)),
		("Alex", ("a2@mail.com",)),
	}

	assert _normalize(accountsMerge(input_accounts)) == expected


def test_chain_merge():
	input_accounts = [
		["Bob", "b1@mail.com", "b2@mail.com"],
		["Bob", "b2@mail.com", "b3@mail.com"],
		["Bob", "b3@mail.com", "b4@mail.com"],
	]

	expected = {("Bob", ("b1@mail.com", "b2@mail.com", "b3@mail.com", "b4@mail.com")),}

	assert _normalize(accountsMerge(input_accounts)) == expected


def test_duplicate_emails_within_account():
	input_accounts = [["Eve", "e1@mail.com", "e1@mail.com", "e2@mail.com"]]

	expected = {("Eve", ("e1@mail.com", "e2@mail.com")),}

	assert _normalize(accountsMerge(input_accounts)) == expected

