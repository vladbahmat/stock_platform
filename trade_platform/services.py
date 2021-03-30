from rest_framework.generics import get_object_or_404

from trade_platform.models import Inventory, Trade


def create_trade(buyer_offer, seller_offer):
    Inventory.objects.get_or_create(person=buyer_offer.person, item=buyer_offer.item)
    quantity = buyer_offer.quantity if buyer_offer.quantity <= seller_offer.quantity else seller_offer.quantity
    total_price = quantity * take_price(seller_offer)
    trade = Trade(item=buyer_offer.item, quantity=quantity, seller=seller_offer.person, seller_offer=seller_offer,
                  buyer=buyer_offer.person, buyer_offer=buyer_offer)
    buyer_offer.quantity -= quantity
    seller_offer.quantity -= quantity
    buyer_inventory = get_object_or_404(Inventory, person=buyer_offer.person, item=buyer_offer.item)
    seller_inventory = get_object_or_404(Inventory, person=seller_offer.person, item=seller_offer.item)
    seller_inventory.quantity -= quantity
    buyer_inventory.quantity += quantity
    profile = buyer_offer.person
    profile.balance -= total_price
    profile.save()
    profile = seller_offer.person
    profile.balance += total_price
    profile.save()
    if buyer_offer.quantity == 0:
        buyer_offer.is_active = False
    if seller_offer.quantity == 0:
        seller_offer.is_active = False
    buyer_offer.price = buyer_offer.quantity * take_price(buyer_offer)
    seller_offer.price = seller_offer.quantity * take_price(seller_offer)
    trade.save()
    buyer_offer.save()
    seller_offer.save()
    buyer_inventory.save()
    seller_inventory.save()


def is_correct(buyer_offer, seller_offer):
    if (buyer_offer.person != seller_offer.person and buyer_offer.item == seller_offer.item) and (
            take_price(buyer_offer) >= take_price(seller_offer)):
        return True
    else:
        return False


def take_price(offer):
    return offer.price / offer.quantity
