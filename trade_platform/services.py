from rest_framework.generics import get_object_or_404

from trade_platform.models import Inventory, Trade

def get_total_price(quantity, price):
    return quantity*price


def update_balance(buyer_offer, seller_offer, quantity):
    profile = buyer_offer.person
    profile.balance -= get_total_price(quantity, take_price(seller_offer))
    profile.save()
    profile = seller_offer.person
    profile.balance += get_total_price(quantity, take_price(seller_offer))
    profile.save()


def update_inventories(buyer_offer, seller_offer, quantity):
    buyer_inventory, _ = Inventory.objects.get_or_create(person=buyer_offer.person, item=buyer_offer.item)
    seller_inventory = get_object_or_404(Inventory, person=seller_offer.person, item=seller_offer.item)
    seller_inventory.quantity -= quantity
    buyer_inventory.quantity += quantity
    buyer_inventory.save()
    seller_inventory.save()


def get_quantity(buyer_offer, seller_offer):
    return buyer_offer.quantity if buyer_offer.quantity <= seller_offer.quantity else seller_offer.quantity


def update_quantity(buyer_offer, seller_offer):
    buyer_offer.quantity -= get_quantity(buyer_offer, seller_offer)
    seller_offer.quantity -= get_quantity(buyer_offer, seller_offer)


def update_active_status(buyer_offer, seller_offer):
    if buyer_offer.quantity == 0:
        buyer_offer.is_active = False
    if seller_offer.quantity == 0:
        seller_offer.is_active = False


def update_price(buyer_offer, seller_offer):
    buyer_offer.price = buyer_offer.quantity * take_price(buyer_offer)
    seller_offer.price = seller_offer.quantity * take_price(seller_offer)


def save_offers(buyer_offer, seller_offer):
    update_price(buyer_offer, seller_offer)
    update_balance(buyer_offer, seller_offer, get_quantity(buyer_offer, seller_offer))
    update_inventories(buyer_offer, seller_offer, get_quantity(buyer_offer, seller_offer))
    update_quantity(buyer_offer, seller_offer)
    update_active_status(buyer_offer, seller_offer)
    buyer_offer.save(update_fields=('quantity', 'price', 'is_active'))
    seller_offer.save(update_fields=('quantity', 'price', 'is_active'))


def create_trade(buyer_offer, seller_offer):
    trade = Trade(item=buyer_offer.item, quantity=get_quantity(buyer_offer, seller_offer), seller=seller_offer.person,
                  seller_offer=seller_offer, buyer=buyer_offer.person, buyer_offer=buyer_offer)
    trade.save()
    save_offers(buyer_offer, seller_offer)


def is_correct(buyer_offer, seller_offer):
    if (buyer_offer.person != seller_offer.person and buyer_offer.item == seller_offer.item) and (
            take_price(buyer_offer) >= take_price(seller_offer)):
        return True
    else:
        return False


def take_price(offer):
    return offer.price / offer.quantity
