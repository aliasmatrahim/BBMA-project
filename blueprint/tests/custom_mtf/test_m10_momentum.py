"""Canonical predicate extraction: direction/width/outside strict boundaries."""
from pathlib import Path
import re, subprocess, tempfile

def test_momentum_shared_classifier_equivalence():
    source=Path('blueprint/source/BBMA_EA.mq4').read_text()
    match=re.search(r'bool M10_ClassifyMomentum\(',source)
    assert match, 'Shared M10 momentum classifier missing'
    start=source.index('{',match.start());depth=1;end=start+1
    while depth:
        depth+=(source[end]=='{')-(source[end]=='}');end+=1
    function=source[match.start():end].replace('BollingerBand &','BollingerBand &')
    code='enum ENUM_DIRECTION {DIR_NONE=0,DIR_BUY=1,DIR_SELL=-1}; struct BollingerBand {double TOP_BB,MID_BB,LOW_BB,Width;};\n'+function+r'''
int main(){int n=0;for(int d=-1;d<=1;d++)for(int c=0;c<=6;c++)for(int top=0;top<=4;top++)for(int mid=0;mid<=4;mid++)for(int low=0;low<=4;low++)for(int width=0;width<=4;width++){
 BollingerBand a={(double)top,(double)mid,(double)low,(double)width}, b={3,3,3,2};
 bool valid=c>0&&top>0&&mid>0&&low>0&&width>0;
 bool expected=valid&&width>2&&((d==1&&mid>3&&top>3&&c>top)||(d==-1&&mid<3&&low<3&&c<low));
 if(M10_ClassifyMomentum(c,a,b,(ENUM_DIRECTION)d)!=expected)return 1;n++;
 } return n==13125?0:2;}
'''
    with tempfile.TemporaryDirectory() as td:
        path=Path(td);(path/'case.cpp').write_text(code)
        subprocess.run(['g++','-std=c++11',str(path/'case.cpp'),'-o',str(path/'case')],check=True)
        subprocess.run([str(path/'case')],check=True)
