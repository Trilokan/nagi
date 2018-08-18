def purchase_calculation(unit_price, quantity, discount, tax, tax_state):
    price = 0
    if (unit_price > 0) and (quantity > 0):
        price = unit_price * quantity

    discount = discount if discount else 0
    tax = int(tax) if tax else 0

    discount_amount = (price * float(discount)/100) or 0
    discounted_amount = (price - discount_amount) or 0

    tax_amount = (discounted_amount * float(tax)/100) or 0
    taxed_amount = (discounted_amount + tax_amount) or 0
    untaxed_amount = 0
    total_amount = taxed_amount + untaxed_amount

    cgst = sgst = igst = 0
    if tax_state == 'inter_state':
        sgst = tax_amount
    elif tax_state == 'outer_state':
        cgst = igst = tax_amount / 2

    return {"cgst": cgst,
            "sgst": sgst,
            "igst": igst,
            "discounted_amount": discounted_amount,
            "discount_amount": discount_amount,
            "tax_amount": tax_amount,
            "taxed_amount": taxed_amount,
            "untaxed_amount": untaxed_amount,
            "total_amount": total_amount}
