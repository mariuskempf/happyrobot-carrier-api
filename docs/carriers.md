# North-American Carriers

The following lists a couple of large carriers in North America, their corresponding MC and DOT numbers. It also provides
information about the Federal Motor Carrier Safety Administration (FMCSA) website and API used to retrieve official
information about the carriers. This is used for validating the eligibility.

## Overview

The following are a couple of exemplary carriers.

| Carrier                  | DOT Number | MC Number |
| ------------------------ | ---------- | --------- |
| J.B. Hunt Transport      | 80806      | 135797    |
| Werner Enterprises       | 1054507    | 441401    |
| Schneider National       | 264184     | 133655    |
| North American Van Lines | 70851      | 107012    |
| XPO Logistics Freight    | 241829     | 165377    |
| DHL Express USA          | 315026     | 123343    |

### Additional Remarks & Insights Gathered

- Large carriers have multiple entities — J.B. Hunt for example has subsidiaries each with their own DOT/MC numbers.

## FMCSA Carrier Information

**Websites and API**

- [FMCSA - Federal Motor Carrier Safety Administration](https://mobile.fmcsa.dot.gov/QCDevsite/)
- [FMCSA - API Documentation](https://mobile.fmcsa.dot.gov/QCDevsite/docs/getStarted)
- [FMCSA - SAFER System](https://safer.fmcsa.dot.gov/CompanySnapshot.aspx)

API elements considered relevant regarding eligibility of a carrier:

| Field            | Description                                                         | Type       |
| ---------------- | ------------------------------------------------------------------- | ---------- |
| allowToOperate   | Indicates if a carrier is allowed to operate by law                 | Y or N     |
| outOfService     | Carrier received out of service order and is not allowed to operate | Y or N     |
| outOfServiceDate | The date the carrier received out of service order                  | MM/DD/YYYY |
| complaintCount   | Number of customer complaints about the carrier received by FMCSA   | Number     |
| dotNumber        | U.S. DOT registered number for the carrier                          | Number     |
| mcNumber         | U.S. DOT registered motor carrier number for the carrier            | Number     |
| legalName        | Legal registered name of the carrier                                | String     |
| dbaName          | Alternative operating name of the carrier                           | String     |
