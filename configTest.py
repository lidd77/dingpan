from configparser import ConfigParser
cfg = ConfigParser()

cfg.read('config.ini')
cfg.sections()
phone = cfg.get('Unity','phone')
warnTime = cfg.get('Unity','warnTime')

symbal1 = cfg.get('pair1','symbol')
priceHigh2 = cfg.getfloat('pair2','priceHigh')
priceLow3 = cfg.getfloat('pair3','priceLow')
 
print(warnTime)
print(phone,symbal1,priceHigh2,priceLow3)
 