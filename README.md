# Competitive Pokemon Dataset Analysis

_Data Wrangling and Exploratory Data Analysis_

CSMODEL machine project by the Froggers

## Outline

1.  **Introduction**
    1.  Raw Data
        1.  Pokemon Showdown - Battle logs ([Showdown Scraper](https://github.com/jrgo7/showdown-scraper))
            1.  Ties and Forfeit
        2.  [Bulbagarden - Gen 5 Pokemon base stats](https://bulbapedia.bulbagarden.net/wiki/List_of_Pokémon_by_base_stats_in_Generations_II-V)
        3.  Smogon - Gen 5 OU usage on [2015](https://www.smogon.com/stats/2015-01/gen5ou-0.txt) and [2025](https://www.smogon.com/stats/2025-01/gen5ou-0.txt)
2.  **Research Questions (EDAs)**
    1.  What is the distribution of base stats among teams, and are they correlated?
    2.  Do people generally pick a certain Pokemon more often than the rest?
    3.  Do higher-skilled players end battles quicker?
    4.  What types are usually run on competitive Pokemon teams?
3.  **Dataset Preprocessing**
    1.  Showdown ([`battlelogs_to_csv.py`](battlelogs_to_csv.py))
        1.  Removing duplicate players
        2.  Turn Count
        3.  Lead Pokemon
    2.  Smogon - Pokemon Usage
    3.  [Bulbagarden - Base Stats](phase-1-base-stats.ipynb)
    4.  Types (one hot encoding)
4.  **Exploratory Data Analysis**
    1.  Base stats (histograms, box plot, correlation plot)
        1.  per team (averaged)
        2.  per lead **Pokemon**
    2.  Frequencies
        1.  Lead Pokemon frequency (histogram)
        2.  Gen5OU usage (goodness of fit)
    3.  Elo and turncount (histogram, t-test, correlation)
        1.  Stalling techniques causing outliers in turn count
    4.  Types
        1. Histogram
