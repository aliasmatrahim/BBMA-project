#ifndef BBMA_CUSTOM_PAIR_BINDING_V1
#define BBMA_CUSTOM_PAIR_BINDING_V1
// Planning only. Canonical identity helpers remain the sole ID/Magic owners.
struct CustomPairBinding
{
 string actual;
 int pairIndex;
 int pairId;
 int magic;
 bool append;
};
bool BuildCustomPairBindingPlan(string &universe[],string &poolActual[],int &poolIds[],int &poolMagics[],bool &poolReady[],int strategy,int instance,int capacity,CustomPairBinding &out[],string &reason)
{
 ArrayResize(out,0);reason="";int count=ArraySize(poolActual);
 if(capacity<0 || count>capacity || ArraySize(poolIds)!=count || ArraySize(poolMagics)!=count || ArraySize(poolReady)!=count)
 {reason="INVALID_PAIR_POOL";return false;}
 if(GenerateMagicNumber(strategy,instance,1)==0){reason="INVALID_DEPLOYMENT_IDENTITY";return false;}
 for(int p=0;p<count;p++)
 {
  if(poolActual[p]=="" || poolMagics[p]==0 || GenerateMagicNumber(strategy,instance,poolIds[p])!=poolMagics[p])
  {reason="INVALID_EXISTING_PAIR_IDENTITY";return false;}
  for(int q=0;q<p;q++)
   if(poolActual[p]==poolActual[q] || poolIds[p]==poolIds[q] || poolMagics[p]==poolMagics[q])
   {reason="EXISTING_PAIR_COLLISION";return false;}
 }
 CustomPairBinding staged[];int total=ArraySize(universe),next=count;
 if(ArrayResize(staged,total)!=total){reason="BINDING_ALLOCATION_FAILED";return false;}
 for(int i=0;i<total;i++)
 {
  string actual=universe[i];
  if(actual==""){reason="EMPTY_RESOLVED_SYMBOL";return false;}
  for(int prior=0;prior<i;prior++)
   if(staged[prior].actual==actual){reason="DUPLICATE_RESOLVED_SYMBOL";return false;}
  int match=-1;
  for(int j=0;j<count;j++)if(poolActual[j]==actual){match=j;break;}
  staged[i].actual=actual;staged[i].append=(match<0);
  if(match>=0)
  {
   if(!poolReady[match]){reason="EXISTING_PAIR_NOT_READY:"+actual;return false;}
   staged[i].pairIndex=match;staged[i].pairId=poolIds[match];staged[i].magic=poolMagics[match];
   continue;
  }
  if(next>=capacity){reason="COMBINED_PAIR_CAPACITY";return false;}
  int pairId=GeneratePairID(actual),magic=GenerateMagicNumber(strategy,instance,pairId);
  if(magic==0){reason="INVALID_NEW_PAIR_IDENTITY";return false;}
  for(int old=0;old<count;old++)
   if(poolIds[old]==pairId || poolMagics[old]==magic){reason="NEW_PAIR_ID_COLLISION:"+actual;return false;}
  for(int earlier=0;earlier<i;earlier++)
   if(staged[earlier].pairId==pairId || staged[earlier].magic==magic){reason="NEW_PAIR_ID_COLLISION:"+actual;return false;}
  staged[i].pairIndex=next++;staged[i].pairId=pairId;staged[i].magic=magic;
 }
 if(ArrayResize(out,total)!=total){reason="BINDING_ALLOCATION_FAILED";return false;}
 for(int k=0;k<total;k++)out[k]=staged[k];
 return true;
}
#endif
