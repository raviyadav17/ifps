import smartpy as sp

class TokenExchange(sp.Contract):
    def __init__(self, admin, token_a, token_b):
        self.init(
            admin = admin,
            token_a = token_a,
            token_b = token_b,
            balances = sp.big_map(tvalue=sp.TNat, tk=sp.TAddress),
        )

    @sp.entry_point
    def deposit(self, params):
        sp.verify(sp.sender == self.data.admin, message="Only admin can deposit tokens")
        token = params.token
        amount = params.amount
        sp.verify(sp.amount == 0, message="No XTZ should be sent")
        sp.verify(amount > 0, message="Amount must be positive")
        self.data.balances[token] += amount

    @sp.entry_point
    def swap(self, params):
        token_from = params.token_from
        token_to = params.token_to
        amount = params.amount

        sp.verify(self.data.balances[token_from].get(sp.sender, 0) >= amount, message="Insufficient balance")

        amount_received = (amount * self.data.token_b) / self.data.token_a

        self.data.balances[token_from][sp.sender] -= amount
        self.data.balances[token_to][sp.sender] += amount_received

@sp.add_test(name="Token Exchange")
def test():
    admin = sp.test_account("Admin")
    user = sp.test_account("User")
    
    contract = TokenExchange(admin.address, 10, 20)
    scenario = sp.test_scenario()
    scenario.h1("Token Exchange Contract")

    scenario += contract
    scenario += contract.deposit(token=contract.data.token_a, amount=100).run(sender=admin)

    scenario.h2("Swap tokens")
    scenario += contract.swap(token_from=contract.data.token_a, token_to=contract.data.token_b, amount=20).run(sender=user)
    scenario.verify(contract.data.balances[contract.data.token_a][user.address] == 80)
    scenario.verify(contract.data.balances[contract.data.token_b][user.address] == 40)

    scenario.h2("Try to swap more tokens than available")
    with scenario.hold():
        scenario += contract.swap(token_from=contract.data.token_a, token_to=contract.data.token_b, amount=100).run(sender=user)

    scenario.h2("Try to swap without depositing first")
    with scenario.hold():
        scenario += contract.swap(token_from=contract.data.token_a, token_to=contract.data.token_b, amount=10).run(sender=user)
