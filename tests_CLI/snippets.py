#
# $Id: snippets.py 1544 $
#
""" pieces of garbage (or not so trash) code 
https://github.com/blind-coder/SpaceTrader/blob/master/SpaceTrader/src/main/java/de/anderdonau/spacetrader/Main.java
"""

GEOPOLITIC = {'civ': ['medieval', 'modern', 'evolved', 'futuristic',],
              'regim': ['dictatorship', 'monarchy', 'democracy',],
              # stable or war is boolean, no need for constant
             }

if random.choice((True, False)):
    self.status = 'peace'
else:
    self.status = 'war'

liste = [{'thekey': 'check1'}, {'thekey': 'check2'}]
any('check1' in dico.values() for dico in liste)
if not any(temp.name in planete.__dict__.values() for planete in planetes):

#bool Collision(int curseur_x,int curseur_y,AABB box)
#  if (curseur_x >= box.x && curseur_x < box.x + box.w
#      && curseur_y >= box.y && curseur_y < box.y + box.h)
#  return true; else return false;

print(planete.__dict__.keys(), planete.__dict__.values())

# http://effbot.org/pyfaq/how-do-i-get-a-list-of-all-instances-of-a-given-class.htm
# trier les objets en fonction de leur class : isinstance()

        Government = collections.namedtuple('Government',
                                          ('systemSize',
                                           'techLevel',
                                           'regim',
                                           'status'
                                           ))
        self.gov = Government(constants.SYSTEMSIZE[self.systemSize],
                              constants.TECHLEVEL[self.techLevel],
                              constants.REGIM[self.regim],
                              constants.STATUS[self.status])


        for good in list(constants.GOODS.keys()):
            self.price_slip.update({good: 0})

# mockup02.py
        #self.can1 = tk.Canvas(self.OngletTrading, width=123, height=125, bg='white')
        #self.photo = tk.PhotoImage(file='/usr/share/pixmaps/debian-logo.png')
        #self.can1.create_image(65, 65, image=self.photo)

        #self.can1.grid(in_=self.OngletTrading, padx=2, pady=2, sticky='news')

        # test
        # self.affiche.configure(text=str(self.colgauch.grid_info()))

# button: state='disabled', ou state='normal',
# devrait se changer avec self.id.configure(state='normal')

        # values=?
        cargo0 = tk.IntVar()
        # self.spin0 = tk.Spinbox(self.framecTradingInfo, from_=0, to=MAX, increment=1, width=3)
        #self.spin0.config(textvariable=cargo0, font="courrier 10", justify="center")
        # self.spin1 = tk.Spinbox(self.framecTradingInfo, from_=0, to=MAX, increment=1, width=3)
        # self.spin2 = tk.Spinbox(self.framecTradingInfo, from_=0, to=MAX, increment=1, width=3)
        # self.spin3 = tk.Spinbox(self.framecTradingInfo, from_=0, to=MAX, increment=1, width=3)
        # self.spin4 = tk.Spinbox(self.framecTradingInfo, from_=0, to=MAX, increment=1, width=3)
        # self.spin5 = tk.Spinbox(self.framecTradingInfo, from_=0, to=MAX, increment=1, width=3)
        # self.spin6 = tk.Spinbox(self.framecTradingInfo, from_=0, to=MAX, increment=1, width=3)
        # self.spin7 = tk.Spinbox(self.framecTradingInfo, from_=0, to=MAX, increment=1, width=3)
        # self.spin8 = tk.Spinbox(self.framecTradingInfo, from_=0, to=MAX, increment=1, width=3)
        # self.spin9 = tk.Spinbox(self.framecTradingInfo, from_=0, to=MAX, increment=1, width=3)
        # self.spin10 = tk.Spinbox(self.framecTradingInfo, from_=0, to=MAX, increment=1, width=3)
#
        # self.spin0.grid(in_=self.framecTradingInfo, row=0, column=0, sticky='news')
        # self.spin1.grid(in_=self.framecTradingInfo, row=1, column=0, sticky='news')
        # self.spin2.grid(in_=self.framecTradingInfo, row=2, column=0, sticky='news')
        # self.spin3.grid(in_=self.framecTradingInfo, row=3, column=0, sticky='news')
        # self.spin4.grid(in_=self.framecTradingInfo, row=4, column=0, sticky='news')
        # self.spin5.grid(in_=self.framecTradingInfo, row=5, column=0, sticky='news')
        # self.spin6.grid(in_=self.framecTradingInfo, row=6, column=0, sticky='news')
        # self.spin7.grid(in_=self.framecTradingInfo, row=7, column=0, sticky='news')
        # self.spin8.grid(in_=self.framecTradingInfo, row=8, column=0, sticky='news')
        # self.spin9.grid(in_=self.framecTradingInfo, row=9, column=0, sticky='news')
        # self.spin10.grid(in_=self.framecTradingInfo, row=10, column=0, sticky='news')



# test UI
        # menu Commerce
        self.menutrade = tk.Menu(self.menubar, tearoff=0)
        self.menutrade.add_command(label='Buy', command=self.box_alert)
        self.menutrade.add_command(label='Sell', command=self.box_alert)
        self.menutrade.add_command(label='Yard', command=self.box_alert)
        #   show spaceship state
        #   bouton acheter vaisseau/équipement
        #   bouton vendre vaisseau/équipement
        self.menutrade.add_command(label='Bank', command=self.box_error)
        #   bouton Crédit
        #   bouton Assurance
        self.menubar.add_cascade(label='Trade', menu=self.menutrade)

        # menu Tableau de service
        # Status du commandant
        # Quête
        # Vaisseau
        # Cargo spécial

        # menu Cartes
        # Information du système
        #   bouton News
        # Carte galactique => tabs

TradeItem = collections.namedtuple() ?

TradeItem = collections.namedtuple('TradeItem',
                                   ['name',
                                    'tp',
                                    'tu',
                                    'ttp',
                                    'plt',
                                    'pi',
                                    'var',
                                    'dps',
                                    'cr',
                                    'er',
                                    'mintp',
                                    'maxtp',
                                    'ro'
                                   ])

""" key: name;
tp: techProduction          // Tech level needed for production
tu: techUsage               // Tech level needed to use
ttp: techTopProduction      // Tech level which produces this item the most
plt: priceLowTech           // Medium price at lowest tech level
pi: priceInc                // Price increase per tech level
var: variance               // Max percentage above or below calculated price
dps: doublePriceStatus      // Price increases considerably when this event occurs
cr: cheapResource           // When this resource is available, this trade item is cheap
er: expensiveResource       // When this resource is available, this trade item is expensive
mintp: minTradePrice        // Minimum price to buy/sell in orbit
maxtp: maxTradePrice        // Maximum price to buy/sell in orbit
ro: roundOff                // Roundoff price for trade in orbit
"""

class TradeItem:
    """ """
    def __init__(self):
        self.name = ''
        self.techProduction = ''
        self.techUsage = ''
        self.techTopProduction = ''
        self.priceLowTech = ''
        self.priceInc = ''
        self.variance = ''
        self.doublePriceStatus = ''
        self.cheapResource = ''
        self.expensiveResource = ''
        self.minTradePrice = ''
        self.maxTradePrice = ''
        self.roundOff = ''

        # randomize a bit
        base = base + random.randrange(self.tradeitem.var)

        # price can't be negative
        if base < 0:
            base = 0


"""
    public int StandardPrice(int Good, int Size, int Tech, int Government, int Resources) {
    // *************************************************************************
    // Standard price calculation
    // *************************************************************************
    int Price;

    if (((Good == NARCOTICS) && (!Politics.mPolitics[Government].drugsOK)) || 
        ((Good == FIREARMS) && (!Politics.mPolitics[Government].firearmsOK))) {
        return 0;
    }

    // Determine base price on techlevel of system
    Price =
        Tradeitems.mTradeitems[Good].priceLowTech + (Tech * Tradeitems.mTradeitems[Good].priceInc);

    // If a good is highly requested, increase the price
    if (Politics.mPolitics[Government].wanted == Good) {
        Price = (Price * 4) / 3;
    }

    // High trader activity decreases prices
    Price = (Price * (100 - (2 * Politics.mPolitics[Government].strengthTraders))) / 100;

    // Large system = high production decreases prices
    Price = (Price * (100 - Size)) / 100;

    // Special resources price adaptation
    if (Resources > 0) {
        if (Tradeitems.mTradeitems[Good].cheapResource >= 0) {
            if (Resources == Tradeitems.mTradeitems[Good].cheapResource) {
                Price = (Price * 3) / 4;
            }
        }
        if (Tradeitems.mTradeitems[Good].expensiveResource >= 0) {
            if (Resources == Tradeitems.mTradeitems[Good].expensiveResource) {
                Price = (Price * 4) / 3;
            }
        }
    }

    // If a system can't use something, its selling price is zero.
    if (Tech < Tradeitems.mTradeitems[Good].techUsage) {
        return 0;
    }

    if (Price < 0) {
        return 0;
    }

    return Price;
    }

    public void DeterminePrices(int SystemID) {
    // *************************************************************************
    // Determine prices in specified system (changed from Current System) SjG
    // *************************************************************************
    int i;

    for (i = 0; i < MAXTRADEITEM; ++i) {
        BuyPrice[i] = StandardPrice(i, SolarSystem[SystemID].size, SolarSystem[SystemID].techLevel,
            SolarSystem[SystemID].politics, SolarSystem[SystemID].specialResources);

        if (BuyPrice[i] <= 0) {
            BuyPrice[i] = 0;
            SellPrice[i] = 0;
            continue;
        }

        // In case of a special status, adapt price accordingly
        if (Tradeitems.mTradeitems[i].doublePriceStatus >= 0) {
            if (SolarSystem[SystemID].status == Tradeitems.mTradeitems[i].doublePriceStatus) {
                BuyPrice[i] = (BuyPrice[i] * 3) >> 1;
            }
        }

        // Randomize price a bit
        BuyPrice[i] = BuyPrice[i] + GetRandom(Tradeitems.mTradeitems[i].variance) - GetRandom(
            Tradeitems.mTradeitems[i].variance);

        // Should never happen
        if (BuyPrice[i] <= 0) {
            BuyPrice[i] = 0;
            SellPrice[i] = 0;
            continue;
        }

        SellPrice[i] = BuyPrice[i];
        if (PoliceRecordScore < DUBIOUSSCORE) {
            // Criminals have to pay off an intermediary
            SellPrice[i] = (SellPrice[i] * 90) / 100;
        }
    }

    RecalculateBuyPrices(SystemID);
    }

    public void RecalculateBuyPrices(int SystemID) {
    // *************************************************************************
    // After changing the trader skill, buying prices must be recalculated.
    // Revised to be callable on an arbitrary Solar System
    // *************************************************************************
    int i;

    for (i = 0; i < MAXTRADEITEM; ++i) {
        if (SolarSystem[SystemID].techLevel < Tradeitems.mTradeitems[i].techProduction) {
            BuyPrice[i] = 0;
        } else if (((i == NARCOTICS) && (!Politics.mPolitics[SolarSystem[SystemID].politics].drugsOK)) || 
                   ((i == FIREARMS) && (!Politics.mPolitics[SolarSystem[SystemID].politics].firearmsOK))) {
            BuyPrice[i] = 0;
        } else {
            if (PoliceRecordScore < DUBIOUSSCORE) {
                BuyPrice[i] = (SellPrice[i] * 100) / 90;
            } else {
                BuyPrice[i] = SellPrice[i];
            }
            // BuyPrice = SellPrice + 1 to 12% (depending on trader skill (minimum is 1, max 12))
            BuyPrice[i] = (BuyPrice[i] * (103 + (MAXSKILL - Ship.TraderSkill())) / 100);
            if (BuyPrice[i] <= SellPrice[i]) {
                BuyPrice[i] = SellPrice[i] + 1;
            }
        }
    }
    }
"""
