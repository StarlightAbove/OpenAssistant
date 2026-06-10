import csv
import os
from typing import Optional
from plaid.api import plaid_api # type: ignore
from plaid.model.transactions_get_request import TransactionsGetRequest # type: ignore
from plaid.configuration import Configuration # type: ignore
from plaid.api_client import ApiClient # type: ignore

import google.generativeai as genai


class FinancialAgent:
    def __init__(self, plaid_client_id: str, plaid_secret: str, gemini_api_key: str):
        """Initialize Plaid and Gemini clients."""
        # Setup Plaid
        configuration = Configuration(
            host=plaid_api.Environment.Sandbox,
            api_key=plaid_secret,
        )
        api_client = ApiClient(configuration)
        self.plaid_client = plaid_api.PlaidApi(api_client)
        self.plaid_client_id = plaid_client_id
        self.plaid_secret = plaid_secret
        
        # Setup Gemini
        genai.configure(api_key=gemini_api_key)
        self.gemini_model = genai.GenerativeModel("gemini-pro")

    def get_transactions(self, access_token: str, start_date: str, end_date: str) -> list:
        """Fetch transactions from Plaid for given date range."""
        request = TransactionsGetRequest(
            client_id=self.plaid_client_id,
            secret=self.plaid_secret,
            access_token=access_token,
            start_date=start_date,
            end_date=end_date,
        )
        response = self.plaid_client.transactions_get(request)
        return response["transactions"]

    def load_budget_rules(self, config_path: str = "config/budget_rules.csv") -> list[dict]:
        """Load budget rules from CSV file."""
        rules = []
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                reader = csv.DictReader(f)
                rules = list(reader)
        return rules

    def load_demographics(self, config_path: str = "config/demographics.txt") -> Optional[dict]:
        """Load demographics from a text file."""
        if not os.path.exists(config_path):
            return None

        demographics = {}
        with open(config_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or ":" not in line:
                    continue
                key, value = line.split(":", 1)
                demographics[key.strip()] = value.strip()
        return demographics

    def evaluate_spending(
        self,
        transactions: list,
        budget_rules: list[dict],
        demographics: Optional[dict] = None,
    ) -> str:
        """Use Gemini to evaluate spending habits against budget rules."""
        transactions_text = "\n".join([
            f"- {t.get('name')}: ${t.get('amount')} ({t.get('date')})"
            for t in transactions
        ])
        
        rules_text = "\n".join([
            f"- {r.get('rule title', '')}: {r.get('rule description', '')}"
            for r in budget_rules
        ]) or "No rules defined yet"

        demographics_text = ""
        if demographics:
            demographics_text = "\n".join([
                f"- {key}: {value}" for key, value in demographics.items()
            ])

        prompt = f"""Analyze the following spending transactions against these budget rules and provide insights:

DEMOGRAPHICS:
{demographics_text or 'No demographic details provided'}

TRANSACTIONS:
{transactions_text}

BUDGET RULES:
{rules_text}

Provide a summary of spending habits, compliance with rules, and recommendations."""

        response = self.gemini_model.generate_content(prompt, temperature=0.0)
        return response.text

    def run(self, access_token: str, start_date: str, end_date: str, config_path: str = "config/budget_rules.csv") -> str:
        """Execute the full financial analysis workflow."""
        transactions = self.get_transactions(access_token, start_date, end_date)
        budget_rules = self.load_budget_rules(config_path)
        demographics = self.load_demographics("config/demographics.txt")
        analysis = self.evaluate_spending(transactions, budget_rules, demographics)
        return analysis