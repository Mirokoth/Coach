import asyncio
import os
import time
from datetime import datetime, timedelta

import challonge

from config import config

# Test tournaments
# TODO: Override automatically, with config, or with gsheets later
tournNames = {
    "Test_Tourno": {},
    "Test_Tourno2": {},
    "Test_Tourno3": {}
}

# Grab the latest copy of a tournament's match list and compare it to our previous copy
def diff(coach, tournName, server_list, matchList):

    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    loop = asyncio.get_event_loop()
    challonge.set_credentials(config.CHAL_USER, config.CHAL_API)

    # Pull down the latest list of matches in a specified challonge tournament
    newMatchList = challonge.matches.index(tournName)

    # Create a local copy of matches if it doesn't exist
    if len(matchList) == 0:
        # Assign match list
        matchList = challonge.matches.index(tournName)
        print('No local match list to compare to yet, populating..')
        # Skip as we have nothing to compare to
        return matchList
        # matchList = newMatchList

    change = False
    # Check each match in the latest tournament
    for newMatch in newMatchList:
        # Compare the latest match list against our current list
        for match in matchList:
            # Compare match ID's
            if match['identifier'] == newMatch['identifier']:
                if 'None' in str(newMatch['winner-id']):
                    if (newMatch['player1-id'] != match['player1-id'] or
                     newMatch['player2-id'] != match['player2-id']):
                        if ('None' not in str(newMatch['player1-id']) and
                            'None' not in str(newMatch['player2-id'])):


                            tournament = challonge.tournaments.show(newMatch['tournament-id'])
                            player1 = challonge.participants.show(tournament['name'], newMatch['player1-id'])
                            player2 = participant = challonge.participants.show(tournament['name'], newMatch['player2-id'])
                            # cTime sets the amount of minutes a team has to show up for a match
                            cTime = datetime.now() + timedelta(minutes=30)

                            newMatchString = ('Match beginning: ```\n{} vs. {}\n\n'
                            'All players please report to tournament rooms by '
                            '{:%H:%M}.\n\nIf there are any issue please seek a LAG'
                            ' staff member.```'.format(player1['name'], player2['name'], cTime))

                            print('Found match beginning, sending to coach..')
                            coach.loop.create_task(coach.forward_message(coach.server, newMatchString))

                elif ('None' not in str(newMatch['winner-id']) and
                        newMatch['winner-id'] != match['winner-id']):

                    # Assigns the final score to the player id for winner/loser
                    # Player1 will be score[0] and Player2 score[1]
                    score = newMatch['scores-csv'].split('-', 2)
                    if newMatch['winner-id'] == newMatch['player1-id']:
                        winScore = score[0]
                        loseScore = score[1]
                    else:
                        winScore = score[1]
                        loseScore = score[0]

                    tournament = challonge.tournaments.show(newMatch['tournament-id'])
                    winner = challonge.participants.show(tournament['name'], newMatch['winner-id'])
                    loser = participant = challonge.participants.show(tournament['name'], newMatch['loser-id'])
                    change = True
                    # Logs each win for testing purposes
                    with open(DIRECTORY + '\\win_log\\' + tournament['name'] + " - " +
                                match['identifier'] + " - " + time.strftime('%H-%M') + ".txt", 'a+') as txt:
                                txt.write(str(newMatch))
                                txt.close()

                    matchWinStr = ('**{}** match has been won:\n```'
                            '\n{} vs. {}\n\n{} beat {}\n'
                            'with a final score of {} to {}\n\n'
                            'Ladder details can be found {}```'.format(tournament['name'],
                             winner['name'], loser['name'], winner['name'], loser['name'],
                              winScore, loseScore, tournament['full-challonge-url']))

                    print('Found match win, sending to coach..')
                    coach.loop.create_task(coach.forward_message(coach.server, matchWinStr))


    if change == True:
        print("Found a change!")
        # Return new match list
        return newMatchList
    else:
        # Return previous match list
        return matchList


'''
Background task that will check Challonge tournaments
for updates
'''
# Poll Challonge
class Poller():

    def __init__(self, coach):
        self.coach = coach
        self.loop = asyncio.get_event_loop()

    # Background loop - change sleep time to configure run frequency
    async def background_scan(self):
        while not self.coach.is_closed:
            await asyncio.sleep(config.CHAL_POLL_FREQUENCY)
            print('{} - Performing background task to scan tournaments'.format(time.strftime('%H:%M:%S')))
            for tournament in tournNames:
                print('Checking ' + tournament + '..')
                tournNames[tournament] = diff(self.coach, str(tournament), self.coach.servers, tournNames[tournament])
            print('{} - Background tasks to scan tournaments - Complete'.format(time.strftime('%H:%M:%S')))
