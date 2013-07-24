class CreditCard:
    """A consumer credit card."""

    __slots__ = '_customer', '_bank', '_account', '_limit', '_balance'

    def __init__(self, customer, bank, acnt, limit):
        """Create a new credit card instance.

        The initial balance is zero.
        customer    the name of the customer (e.g., John Bowman )
        bank        the name of the bank (e.g., California Savings )
        acnt        the acount identifier (e.g., 5391 0375 9387 5309 )
        limit       credit limit (measured in dollars)
        """
        self._customer = customer
        self._bank = bank
        self._account = acnt
        self._limit = limit
        self._balance = 0

    def get_customer(self):
        """Return name of the customer."""
        return self._customer

    def get_bank(self):
        """Return the bank s name."""
        return self._bank

    def get_account(self):
        """Return the card identifying number stored as a string."""
        return self._account

    def get_limit(self):
        """Return current credit limit."""
        return self._limit

    def get_balance(self):
        """Return current balance."""
        return self._balance

    def charge(self, price):
        """Charge given price to the card, assuming sufficient credit limit.
        Return True if charge was processed; False if charge was denied.
        """
        if price + self._balance > self._limit: # if charge would exceed limit
            return False
        else:
            self._balance += price
            return True

    def make_payment(self, amount):
        """Process customer payment that reduces balance."""
        self._balance -= amount


class PredatoryCreditCard(CreditCard):
    """An extension to CreditCard that compounds interest and fees."""

    __slots__ = '_apr'
    OVERLIMIT_FEE = 5

    def __init__(self, customer, bank, acnt, limit, apr):
        """Create a new predatory credit card instance.

        The initial balance is zero.

        customer    the name of the customer (e.g., John Bowman )
        bank        the name of the bank (e.g., California Savings )
        acnt        the acount identifier (e.g., 5391 0375 9387 5309 )
        limit       credit limit (measured in dollars)
        apr         annual percentage rate (e.g., 0.0825 for 8.25% APR)
        """
        super().__init__(customer, bank, acnt, limit) # call super constructor
        self._apr = apr

    def get_apr(self):
        """Return the annual percentage rate."""
        return self._apr

    def charge(self, price):
        """Charge given price to the card, assuming sufficient credit limit.

        Return True if charge was processed.
        Return False and assess $5 fee if charge is denied.
        """
        success = super().charge(price)  # call inherited method
        if not success:
            self._balance += PredatoryCreditCard.OVERLIMIT_FEE # penalty
        return success

    def process_month(self):
        """Assess monthly interest on outstanding balance."""

        # if positive balance, convert APR to monthly multiplicative factor
        if self._balance > 0:
            monthly_factor = pow(1 + self._apr, 1.0/12)
            self._balance *= monthly_factor

