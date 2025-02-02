from django.core.management.base import BaseCommand
from pos.models import Item

class Command(BaseCommand):
    help = 'Adds a list of items to stock'

    def handle(self, *args, **kwargs):
        items = [
            ("ALLSOPSS", 180),
            ("BALOZI", 210),
            ("BEST WHISKY 1/4", 450),
            ("BEST GIN 1/4", 450),
            ("BEST GIN 3/4", 1100),
            ("BEST CREAM 1/4", 500),
            ("BLACK AND WHITE 1/2", 850),
            ("BLACK AND WHITE 3/4", 1500),
            ("BRAVADO", 70),
            ("COUNTY 1/4", 300),
            ("COUNTY 3/4", 950),
            ("CHROME V 1/4", 300),
            ("CHROME V 3/4", 850),
            ("CHROME GIN 1/4", 300),
            ("GUARANA", 250),
            ("GILBEY'S 1/4", 600),
            ("GILBEY'S 1/2", 850),
            ("GILBEY'S 3/4", 1600),
            ("GUINNESS", 250),
            ("DELMONTE", 350),
            ("GOFRUT", 350),
            ("HUNTER'S 1/4", 450),
            ("HUNTER'S 1/2", 650),
            ("HUNTER'S 3/4", 1300),
            ("KANE EXTRA 1/4", 300),
            ("KANE EXTRA 3/4", 900),
            ("K.C 1/4", 350),
            ("K.C 1/2", 550),
            ("K.C 3/4", 900),
            ("KIBAO 1/4", 350),
            ("KIBAO 3/4", 850),
            ("LEMONADE", 100),
            ("S/MINUTE MAID", 100),
            ("B/MINUTE MAID", 200),
            ("PILSNER", 210),
            ("POWER PLAY", 100),
            ("PREDETOR", 100),
            ("RED BULL", 300),
            ("S/SODA", 50),
            ("B/SODA", 100),
            ("S/DASANI", 50),
            ("B/DASANI", 100),
            ("TRIPLE ACE 1/4", 300),
            ("TUSKER", 230),
            ("CIDER", 300),
            ("VAT 69 1/2", 1000),
            ("VAT 69 3/4", 2000),
            ("V & A 1/4", 450),
            ("V & A 3/4", 1300),
            ("VICEROY 1/4", 600),
            ("VICEROY 1/2", 900),
            ("VICEROY 3/4", 1800),
            ("RICHOT 1/4", 600),
            ("RICHOT 1/2", 850),
            ("WHITE CAP", 250),
            ("4TH STREET", 1350),
            ("BOND 7 1/4", 600),
            ("Kingfisher", 270)
        ]

        # Loop over each item and add to the database
        for name, price in items:
            Item.objects.get_or_create(name=name, unit_price=price)

        self.stdout.write(self.style.SUCCESS('Successfully added items to stock'))
