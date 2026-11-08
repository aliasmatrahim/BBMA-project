#property strict
#include "..\\..\\m10-stage\\blueprint\\source\\custom_mtf\\CustomInputs.mqh"
input bool ExpectedValid=true;
int OnInit(){string reason;bool v=InitializeCustomInputs(reason);Print("[INPUT_ADMISSION] expected=",ExpectedValid," actual=",v," reason=",reason," passed=",v==ExpectedValid);return v==ExpectedValid?INIT_SUCCEEDED:INIT_FAILED;}
void OnTick(){}
