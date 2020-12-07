# sharpy-starter-bot
Starter bot using  [sharpy-sc2](https://github.com/DrInfy/sharpy-sc2/wiki) and [python-sc2](https://github.com/BurnySc2/python-sc2) for playing [Starcraft 2](https://starcraft2.com/en-us/) using [sc2 api](https://github.com/Blizzard/s2client-api).

## To download
`git clone --recursive https://github.com/DrInfy/sharpy-starter-bot`

## To run the bot vs ingame ai
`python run_custom.py -m EverDreamLE -p1 protossbot -p2 ai`

`python run_custom.py -m SubmarineLE -p1 zergbot -p2 ai`

`python run_custom.py -m GoldenWallLE -p1 terranbot -p2 ai`

Replays and logs will be in `games` folder.

## To publish the bots for ladder
to publish the bot(s) as ladder ready versions:
`python ladder_zip.py [botname]`

To publish the bot(s) as stand-alone executable:
`python ladder_zip.py [botname] -e`

published bot(s) will be in `publish folder

## To get coding assistance in PyCharm
Mark sharpy-sc2 and sharpy-sc2/python directories as source roots.

## Documentation 
Refer to [sharpy documentation](https://github.com/DrInfy/sharpy-sc2/wiki) for features
