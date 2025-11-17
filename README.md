# voter_analytics
A Django web application to explore and analyze registered voter data. Users can filter voters by demographics, party affiliation, voter score, and election participation, view individual voter details, and generate interactive charts visualizing trends such as birth year distribution, party affiliation, and election participation rates.

> **Note:** This repository includes models, views, and templates to demonstrate the app's functionality, but does not include project-level configuration or sensitive backend code.


---

**Author:** Anna LaPrade (alaprade@bu.edu)  
**Date:** October 2025 

---

## Overview

`voter_analytics` is a Django web application for analyzing voter registration and election participation data. The app allows users to:

- Browse and search registered voters.
- Filter voters by party affiliation, birth year, voter score, and election participation.
- View detailed voter information.
- Generate interactive visual analytics (histograms, pie charts, bar charts) using Plotly.


---

## Features

### Voter List

- Paginated list of voters (100 per page).
- Filters for party, birth year range, voter score, and participation in recent elections.
- Clickable rows to view detailed voter information.

### Voter Detail View

- Displays complete information for a single voter:
  - Identification and contact info
  - Birth and registration dates
  - Party affiliation and precinct number
  - Election participation history
  - Voter score
- Provides a Google Maps link for the voter's address.

### Graph Analytics

- Interactive visualizations powered by Plotly:
  - **Birth Year Distribution** – histogram of voters’ birth years.
  - **Party Affiliation** – pie chart of voters by party.
  - **Election Participation** – bar charts showing participation in recent elections.
- Filters apply to graphs to focus on specific subsets of voters.

---

## Usage (For Visitors)
> **Note:** This repository includes models, views, and templates to demonstrate the app's functionality, but does not include project-level configuration or sensitive backend code.

### Browse Voters
- Go to the **Voter List** page (`/voters/`) to see all registered voters.
- Click a voter to view details like address, party, election history, and voter score.

### Explore Graphs
- Go to the **Graphs** page (`/graphs/`) to see interactive charts:
  - Birth Year Distribution
  - Party Affiliation
  - Election Participation
- Use the filter form to narrow results by party, birth year, voter score, or election participation.



