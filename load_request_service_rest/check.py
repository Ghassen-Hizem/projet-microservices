class CashiersCheck:
    """
    Represents a cashier's check.
    """

    def __init__(self, check_number, bank_name, bank_address, payer_name, payee_name, amount, issue_date, memo=None, routing_number=None, account_number=None):
        """
        Initializes a CashiersCheck object.

        Args:
            check_number (str): The unique identifier for the check.
            bank_name (str): The name of the issuing bank.
            bank_address (str): The address of the issuing bank.
            payer_name (str): The name of the person or entity that requested the check (often the same as the bank).
            payee_name (str): The name of the person or entity the check is payable to.
            amount (float): The amount of the check.
            issue_date (str): The date the check was issued (e.g., "YYYY-MM-DD").
            memo (str, optional): An optional memo or note. Defaults to None.
            routing_number (str, optional): The bank routing number. Defaults to None.
            account_number (str, optional): The account number the funds were drawn from. Defaults to None.
        """
        self.check_number = check_number
        self.bank_name = bank_name
        self.bank_address = bank_address
        self.payer_name = payer_name
        self.payee_name = payee_name
        self.amount = amount
        self.issue_date = issue_date
        self.memo = memo
        self.routing_number = routing_number
        self.account_number = account_number

    def __str__(self):
        """
        Returns a string representation of the CashiersCheck.
        """
        return f"Cashier's Check #{self.check_number} from {self.bank_name} payable to {self.payee_name} for ${self.amount}"

