#ifndef CUSTOM_OWNER_TEST_EQUALITY
#define CUSTOM_OWNER_TEST_EQUALITY
bool SameReEntryData(ReEntryData &a,ReEntryData &b)
{
 return a.Type==b.Type &&
        a.State==b.State &&
        a.Direction==b.Direction &&
        a.Timeframe==b.Timeframe &&
        a.EntryPrice==b.EntryPrice &&
        a.StopLoss==b.StopLoss &&
        a.TakeProfit==b.TakeProfit &&
        a.StopLossPoints==b.StopLossPoints &&
        a.MA5_Level==b.MA5_Level &&
        a.MA10_Level==b.MA10_Level &&
        a.MA50_Level==b.MA50_Level &&
        a.MID_BB==b.MID_BB &&
        a.EntryCandle==b.EntryCandle &&
        a.ConfirmationCandle==b.ConfirmationCandle &&
        a.StartBar==b.StartBar &&
        a.StartCandleTime==b.StartCandleTime &&
        a.LastUpdateBar==b.LastUpdateBar &&
        a.LastUpdateCandleTime==b.LastUpdateCandleTime &&
        a.ConfirmationBar==b.ConfirmationBar &&
        a.ExpiryBar==b.ExpiryBar &&
        a.ExpiryCandleTime==b.ExpiryCandleTime &&
        a.MinCandlesRequired==b.MinCandlesRequired &&
        a.QualifyingCandles==b.QualifyingCandles &&
        a.Type1ContextState==b.Type1ContextState &&
        a.Type1OwnerSignal==b.Type1OwnerSignal &&
        a.Type1OwnerCandleTime==b.Type1OwnerCandleTime &&
        a.Type1RangingStartCandleTime==b.Type1RangingStartCandleTime &&
        a.Type1PreviousClose==b.Type1PreviousClose &&
        a.IsValid==b.IsValid &&
        a.StrengthScore==b.StrengthScore &&
        a.Reason==b.Reason;
}
bool SameExtremeLifecycleData(ExtremeLifecycleData &a,ExtremeLifecycleData &b)
{
 return a.Maturity==b.Maturity &&
        a.Direction==b.Direction &&
        a.Timeframe==b.Timeframe &&
        a.RawBar==b.RawBar &&
        a.RawCandleTime==b.RawCandleTime &&
        a.ConfirmationBar==b.ConfirmationBar &&
        a.ConfirmationCandleTime==b.ConfirmationCandleTime &&
        a.ConfirmationClose==b.ConfirmationClose &&
        a.LastUpdateBar==b.LastUpdateBar &&
        a.LastUpdateCandleTime==b.LastUpdateCandleTime &&
        a.PreviousClose==b.PreviousClose &&
        a.ProvisionalBodyAnchor==b.ProvisionalBodyAnchor &&
        a.FrozenBodyAnchor==b.FrozenBodyAnchor &&
        a.RelevantMA5==b.RelevantMA5 &&
        a.RetestStartBar==b.RetestStartBar &&
        a.RetestStartCandleTime==b.RetestStartCandleTime &&
        a.RetestCompletionBar==b.RetestCompletionBar &&
        a.RetestCompletionCandleTime==b.RetestCompletionCandleTime &&
        a.IsValid==b.IsValid &&
        a.Reason==b.Reason;
}
bool SameOwners(CustomAuxLifecycle &a,CustomAuxLifecycle &b)
{
 return a.lastClosed==b.lastClosed && SameReEntryData(a.reBuy,b.reBuy) && SameReEntryData(a.reSell,b.reSell) && SameExtremeLifecycleData(a.extremeBuy,b.extremeBuy) && SameExtremeLifecycleData(a.extremeSell,b.extremeSell);
}
#endif
