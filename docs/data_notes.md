# FSA API — Cardiff data notes

- Authority: Cardiff
- LocalAuthorityId: 339
- Total establishments: 3,506 (meta.totalCount)
- At pageSize=500, that's ~8 pages

## Fields per establishment I'll keep

- FHRSID — unique id (e.g. 979940)
- BusinessName (e.g. "200 Degrees Coffee Shop")
- BusinessType (e.g. "Restaurant/Cafe/Canteen", "Retailers - other", "Pub/bar/nightclub")
- PostCode (e.g. "CF10 2BH")
- RatingValue — digit string "0"–"5" in Cardiff; may be text ("AwaitingInspection", "Exempt") elsewhere
- RatingDate (ISO datetime, e.g. "2025-09-17T00:00:00")
- scores.Hygiene, scores.Structural, scores.ConfidenceInManagement
- geocode.latitude, geocode.longitude — sometimes null (saw "3S Convenience Store" with both null)

## Gotchas

- A bad authority id returns HTTP 200 with 0 results, no error — my loader must fail if 0 rows
- RatingValue is a string, not a number
- geocode fields can be null → cast carefully in SQL
- The underlying local authority code is 556 (Vale of Glamorgan SRS) even though we query by id 339