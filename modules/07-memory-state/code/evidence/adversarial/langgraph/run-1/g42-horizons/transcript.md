# langgraph · adversarial · run 1 · g42-horizons

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## hz-probe  ·  desk_probe  ·  eli  ·  2026-11-14T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | prospective | a reminder more than 90 days ahead is refused (its note would outlive every retention window) | `{"reminder_400_days_accepted": false, "reminder_60_days_accepted": true, "travel_notice_3_years_accepted": false, "results": [{"error": "a reminder can be set at most 90 days ahead; it holds the customer's own words unti …` |
| PASS | prospective | a reminder 60 days ahead is accepted | `{"reminder_400_days_accepted": false, "reminder_60_days_accepted": true, "travel_notice_3_years_accepted": false, "results": [{"error": "a reminder can be set at most 90 days ahead; it holds the customer's own words unti …` |
| PASS | semantic | a travel notice more than a year long is refused | `{"reminder_400_days_accepted": false, "reminder_60_days_accepted": true, "travel_notice_3_years_accepted": false, "results": [{"error": "a reminder can be set at most 90 days ahead; it holds the customer's own words unti …` |
