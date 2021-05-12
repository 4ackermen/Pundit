
![Logo](https://user-images.githubusercontent.com/32199592/118006127-a0c27000-b368-11eb-8864-20a3a233c9c2.png)

    
# Pundit

A Discord Bot for recruiting teams



[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)

[![Support Server](https://img.shields.io/discord/591914197219016707.svg?label=Discord&logo=Discord&colorB=7289da&style=for-the-badge)](https://discord.gg/gFgsKNq3)
## Features

**Task Submission**
- Handles submission from users
- Set submission templates
- Support for multiple languages

**Task Verification**
- Handles plagiarism using MOSS
- Flag checker
- Allows to run test cases

**Leaderboard**
- Manages public leaderboard 

**Statistics**
- Track a user's progress
## Tech Stack

Python, Docker, and the Discord API

  
## Demo

Add Pundit to your Discord server by clicking [here]()

## Installation

```bash
sudo apt install mysql-server
pip install mosspy
bash init.sh /path/to/dump.sql
git clone https://github.com/4ackermen/Pundit/
cd pundit
python3 start.py
```


Update the discord bot's token in `config.yaml`
Note: Written for discord.py==1.4.1

## Usage

```
- !help
```

  
## Documentation

### Task Validator

#### For Challenge Authors

Supported Challenge Types

- Flag Based
- Programming Based

This is the format that should be followed for creating a challenge.

TODO

- restrict a few systemcalls for c and asm tasks

#### tasks.yaml

```yaml
sanity:
  name: Sanity Check
  desc: Just the Sanity Check
  value: 100
  flageval: yes
  flag: flag{.*}

summer:
  name: The Summer
  desc: Prints the sum of number given
  value: 200
  flageval: no
  language: python
  allowed:
    - re
    - string
  maxlines: 0
  delimiter: !!str " "
  testcases:
    sample:
      input: "50 50\n"
      output: "100\n"
    input:
      - [100]
      - [100, 69]
      - [100, 10, 1]
    output:
      - [100]
      - [169]
      - [111]

swapper:
  name: Swapper
  desc: Sawps the case of the list of strings given
  value: 200
  flageval: no
  language: c
  flags:
    - "-Wall"
    - "-Werror=format-security"
    - "-fstack-protector-all"
  delimiter: !!str "\n"
  testcases:
    sample:
      input: "2\nbB\ncC\n"
      output: "Bb\nCc\n"
    input:
      - [1, aa]
      - [2, bB, cC]
      - [3, dd, ee, ff]
    output:
      - [AA]
      - [Bb, Cc]
      - [DD, EE, FF]
```

**Refer [tasks.yaml](./tasks.yaml) for more accurate instructions**

#### For Players

All the tasks must be zipped in the following structure

```
- tasks.zip
  - swapper/
    - swapper.py
  - summer/
    - summer.c
    - Makefile
  - sanity/
    - sanity.flag
    - sanity.txt
```

Make the zip file downloadable from the internet and give the link to pundit

Ex.
`!tasks submit https://bashupload.com/Nb-Kb/tasks.zip`

All the python files must take the testcase input from stdin and print the respective output to stdout.

The flag evaluated solutions should be named `task.flag` with the contents `flag{.*}` i.e, the respective flag.



## Authors

- Bommidi Jaswanth
- Suraj K Suresh
- Keshav Varma
- Akhil K G

  
## License

[MIT](https://choosealicense.com/licenses/mit/)