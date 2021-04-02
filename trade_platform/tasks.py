from stock_platform.celery import app
from trade_platform.models import Offer, Inventory, User
from trade_platform.services import take_price, create_trade, is_correct
from django.core.mail import send_mail

@app.task
def offer():
    offers = Offer.objects.filter(is_active=True).select_related('person')
    offers_sell = [offer for offer in offers if offer.is_sell]
    offers_buy = [offer for offer in offers if not offer.is_sell]
    for buyer_offer in offers_buy:
        goof_offers = []
        for seller_offer in offers_sell:
            if is_correct(buyer_offer, seller_offer):
                goof_offers.append(seller_offer)
            best_offer = goof_offers[0]
            for offer in goof_offers[1:]:
                if take_price(offer) < take_price(best_offer):
                    best_offer = offer
            create_trade(buyer_offer, best_offer)


@app.task
def change_price(info):
    Offer.objects.filter(pk__in=info['offers']).update(price=info['price'])


@app.task
def send_item_update_notificate(id):
    users = User.objects.filter(profile__inventory__item=id).values_list('email', flat=True)
    send_mail('shrek', 'shrek the best movie', 'uservice589@gmail.com', users)