#ifndef CUSTOM_CLOSED_PRICE_FIXTURE
#define CUSTOM_CLOSED_PRICE_FIXTURE
// Prevalidated structural-unit input: complete flat M10 Close history at native bar times.
// This is a source fixture, not market/session coverage or a classifier replacement.
bool closedPriceFixture=false;string closedPriceSymbol="";int closedPriceTF=0;double closedPriceValue=0;
void SetClosedPriceFixture(string symbol,int tf,double close)
{closedPriceFixture=true;closedPriceSymbol=symbol;closedPriceTF=tf;closedPriceValue=close;}
void ClearClosedPriceFixture(){closedPriceFixture=false;}
double FixtureClosedPrice(string symbol,int tf,int shift)
{if(closedPriceFixture && symbol==closedPriceSymbol && tf==closedPriceTF)return closedPriceValue;return iClose(symbol,tf,shift);}
#define iClose FixtureClosedPrice
#endif
