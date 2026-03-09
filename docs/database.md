# Seed Loads — Acme Logistics

The following table shows the dummy data created for this demo and stored in the SQLITE Database `data/loads.db`.

# Seed Loads — Acme Logistics

| ID      | Origin          | Destination        | Equipment | Commodity              | Miles | Offer Rate | Ceiling (110%) | Pickup           | Delivery         | Weight (lbs) | Pieces | Notes                   |
| ------- | --------------- | ------------------ | --------- | ---------------------- | ----- | ---------- | -------------- | ---------------- | ---------------- | ------------ | ------ | ----------------------- |
| LOAD001 | Chicago, IL     | Dallas, TX         | Dry Van   | General Merchandise    | 921   | $2,200.00  | $2,420.00      | 2026-03-10 06:00 | 2026-03-11 18:00 | 42,000       | 24     | No touch freight        |
| LOAD002 | Los Angeles, CA | Phoenix, AZ        | Dry Van   | Electronics            | 372   | $850.00    | $935.00        | 2026-03-10 08:00 | 2026-03-10 20:00 | 38,000       | 12     | Dock to dock            |
| LOAD003 | New York, NY    | Boston, MA         | Dry Van   | Retail Goods           | 215   | $620.00    | $682.00        | 2026-03-10 10:00 | 2026-03-10 18:00 | 28,000       | 30     | Liftgate required       |
| LOAD004 | Denver, CO      | Kansas City, MO    | Dry Van   | Auto Parts             | 601   | $1,100.00  | $1,210.00      | 2026-03-12 07:00 | 2026-03-13 06:00 | 40,000       | 50     | No touch                |
| LOAD005 | Nashville, TN   | Charlotte, NC      | Dry Van   | Furniture              | 408   | $720.00    | $792.00        | 2026-03-10 08:00 | 2026-03-10 16:00 | 32,000       | 15     | Inside delivery         |
| LOAD006 | Dallas, TX      | Los Angeles, CA    | Dry Van   | Clothing & Apparel     | 1,435 | $2,800.00  | $3,080.00      | 2026-03-13 07:00 | 2026-03-14 20:00 | 45,000       | 60     | Team driver preferred   |
| LOAD007 | Miami, FL       | Atlanta, GA        | Dry Van   | Medical Supplies       | 662   | $950.00    | $1,045.00      | 2026-03-11 10:00 | 2026-03-12 08:00 | 30,000       | 20     | No touch freight        |
| LOAD008 | Memphis, TN     | Houston, TX        | Dry Van   | Industrial Chemicals   | 561   | $1,380.00  | $1,518.00      | 2026-03-13 06:00 | 2026-03-14 10:00 | 38,000       | 10     | Hazmat placard required |
| LOAD009 | Seattle, WA     | San Francisco, CA  | Dry Van   | Consumer Electronics   | 808   | $1,650.00  | $1,815.00      | 2026-03-11 07:00 | 2026-03-12 14:00 | 36,000       | 45     | No touch                |
| LOAD010 | Columbus, OH    | Philadelphia, PA   | Dry Van   | Paper Products         | 460   | $780.00    | $858.00        | 2026-03-10 09:00 | 2026-03-10 20:00 | 34,000       | 22     | Dock to dock            |
| LOAD011 | Phoenix, AZ     | Denver, CO         | Dry Van   | Sporting Goods         | 602   | $1,250.00  | $1,375.00      | 2026-03-12 08:00 | 2026-03-13 10:00 | 40,000       | 35     | No touch freight        |
| LOAD012 | Charlotte, NC   | Chicago, IL        | Dry Van   | Auto Parts             | 789   | $1,480.00  | $1,628.00      | 2026-03-11 06:00 | 2026-03-12 18:00 | 42,000       | 28     | Team driver preferred   |
| LOAD013 | Atlanta, GA     | Miami, FL          | Reefer    | Fresh Produce          | 662   | $1,450.00  | $1,595.00      | 2026-03-11 07:00 | 2026-03-12 10:00 | 36,000       | 40     | Temp: 34-38F            |
| LOAD014 | Seattle, WA     | Portland, OR       | Reefer    | Frozen Seafood         | 174   | $480.00    | $528.00        | 2026-03-11 06:00 | 2026-03-11 12:00 | 22,000       | 18     | Temp: 28-32F            |
| LOAD015 | Minneapolis, MN | Chicago, IL        | Reefer    | Dairy Products         | 409   | $980.00    | $1,078.00      | 2026-03-12 06:00 | 2026-03-12 18:00 | 34,000       | 28     | Temp: 34-38F            |
| LOAD016 | Portland, OR    | San Francisco, CA  | Reefer    | Wine & Spirits         | 638   | $1,250.00  | $1,375.00      | 2026-03-12 08:00 | 2026-03-13 10:00 | 26,000       | 200    | Temp: 55-60F            |
| LOAD017 | Los Angeles, CA | Las Vegas, NV      | Reefer    | Ice Cream              | 270   | $650.00    | $715.00        | 2026-03-10 10:00 | 2026-03-10 18:00 | 24,000       | 30     | Temp: 28-32F            |
| LOAD018 | Chicago, IL     | Minneapolis, MN    | Reefer    | Meat & Poultry         | 409   | $920.00    | $1,012.00      | 2026-03-11 08:00 | 2026-03-12 06:00 | 32,000       | 15     | Temp: 34-38F            |
| LOAD019 | Dallas, TX      | Houston, TX        | Reefer    | Fresh Vegetables       | 239   | $420.00    | $462.00        | 2026-03-10 07:00 | 2026-03-10 13:00 | 20,000       | 50     | Temp: 34-38F            |
| LOAD020 | Boston, MA      | New York, NY       | Reefer    | Frozen Meals           | 215   | $540.00    | $594.00        | 2026-03-12 09:00 | 2026-03-12 15:00 | 18,000       | 24     | Temp: 28-32F            |
| LOAD021 | Denver, CO      | Salt Lake City, UT | Reefer    | Pharmaceuticals        | 371   | $780.00    | $858.00        | 2026-03-13 08:00 | 2026-03-13 18:00 | 28,000       | 8      | Temp: 34-38F            |
| LOAD022 | Houston, TX     | Memphis, TN        | Flatbed   | Steel Coils            | 561   | $1,750.00  | $1,925.00      | 2026-03-10 09:00 | 2026-03-11 08:00 | 44,000       | 6      | Tarping required        |
| LOAD023 | Phoenix, AZ     | Las Vegas, NV      | Flatbed   | Construction Equipment | 297   | $590.00    | $649.00        | 2026-03-11 09:00 | 2026-03-11 15:00 | 38,000       | 3      | Oversized load          |
| LOAD024 | Kansas City, MO | St. Louis, MO      | Flatbed   | Lumber                 | 248   | $420.00    | $462.00        | 2026-03-10 11:00 | 2026-03-10 16:00 | 36,000       | 1      | Straps provided         |
| LOAD025 | Atlanta, GA     | Nashville, TN      | Flatbed   | Steel Beams            | 249   | $680.00    | $748.00        | 2026-03-11 08:00 | 2026-03-11 16:00 | 40,000       | 12     | Tarping required        |
| LOAD026 | Dallas, TX      | San Antonio, TX    | Flatbed   | Heavy Machinery        | 274   | $380.00    | $418.00        | 2026-03-10 07:00 | 2026-03-10 13:00 | 42,000       | 2      | Escort required         |
| LOAD027 | Chicago, IL     | Detroit, MI        | Flatbed   | Sheet Metal            | 281   | $620.00    | $682.00        | 2026-03-12 08:00 | 2026-03-12 16:00 | 38,000       | 20     | Straps provided         |
| LOAD028 | Los Angeles, CA | Seattle, WA        | Flatbed   | Wind Turbine Parts     | 1,137 | $2,100.00  | $2,310.00      | 2026-03-13 06:00 | 2026-03-14 18:00 | 44,000       | 4      | Tarping required        |
| LOAD029 | Denver, CO      | Albuquerque, NM    | Flatbed   | Concrete Pipes         | 449   | $720.00    | $792.00        | 2026-03-11 09:00 | 2026-03-11 19:00 | 36,000       | 8      | Straps provided         |
| LOAD030 | Memphis, TN     | Birmingham, AL     | Flatbed   | Roofing Materials      | 210   | $480.00    | $528.00        | 2026-03-10 10:00 | 2026-03-10 16:00 | 40,000       | 100    | Tarping required        |

> **Note:** Use the VSC extension [SQLite Viewer](https://marketplace.visualstudio.com/items?itemName=qwtel.sqlite-viewer) to visualize the actual `loads.db` and interact with it.

**Equipment Types Explained**

- **Dry Van** - An enclosed box trailer — the standard truck you see everywhere. Used for general freight.
- **Reefer (Refrigerated)** - An enclosed trailer with a built-in refrigerator. Used for anything that needs temperature control.
- **Flatbed** - An open trailer with no sides or roof — just a flat platform. Used for oversized, heavy, or awkwardly shaped freight that can't fit in an enclosed trailer
