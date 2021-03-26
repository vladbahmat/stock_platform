from stock_platform.celery import app
from trade_platform.models import Offer
from trade_platform.services import take_price, create_trade, is_correct


@app.task
def offer():
    offers = list(Offer.objects.select_related('item'))
    offers_sell = [offer for offer in offers if (offer.is_sell and offer.is_active)]
    offers_buy = [offer for offer in offers if (not offer.is_sell and offer.is_active)]
    for buyer_offer in offers_buy:
        suitable_offers = []
        for seller_offer in offers_sell:
            if is_correct(buyer_offer, seller_offer):
                suitable_offers.append(seller_offer)
            best_offer = suitable_offers[0]
            for offer in suitable_offers[1:]:
                if take_price(offer) < take_price(best_offer):
                    best_offer = offer
            create_trade(buyer_offer, best_offer)
