import stripe
stripe.api_key = 'sk_test_51OLApAJc9YBOSInQwK7chDLLk0gCizBPCZrjJ33Rb8VjITq4PbpbDcAaPfYDDjf37gbRveyoBKPMC4XQtj0R5E5l00Bu0oh2ZR'


def get_link(amount):

    donation_amount = stripe.Price.create(
                        currency="rub",
                        unit_amount=amount*100,
                        product_data={"name": "Donation"})

    session = stripe.checkout.Session.create(
                        success_url="https://example.com/success",
                        line_items=[{"price": donation_amount['id'], "quantity": 1}],
                        mode="payment",
    )

    return session["url"], session["id"]