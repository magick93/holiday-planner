
<img src="https://miro.medium.com/v2/resize:fit:4800/format:webp/0*5kWZbfmt-zpA57Qa.jpg">


# Holiday Planner

## Getting started

1. `pnpm i` should install supabase.
1. `pnpm dev`  to spin up supabase. This may take a few minutes as it will pull down some docker images.
1. Change directory to `apps/holiday-planner-api/holiday_planner`. See also `apps/holiday-planner-api/README.md`


# Docs

See http://127.0.0.1:8000/api/docs#/

First, lets do some Geocoding!
This makes use of https://geocoding-api.open-meteo.com.


```
curl -X 'GET' \
  'http://127.0.0.1:8000/api/geocoding?name=Paris' \
  -H 'accept: */*'

```

This command will the `place` table. 

However, the Holiday Planner may not want places called **Paris** to be publicly available. There is, of course, Paris, the capital of France. But there is also Paris, Texas. Sure, its a great movie, but no one really wants to visit Paris Texas. So, we can run the following:

```
curl -X 'PATCH' \
  'http://127.0.0.1:8000/api/toggle-country-public-status/US' \
  -H 'accept: application/json'
```
This will toggle the `is_public` boolean in the `country` table. Call this twice and you should get:

```json
{
  "id": "US",
  "name": "UNITED STATES",
  "iso": "US",
  "is_public": false
}
```

And lets set France to be enabled:

```bash
curl -X 'PATCH' \
  'http://127.0.0.1:8000/api/toggle-country-public-status/FR' \
  -H 'accept: application/json'
```

You should get a response of:

```json

{
  "id": "FR",
  "name": "FRANCE",
  "iso": "FR",
  "is_public": true
}

```

Now, lets see what Places are available:

```bash

curl -X 'GET' \
  'http://127.0.0.1:8000/api/places/?page=1&page_size=100' \
  -H 'accept: application/json'

```

Paris should be in the list of results.



# Technologies in use

## Turborepo

This particular repo doesnt _really_ need a monorepo. However, I'm adding this to hopefully inform and and introduce the benefits of monorepos. See https://turbo.build/

## Supabase

Supabase is basically Postgres with batteries included. I've included this because it is a very easy way to spin up a postgres database. I also wanted to see how well the [supabase-py](https://github.com/supabase-community/supabase-py) project is developing, in particular, the support for `rpc` (postgres functions) is. 

## Postgres

Besides the usual SQL tables, some interesting pieces of logic are the following:

### Policies
The django application uses a postgres user that is assigned the `anon` role. 

There is a Row Level Security policy called `select_places_policy`. This prevents any rows in the `place` table being returned where the country id is not enabled (true).


### Upsert when Geocoding

The `upsert_places()` performs a insert or update. 
When a row is inserted, the longitude and latitude are converted to a Postgis datatype.
If there exists a row that has postgis geometry type with same value, then an update is performed.
There is a trigger in the `place` table - `update_place_updated_at` - that ensures the `updated_at` value is actually updated.


# Future improvements. 

Clearly this is not a complete application. 

If I were to improve this, some things I'd suggest are:

1. Having seperate applications for Adminstration and Public use. 
1. Using JWT for auth.
1. Have better test coverage, especially integration tests.
1. General cleanup. There are some hardcoded values, such as in the REST client call to https://geocoding-api.open-meteo.com. Also, the project structure could be improved.


