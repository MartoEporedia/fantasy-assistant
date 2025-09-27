# Fantasy Assistant âš½ðŸ“Š  

[![License](https://img.shields.io/badge/license-TBD-lightgrey.svg)](LICENSE)  
![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)  
![Last Commit](https://img.shields.io/github/last-commit/martoeporedia/fantasy-assistant)  
![Issues](https://img.shields.io/github/issues/martoeporedia/fantasy-assistant)  

**Fantasy Assistant** is a data-driven fantasy football (Serie A) assistant.  
It helps managers during **auctions** (including sealed-bid), **roster management**, **trades**, and **weekly lineups** using stats, historical data, community insights, and AI-powered predictions.  

---

## âœ¨ Features

### Auctions
- Support for different auction types:
  - **Classic** (open bids)
  - **Snake draft**
  - **Hybrid** (sealed-bid + open)
  - **Sealed-bid** (special focus)
- Suggested bid ranges based on player value, market trends, and historical data.
- Simulations of possible outcomes (if you win/lose a player).
- Dynamic budget advisor to optimize strategy.

### Post-Auction Roster
- Dashboard with role balance score.
- Strengths and weaknesses analysis.
- Trade suggestions and repair auction strategy.

### Season Management
- Weekly lineup recommendations based on stats, fixtures, and injuries.
- Notifications about unavailable players and price changes.
- Comparison with public rosters and community intelligence.

---

## ðŸ—ï¸ Architecture (MVP)

```mermaid
flowchart TD

    subgraph Client["ðŸ“± Frontend (React Native + Expo)"]
        A1[Home]
        A2[Auction Module]
        A3[Roster Dashboard]
        A4[Notifications]
    end

    subgraph Backend["ðŸŒ Backend (FastAPI / Node.js)"]
        B1[/API: /players/]
        B2[/API: /advice/bid/]
        B3[/API: /simulations/bid/]
        B4[/API: /advice/roster/]
        B5[/API: /community/trends/]
        B6[/Auth & Notifications/]
    end

    subgraph DB["ðŸ—„ï¸ Database (PostgreSQL - Supabase)"]
        D1[(Players)]
        D2[(Users)]
        D3[(Bids)]
        D4[(Rosters)]
        D5[(Community Data)]
    end

    subgraph AI["ðŸ¤– AI/ML Layer"]
        M1[Value for Money model]
        M2[Bid Range Advisor]
        M3[Roster Balance Scorer]
        M4[LLM Explainability]
    end

    %% Connections
    A1 --> A2
    A2 -->|Player stats & suggestions| B1
    A2 -->|Range suggestions| B2
    A2 -->|Bid simulations| B3
    A3 -->|Roster evaluation| B4
    A2 -->|Auction trends| B5
    A4 -->|Push| B6

    B1 --> D1
    B2 --> M2
    B3 --> M1
    B4 --> M3
    B5 --> D5
    B6 --> D2
    B6 --> D3
    B6 --> D4

    M2 --> D3
    M3 --> D4
    M1 --> D1
    M4 --> A2
    M4 --> A3
```

---

## ðŸ”„ User Flows

### ðŸŽ¯ Sealed-bid Auction
```mermaid
flowchart TD
    U1[Start auction - Sealed-bid] --> U2[Select player]
    U2 --> U3[View AI range & stats]
    U3 --> U4[Insert bid]
    U4 --> U5[Save bid]
    U5 --> U6[Bids summary screen]
    U6 --> U7[Simulate scenarios win/lose]
    U7 --> U8[Wait for reveal]
    U8 --> U9[Post-reveal results]
    U9 --> U10[Update roster & budget]
    U10 --> U11[Dashboard with balance & AI advice]
```

### ðŸ“¢ Classic Auction
```mermaid
flowchart TD
    C1[Start auction - Classic] --> C2[Player announced]
    C2 --> C3[View AI suggested range]
    C3 --> C4[User decides: Bid or Pass]
    C4 -->|Bid| C5[Track live price vs AI value]
    C4 -->|Pass| C6[Skip to next player]
    C5 --> C7[Final winner selected]
    C7 --> C8[Update roster & budget]
    C8 --> C9[Dashboard with advice]
```

### ðŸ Snake Draft
```mermaid
flowchart TD
    S1[Start draft - Snake] --> S2[User priority list]
    S2 --> S3[AI predicts opponent picks]
    S3 --> S4[User turn to pick]
    S4 --> S5[Confirm selection]
    S5 --> S6[Update roster & budget]
    S6 --> S7[Next round prediction]
    S7 --> S8[Repeat until draft complete]
    S8 --> S9[Final roster dashboard]
```

### ðŸ”€ Hybrid Auction
```mermaid
flowchart TD
    H1[Start auction - Hybrid] --> H2[Insert sealed bid]
    H2 --> H3[Top 2 bids selected]
    H3 --> H4[Final open bid stage]
    H4 --> H5[AI suggests safe range]
    H5 --> H6[User decides to raise or fold]
    H6 --> H7[Winner determined]
    H7 --> H8[Update roster & budget]
    H8 --> H9[Dashboard with AI insights]
```

---

### ðŸ”„ Comparative User Flow
```mermaid
flowchart TD

    A0[Start Auction] --> A1[Classic Auction]
    A0 --> A2[Sealed-bid Auction]
    A0 --> A3[Snake Draft]
    A0 --> A4[Hybrid Auction]

    A1 --> A1_4[Winner determined] --> AF[ðŸŸï¸ Final Roster Dashboard]
    A2 --> A2_4[Reveal results] --> AF
    A3 --> A3_4[Confirm choice] --> AF
    A4 --> A4_4[Winner determined] --> AF
```

---

## ðŸ“Š User Flow â€“ Post-Auction Dashboard
```mermaid
flowchart TD

    D0[ðŸŸï¸ Final Roster Dashboard] --> D1[AI Roster Evaluation]
    D1 --> D2[Strengths & Weaknesses Analysis]
    D2 --> D3[Trade Suggestions]
    D2 --> D4[Repair Auction Strategy]

    D0 --> D5[Weekly Lineup Advisor]
    D5 --> D6[Check injuries & suspensions]
    D5 --> D7[AI suggests best XI formation]
    D7 --> D8[Confirm lineup]

    D0 --> D9[Live Notifications]
    D9 --> D10[Last-minute injuries]
    D9 --> D11[Price changes]
    D9 --> D12[Matchday reminders]

    D0 --> D13[Community Intelligence]
    D13 --> D14[Compare with other rosters]
    D13 --> D15[Average auction prices & trends]
    D13 --> D16[Shared trade scenarios]
```

---

## ðŸš€ Roadmap
- [ ] MVP: Auction Assistant (bid ranges, sealed-bid simulator, budget advisor)  
- [ ] Post-auction dashboard with role balance and insights  
- [ ] Weekly lineup recommender  
- [ ] Trade module with roster comparisons  
- [ ] Community intelligence (share and learn from real auctions)  

---

## ðŸ“– License
TBD â€“ choose a license depending on distribution model.  

---

## ðŸ™Œ Contributing
Contributions are welcome!  
Feel free to open issues and pull requests.  

---

## ðŸŸï¸ Goal
To build the **first complete assistant for fantasy football managers**, combining **data, AI, and practical insights** into one app.  