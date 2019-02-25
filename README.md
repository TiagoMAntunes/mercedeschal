# CLI Code Challenge for Mercedes-Benz.io

*Made by:* Tiago Antunes

*Email:* tiago.melo.antunes@tecnico.ulisboa.pt

*University:* Instituto Superior Técnico

*2nd year student*

## What could be improved?
- Possible multi-threaded implementation
- Data abstraction (creating some ADT's that could mask the implementation for simpler reading)
- Improve the HTML parsing to be faster (instead of downloading the whole page, slowly fetch the page until we get the desired zone to analyze. This improvement would be noticeable in the BitBucket service, since the page is really heavy)
- Improve flag parsing (mechanism is a bit rudimentary, could be optimized)
- Implement command design pattern for command addition
- Implement status bonus command
- Implement data restore for CSV and TXT formats

## Decisions made while implementing
- Python for speed of development and is easier to understand, while also being easy to improve some logic (funtion assignments, lambda functions)
- HTML parsing and validation. Easy to implement, BeautifulSoup helps a lot by making it easy to parse the whole html
- Flag mechanism receives what flags to pay attention and validates those flags, making it easier to validate data
- Config file contains the HTML keys to validate and its respective content
- A service will only be displayed as online if the status website is on, and the HTML parsing is validated. Any error will automatically make it be considered as *offline*

## Problems encountered during construction of program
- Difficult to simulate some of the errors shown (lack of knowledge too)
- No idea on how to calculate mttf