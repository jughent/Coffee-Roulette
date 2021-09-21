## Getting Started

### Prerequisites
- python3

### Installation 
- Clone the repo
```
git clone https://github.com/jughent/Coffee-Roulette.git
```

### Preparing Your Files
There are two (.csv) files in which you will need (listed below). You need to save these files in the same location as your repo in order for python to know where to look.
1. A list of all the names of the people participating in the coffee roulette. The list needs to be in 1 column with a *header* as shown below:

  | HeaderName       | 
  | ---------   | 
  | Name1       | 
  | Name2       |  
  | Name3       |  
  | Name4       |  
  | Namen       | 


2. A list of historical matches. This is a list of previous coffee roulette pairings that will be used as a means to eliminate duplicate pairings. The list needs to be in 2 columns with a *header* as shown below:
   
   **NOTE**: If you have no historical data you will still need to pass through a blank list, as python will be expecting 2 lists as input!

  | HeaderName           | HeaderName |
  | ---------      | --------      |
  | Name1          |  Name1        |
  | Name2          |  Name2        |
  | Name3          |  Name3        |
  | Name4          |  Name3        |
  | Namen          |  Namen        |


## Running the program
-  Run the following in your terminal to generate a list of unique pairings

   **NOTE**: Ensure you follow this order when running the command:
   python3 [./python script] [.csv file containing List of names] [.csv file containing List of old pairs] [no. of weeks you want to generate]

```
python3 ./Coffee_Roulette.py NamesList.csv ListOfHistoricalPairs.csv 22
```

## Output
- The generated unique list of pairings will be saved as 'Coffee_Roulette_Pairings.csv' located in the same folder as your repo.
- Each week will have the header "Week [number of weeks], Total matches: [number of matches]" dividing each week
