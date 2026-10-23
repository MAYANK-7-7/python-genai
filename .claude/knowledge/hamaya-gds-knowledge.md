# HAMAYA — GDS / NDC / Fares Knowledge Base
# FlyByTheWay | Ingested: 2026-10-23 | Source: HAMAYA_Knowledge_Base_GDS_NDC_Fares.md

---

## HOW TO USE THIS FILE

For any question on GDS entries, PNR, pricing, ticketing, reissue/exchange, refund/cancel, NDC, Altea, Farelogix, Agent 360, or fare calculation — answer from this file first.

**Always:**
- Name the GDS (Amadeus / Galileo / Sabre) and show the entry in code format
- Explain in plain English what it does and what to check in the response
- Map confidence: [HIGH] = High · [MED] = Medium · [VERIFY] = Low
- Never present a [VERIFY] entry as certain — tell Maya to confirm in a training PCC

**Never:**
- Invent commands not in this file
- State any entry as universal — entries depend on PCC, BSP/ARC, airline configuration

**Known gaps (say "not in my knowledge base"):**
- Sabre Red 360 fare-shopper entries
- Sabre manual exchange/refund masks
- Galileo exchange and SSR/DOCS entries
- Any NDC-specific cryptic entry
- NDC settlement and GST in India

---

## BOOK 0 — LIBRARY METADATA

This knowledge base covers 4 portions:
1. **IATA 5.18 Study Pack** — Core exam preparation (fare construction, ticketing, rules)
2. **Complete Textbook** — Full IATA 5.18 reference material
3. **GDS Command Ebook** — Amadeus, Galileo, and Sabre cryptic command reference
4. **NDC New-Gen Platforms Ebook** — NDC standard, GDS NDC handling, airline direct NDC

**Confidence tags:**
- [HIGH] — Two or more sources confirmed this entry/rule
- [MED] — One source; likely correct but verify in live system
- [VERIFY] — Inferred or office-dependent; must confirm before use in production

**Known gaps in this knowledge base:**
- Sabre Red 360 entries are incomplete — Sabre Red 360 fare-shopper has limited coverage
- Galileo exchange is thin — exchange and reissue commands have minimal coverage
- NDC cryptic entries are not covered — NDC operates via API/JSON, not cryptic
- GST handling within GDS for India bookings — confirm with airline or BSP India

---

## BOOK 1 — IATA 5.18 FARES & TICKETING

### 12-STAGE IATA MACHINE MODEL

The IATA fare construction process follows 12 stages:
1. Determine journey type (OW / RT / OJ / DJ / CT / RW)
2. Identify the applicable fares for each fare component
3. Determine the routing
4. Check the rules (ATPCO Categories 1-35)
5. Apply NUC (Neutral Unit of Construction) values
6. Apply surcharges (YQ/YR)
7. Add all NUC values
8. Convert NUC to local currency using the ROE (Rate of Exchange)
9. Round to nearest currency unit
10. Add taxes (local airport charges, government levies)
11. Verify mileage (TPM ≤ MPM, or apply EMS)
12. Issue ticket (TTP in Amadeus / FQ in Galileo / WP in Sabre)

### NUC / ROE

- **NUC (Neutral Unit of Construction):** 1 NUC = 1 USD (fixed)
- **ROE (Rate of Exchange):** IATA-published per Resolution 024c (updated monthly). Never use market exchange rate.
- **NUC → Local Currency:** NUC amount × ROE = local currency fare
- Always use IATA ROE, not bank rate or market rate

### JOURNEY TYPES

| Code | Type | Description |
|---|---|---|
| OW | One-Way | Single direction, one origin to one destination |
| RT | Round Trip | Return to origin, same routing or mirror |
| OJ | Open Jaw | Origin ≠ turnaround point, or destination ≠ return origin |
| DJ | Double Open Jaw | Both origin and destination are different on outbound vs return |
| CT | Circle Trip | Multiple destinations returning to origin |
| RW | Round the World | Eastbound or westbound full circumnavigation |

### ATPCO CATEGORIES 1-35

Key categories for ticketing:
- Cat 1: Eligibility (who can buy the fare)
- Cat 2: Day/Time (when travel must occur)
- Cat 3: Seasonality (season restrictions)
- Cat 4: Flight Application (which flights the fare applies to)
- Cat 5: Advance Purchase (AP — how many days before departure)
- Cat 6: Minimum Stay
- Cat 7: Maximum Stay
- Cat 8: Stopovers
- Cat 9: Transfers (connections)
- Cat 10: Combinations (how fare components can be combined)
- Cat 11: Blackout Dates
- Cat 14: Travel Restrictions
- Cat 15: Sales Restrictions (which PCCs/agents can sell)
- Cat 16: Penalties (change/cancel fees)
- Cat 25: Tour Conductor Discounts
- Cat 26: Accompanied Travel
- Cat 31: Voluntary Changes (ALWAYS read before Cat 16 for changes)
- Cat 33: Voluntary Refunds (ALWAYS read before Cat 16 for refunds)
- Cat 35: Negotiated Fares (private fare security — overrides Cat 15)

**Priority reading order:**
- For a change/reissue: Read Cat 31 FIRST, then Cat 16
- For a refund/cancellation: Read Cat 33 FIRST, then Cat 16
- For a private/negotiated fare: Read Cat 35 FIRST — security 983

### TC AREAS (IATA Traffic Conference Areas)

- **TC1:** Americas (North America, Central America, South America, Caribbean)
  - Sub-areas: 1 (North America), 2 (Central America + Caribbean), 3 (South America)
  - Key cities: JFK, LAX, MIA, GRU, BOG, MEX

- **TC2:** Europe, Africa, Middle East
  - Sub-areas: Europe (LHR, CDG, FRA, AMS), Middle East (DXB, DOH, AUH), Africa (NBO, JNB, CAI)
  - Key cities for India routes: LHR, CDG, FRA, DXB, DOH, AUH

- **TC3:** Asia, Pacific, Indian Subcontinent
  - Sub-areas: South Asia (DEL, BOM, BLR, MAA), Southeast Asia (SIN, BKK, KUL), Northeast Asia (NRT, ICN, PEK), Pacific (SYD, MEL, AKL)
  - Key India cities: DEL (Delhi), BOM (Mumbai), BLR (Bangalore), MAA (Chennai), CCU (Kolkata), HYD (Hyderabad), AMD (Ahmedabad), PNQ (Pune)

### GLOBAL INDICATORS

Global indicators define which routing is used in fare construction:

| GI | Route |
|---|---|
| AT | Atlantic (TC1-TC2 via Atlantic) |
| PA | Pacific (TC1-TC3 via Pacific) |
| EH | Eastern Hemisphere (within TC2-TC3) |
| WH | Western Hemisphere (within TC1) |
| TS | Trans-Siberian (TC2-TC3 via Russia) |
| AP | Asia-Pacific (within TC3) |
| PO | Polar (TC1-TC3 via Pole) |
| FE | Far East (TC3 Far East) |
| SA | South Atlantic (TC1-TC2 via South Atlantic) |
| RW | Round the World |

### ROUTING — MILEAGE SYSTEM

- **TPM (Ticketed Point Mileage):** Actual mileage of the route as ticketed
- **MPM (Maximum Permitted Mileage):** Maximum mileage allowed for the fare
- **Rule:** TPM must not exceed MPM (or EMS surcharge applies)
- **EMS (Excess Mileage Surcharge):** 5M / 10M / 15M / 20M / 25M (5% to 25% surcharge tiers)
- **HIP (Higher Intermediate Point):** If a stopover point has a higher fare than the final destination, the HIP check requires a fare re-calculation
- **BHC (Backhaul Check):** Prevents routing that backtracks to a cheaper intermediate fare

### FARE BASIS CODES — DECODE ALGORITHM

A fare basis code (FBC) encodes the fare's key attributes. Example: YLOW6M

**Step-by-step decode:**
1. Position 1: Cabin class (Y=Economy, J=Business, F=First, W=Premium Economy)
2. Fare type suffix: OW/RT/AP/EE/IT/BT (see below)
3. Season code: H (High) / L (Low) / K (Shoulder) / P (Peak) / W (Winter) / S (Summer)
4. AP code: Number = days advance purchase required (e.g., 6 = 6 days, 14 = 14 days)
5. Stay requirement: M = months (6M = 6 months maximum stay)

**Fare type codes:**
- OW = One-way
- RT = Round-trip
- EE = Excursion
- AP = Advance Purchase
- PX = Apex
- IT = Inclusive Tour
- BT = Bulk/Tour
- GV = Group
- CH = Child (approximately 75% of adult fare)
- IN = Infant (approximately 10% of adult fare, no seat)
- AD = Agent Discount
- ID = Industry Discount
- SD = Student Discount
- SC = Senior Citizen
- SP = Special

**Rule:** Never decode a fare basis code from letters alone. The rule record (ATPCO) is the product. The FBC letters are the key, not the fare itself. Always pull the full rule from the GDS.

### RBD (RESERVATION BOOKING DESIGNATOR) MAP

| RBD | Cabin |
|---|---|
| F, A | First Class |
| P | First Class Premium |
| J, C, D, I, Z | Business Class |
| W | Premium Economy |
| E | Premium Economy (discounted) |
| Y, B, M, H, K, Q, L, T, V, S, N, G, U, O, X | Economy Class |

### TAXES — INDIA DOMESTIC

- **UDF (User Development Fee):** Airport development levy — varies by airport
- **ADF (Airport Development Fee):** Applies to specific airports (DEL, BOM)
- **PSF (Passenger Service Fee):** Security component
- **GST on base fare:** Economy domestic 5% / Business domestic 12% / International 0%
- **Statutory taxes:** UDF, ADF, PSF — ALWAYS refundable regardless of fare type (DGCA 2026 mandate)

---

## BOOK 2 — GDS COMMAND REFERENCE

### AMADEUS — CORE COMMANDS

**Availability:**
```
AN15NOVDELBOM     Display availability DEL-BOM 15 Nov
AN15NOVDELLHR/AAI Display availability with specific airline (Air India)
AN15NOVDELLHR*C   Business class availability
```

**Fare Display:**
```
FQD DEL LHR /AI /CY    Fare display DEL-LHR on Air India, economy
FQD DEL LHR /AI /CC    Fare display DEL-LHR on Air India, business
FQD DEL LHR /D15NOV    Fare display with travel date
```

**Fare Rules:**
```
FQN1             Display fare rules for line 1 of fare display
FQN1/R,ALL       Display ALL rule categories for line 1
FQN1/R,5         Cat 5 — Advance Purchase
FQN1/R,6         Cat 6 — Minimum Stay
FQN1/R,7         Cat 7 — Maximum Stay
FQN1/R,10        Cat 10 — Combinations
FQN1/R,15        Cat 15 — Sales Restrictions
FQN1/R,16        Cat 16 — Penalties
FQN1/R,31        Cat 31 — Voluntary Changes (READ FIRST for reissue)
FQN1/R,33        Cat 33 — Voluntary Refunds (READ FIRST for refund)
FQN1/R,35        Cat 35 — Negotiated Fares
```

**PNR Build:**
```
SS2Y1            Sell 2 seats in Y class, segment 1
NM1SHARMA/RAHUL MR    Name element — Passenger name
AP 9911234567         Contact phone number
TK TL                 Ticketing time limit
ER                    End and Retrieve (save PNR)
ET                    End Transaction (save and end)
IG                    Ignore (discard changes)
RT                    Retrieve PNR (current)
```

**PNR Retrieval:**
```
RT ABCDEF         Retrieve PNR by record locator
RT+9911234567     Retrieve PNR by phone number
RTLNAME/FNAME     Retrieve PNR by name
```

**Pricing:**
```
FXP               Price PNR (published fares)
FXP/R,UP          Price with upgrade
FXPN              Price with negotiated/private fares
FXB               Price and store fare (best price)
WPNCB             Price with best negotiated + published comparison
```

**Ticketing:**
```
TTP               Issue ticket (Ticket This PNR)
TTP/ET            Issue and end transaction
TTP/T1            Issue ticket for passenger 1 only
```

**Queue:**
```
QC1               Count items on Queue 1
QL1               List items on Queue 1
QR1               Remove from Queue 1
```

**Pre-ticket checklist (Amadeus 9-step):**
1. `FQN1/R,ALL` — Pull full fare rule
2. `FQN1/R,31` — Cat 31 (if any change context)
3. `FQN1/R,33` — Cat 33 (if any refund context)
4. Visual check: FBC Position 1 = booked class in PNR
5. `FQN1/R,15` — PCC authorised to sell?
6. `FQN1/R,35` — Private fare security correct?
7. `FQN1/R,5` — AP deadline not breached?
8. GST rate correct (Economy 5% / Premium 12%)?
9. GSTIN captured for corporate booking?

---

### GALILEO — CORE COMMANDS [MED confidence]

**Availability:**
```
A15NOVDELBOM      Availability DEL-BOM 15 Nov
A15NOVDELLHR*AI   Availability with Air India
```

**Fare Display:**
```
FD DEL LHR/D15NOV/CAI   Fare display with date and carrier
FD*#                     Display fare rules for fare on line #
FQP                      Price PNR
FQBB                     Display best buy fares
```

**PNR:**
```
N.SHARMA/RAHUL MR        Add passenger name
P.9911234567             Add phone number
T.TAW/                   Ticketing time limit
ER                        End and retrieve
EF                        End and file
```

**Ticketing:**
```
FQ                        Issue ticket
FQ*                       Re-display fare for ticketing
```

**Key difference from Amadeus:** Galileo uses different command structure. Format Finder (available in Galileo) is the authoritative source for Galileo-specific commands. Many Galileo commands are single-letter where Amadeus uses two or three letters.

**Known gap:** Galileo exchange/reissue commands are not comprehensively covered in this knowledge base. Use Galileo Format Finder or contact Travelport support.

---

### SABRE — CORE COMMANDS [MED confidence]

**Availability:**
```
15NOVDELBOM       Availability (date+route, no prefix)
15NOVDELLHR/AAI   Availability with carrier
```

**Fare Display:**
```
FQBB DEL LHR      Fare display DEL-LHR
WP                Price PNR
WPNC              Price with negotiated contract fares
WPNCB             Best buy with negotiated + published
WP¥PL             Price and store lowest fare
```

**Fare Rules:**
```
FQNC¥RALL         All rules for stored fare
WPNC¥R31          Cat 31 Voluntary Changes
WPNC¥R33          Cat 33 Voluntary Refunds
```

**PNR:**
```
1SHARMA/RAHUL MR          Name element
9-9911234567 H            Phone number (H = home)
7TAW/                     Ticketing time limit
E                         End transaction
ER                        End and retrieve
```

**Ticketing:**
```
W¥TKT             Issue ticket
W¥TKT¥ETR         Issue and end retrieve
```

**MPM Check:**
```
MPDEL-LON         Check MPM DEL to London
FLIFO             Flight information
```

**Known gap:** Sabre Red 360 fare-shopper entries are not fully covered. Sabre manual exchange/refund masks (the graphical screens) are not in this knowledge base — use Sabre Format Finder or Sabre Central for these.

---

## BOOK 3 — NDC & NEW-GEN PLATFORMS

### NDC (NEW DISTRIBUTION CAPABILITY)

**What NDC is:**
- IATA XML/JSON messaging standard for airlines to sell content directly via API
- NOT a GDS replacement — it is a complementary channel
- Airlines use NDC to offer richer content (ancillaries, bundles, personalised offers)
- Agents access NDC either via GDS NDC content, or direct airline NDC APIs

**NDC is NOT cryptic.** There are no cryptic terminal commands for NDC. NDC operates via API calls (HTTP/JSON or HTTP/XML). Any "NDC command" is an API integration, not a GDS entry.

**NDC Level terminology (IMPORTANT):**
- NDC Levels 1-4 were retired by IATA in 2022
- Do NOT say "NDC Level 3" — use IATA ARM (Airline Retailing Maturity) Index terminology

**NDC Message Flow:**
```
AirShopping → OfferPrice → OrderCreate → OrderRetrieve → OrderReshop → OrderChange → OrderCancel
```

| Message | Purpose |
|---|---|
| AirShopping | Search for available offers (replaces availability + pricing) |
| OfferPrice | Get detailed pricing for a selected offer |
| OrderCreate | Book/create the order (replaces PNR creation + ticketing) |
| OrderRetrieve | Read an existing order (replaces PNR retrieval) |
| OrderReshop | Re-price a modification (replaces re-pricing) |
| OrderChange | Modify an existing order (change, cancel segments) |
| OrderCancel | Cancel the order and initiate refund |

### GDS NDC HANDLING

**Amadeus NDC:**
- Amadeus offers NDC content via Amadeus Travel Platform (NDC-X)
- Airlines connect their NDC to Amadeus — agents access NDC offers alongside GDS fares
- Commands differ by airline and Amadeus configuration — no universal NDC cryptic
- IndiGo NDC via Amadeus: Live since January 2025 (India milestone)
- [VERIFY] Specific Amadeus NDC cryptic entries — not in knowledge base

**Sabre NDC:**
- Sabre offers NDC via Sabre Travel AI (formerly CPAM / NDC aggregator)
- Commands differ per airline — not universal cryptic
- [VERIFY] Sabre NDC-specific commands — not in knowledge base

**Travelport NDC:**
- Travelport offers NDC via Travelport+
- [VERIFY] Galileo/Travelport NDC-specific commands — not in knowledge base

### NEW-GEN PLATFORMS

**Farelogix (now SPRK / Accelya):**
- Airline retailing platform — not a GDS
- Used by airlines as an NDC offer management system
- Spark = SPRK (Accelya, ex-Farelogix) — this is an INFERENCE [VERIFY]
- Agents do not typically access Farelogix directly — airlines use it as a backend

**Amadeus Altea NDC:**
- Amadeus Altea is an airline departure control + reservations system
- Altea NDC: Airline connects via Altea to offer NDC content to agents
- Agent 360 = Singapore Airlines (SQ) agent portal built on Amadeus Altea NDC — this is the Singapore Airlines dedicated agent platform

**Agent 360 (Singapore Airlines):**
- Singapore Airlines dedicated agent portal
- Built on Amadeus Altea NDC
- Used by agencies to access SQ NDC content with richer ancillaries and bundles
- Not available to all agents — requires registration with Singapore Airlines

### INDIA NDC TIMELINE

| Date | Event |
|---|---|
| September 2024 | Air India (AI) goes live on NDC |
| October 2024 | Yatra becomes first Indian TMC to adopt NDC |
| January 2025 | IndiGo (6E) launches NDC via Amadeus |
| May 2026 | Lufthansa Group targets 75% NDC content |

### FBTW NDC POSITIONING

FlyByTheWay operates on:
- GDS (primary): For the majority of airline content
- Duffel NDC (current): API-first NDC aggregator — connects to multiple airlines' NDC
- Decision pending: Move to GDS + NDC hybrid or GDS-only for simplicity

**BSP vs NDC settlement:**
- GDS tickets settle via BSP India (weekly cycle)
- NDC orders settle differently per airline — not all NDC airlines settle via BSP
- [VERIFY] NDC settlement in India BSP context — confirm with IATA India and Duffel

---

## FARE FAMILIES — KEY AIRLINES (India-relevant)

### Air India (AI) — Star Alliance
| Cabin | Family | Refund | Change | Notes |
|---|---|---|---|---|
| Economy | Value | No | Fee | Most restrictive |
| Economy | Classic | Partial | Fee | Standard |
| Economy | Flex | Full | Free | Flexible |
| Economy | Full | Full | Free | No restrictions |
| Premium Economy | — | Partial | Fee | DEL-LHR/JFK routes |
| Business | Saver | Partial | Fee | |
| Business | Flex | Full | Free | |

**IMPORTANT — Air India Prohibited RBDs:**
- I, O, X, P classes are PROHIBITED for revenue passengers on Air India
- Booking AI in these classes triggers automatic TDS (Ticket Debit Memo) ADMs
- Block these RBDs in any booking engine used for AI content

### IndiGo (6E)
| Family | Refund | Change | Notes |
|---|---|---|---|
| Lite | No | No | No baggage |
| Saver | Partial | Fee | Standard economy |
| Flexi | Full | Free | Flexible |
| Corporate | Varies | Varies | Negotiated |

### Vistara (UK) — RETIRED
**⚠️ CRITICAL: Vistara merged into Air India in October 2024. DO NOT book on UK code. All Vistara segments are now under AI (Air India) code.**

### SpiceJet (SG)
**⚠️ OPERATIONAL RISK:** SpiceJet had significant grounding periods in 2024-2025. Flag as operational risk in IRROPS Scout. Reduced fleet, reliability concerns for corporate travel.

### Emirates (EK) — [HIGH confidence]
| Family | Refund | Change | Baggage |
|---|---|---|---|
| Saver | No | Fee | 30kg |
| Flex | Partial | Free | 35kg |
| Flex+ | Full | Free | 35kg+10kg |
| Business Saver | Partial | Fee | 40kg |
| Business Flex | Full | Free | 40kg |
| First Saver | Partial | Fee | 50kg |
| First Flex | Full | Free | 50kg |

### Qatar Airways (QR)
| Family | Refund | Change | Baggage |
|---|---|---|---|
| Economy Light | No | No | 23kg |
| Economy Classic | Partial | Fee | 23kg |
| Economy Comfort | Full | Fee | 23kg+10kg |
| Economy Flex | Full | Free | 23kg+10kg |
| Business Lite | Partial | Fee | 2×32kg |
| Business Classic | Full | Free | 2×32kg |
| First | Full | Free | 3×32kg |

---

## TICKETING RULES

### Ticket Number Structure
- 13-digit ticket number
- Digits 1-3: Airline accounting code (prefix)
  - 176 = Emirates (EK)
  - 098 = Qatar Airways (QR)
  - 555 = Etihad (EY)
  - 607 = Air India (AI)
  - 524 = IndiGo (6E)
  - 220 = Lufthansa (LH)
  - 001 = American Airlines (AA)
  - 006 = Delta (DL)
  - 016 = United (UA)
- Digits 4-7: Form code (document type)
- Digits 8-13: Serial number + check digit

### Coupon Status Codes
| Code | Status | Action |
|---|---|---|
| O | Open | Available for travel |
| F | Flown | Cannot be refunded or exchanged |
| V | Void | Voided same day — no coupon value |
| R | Refunded | Already refunded |
| E | Exchanged | Used in exchange |

### Void Window
- Void is ONLY available on the same day of ticket issuance, before BSP reporting cutoff
- After the BSP cutoff: must process as a refund (with applicable penalties)
- Zero exceptions — no late voids

### Refund Calculation
```
Refund = Fare paid – Cat 33 penalty – non-refundable YQ/YR per rule – taxes
Note: Statutory taxes (UDF/ADF/PSF) ALWAYS refunded regardless of fare type (DGCA 2026 mandate)
```

### EMD (Electronic Miscellaneous Document)
- **EMD-A (Associated):** Tied to a flight coupon — refund only, no residual transfer
- **EMD-S (Standalone):** Not tied to a flight — can be refunded or residual transferred to new EMD-S

---

## INDIA REGULATIONS ON TICKETING

### DGCA 2026 Rules (effective 26 March 2026)
- 48-hour look-in period for domestic flights (departure ≥ 7 days away)
- 48-hour look-in for international flights (departure ≥ 15 days away)
- Statutory taxes (UDF/ADF/PSF) ALWAYS refundable, even on non-refundable fares — no exceptions

### GST on Air Travel (effective 22 September 2025)
- Domestic Economy: 5% GST on base fare
- Domestic Business/First: 18% GST on base fare (revised from 12%)
- International Economy ex-India: 5% GST
- International Business/First ex-India: 18% GST
- SOTO (Sold Outside, Travel Outside India): Zero-rated
- Agent service fee: 18% GST (SAC code 998551)
- Statutory levies (UDF/ADF/PSF): GST exempt

### BSP Settlement
- Agent issues ticket in GDS → HOT file generated → IATA Billing Analysis Centre processes → Agent remits net amount → IATA settles with airlines
- BSP India billing: Weekly cycle (Monday-Sunday settlement)
- RHC (Risk of Holding Cash): Maximum outstanding cash an agent may hold
  - At 100% RHC: BSP cash collection is RESTRICTED
  - Use IATA EasyPay to bypass RHC (48-96h settlement, no RHC impact)
- Peak risk periods: Diwali · Christmas-New Year · Eid → pre-emptive mid-cycle remittance recommended

### ADM (Agency Debit Memo) — Most Common Triggers
1. **RBD mismatch:** Fare Basis Code Position 1 ≠ booked class in PNR — most common ADM trigger
2. **Air India prohibited class:** I/O/X/P booked for revenue passenger
3. **Void window missed:** Trying to void after BSP cutoff
4. **Ticketing without authorization:** Selling fare in PCC not authorised under Cat 15
5. **AP breach:** Ticketing after advance purchase deadline has passed

**ADM dispute window:** 15 days (IATA Resolution 850m) / 14 days (most carriers). Carrier must settle within 60 days.

---

## ALLIANCES & INTERLINE

### Star Alliance (26 members)
Air India (AI) is India's Star Alliance member.
Key India-relevant partners: LH (Lufthansa), LX (Swiss), TG (Thai), SQ (Singapore), EY (note: Etihad not in alliance but key India carrier)

### oneworld (15 members)
No Indian carrier currently in oneworld. Key India-route carriers: BA (British Airways), CX (Cathay Pacific), QR (Qatar — not oneworld), JL (Japan Airlines), QF (Qantas)

### SkyTeam (18 members)
Key India-route carriers: AF (Air France), KL (KLM), DL (Delta), KE (Korean Air)

### Interline vs Codeshare
- **Codeshare:** Marketing carrier sells seats on operating carrier's flight under its own flight number
- **Interline:** Agreement allowing through-ticketing and baggage transfer across two or more carriers on one ticket — requires IET (Interline E-Ticketing) link between carriers
- **Proration:** How interline revenue is shared between carriers — MITA (default, TPM-based), Proportional, or SPA (bilateral, best margin control)

---

## HAMAYA GDS RULE — NON-NEGOTIABLE

When answering any GDS question:
1. State the GDS (Amadeus / Galileo / Sabre)
2. Show the command in code block format
3. State confidence level [HIGH / MED / VERIFY]
4. Explain what the command does in plain English
5. State what to check in the response
6. If the entry is [VERIFY]: say "Confirm this in a training PCC or use [GDS] Help: `HE <entry>` in Amadeus / Format Finder in Galileo/Sabre"

If a command is not in this knowledge base: say "This entry is not in my knowledge base — please check [GDS name] Format Finder or contact [GDS] support."

*Source: HAMAYA_Knowledge_Base_GDS_NDC_Fares.md (Books 0-3) · HAMAYA.md Travel Systems Directive · Ingested: 2026-10-23*
