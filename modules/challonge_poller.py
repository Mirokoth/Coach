import time
# import modules.tournament_diff as tournament_diff
import asyncio
import os
import time

import challonge

from config import config
# from commands.mid_man import mid_man

# Test tournaments
# TODO: Override automatically, with config, or with gsheets later
tournNames = {
    "Test_Tourno": {},
    "Test_Tourno2": {}
}

# Grab the latest copy of a tournament's match list and compare it to our previous copy
def diff(coach, tournName, server_list, matchList):

    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    loop = asyncio.get_event_loop()
    challonge.set_credentials(config.CHAL_USER, config.CHAL_API)

    # Pull down the latest list of matches in a specified challonge tournament
    newMatchList = challonge.matches.index(tournName)
    # print(newMatchList)

    # if len(matchList) == 0:
    #     print("This match list has a length of 0")

    # Create a local copy of matches if it doesn't exist
    if len(matchList) == 0:
        # Assign match list
        matchList = challonge.matches.index(tournName)
        print('No local match list to compare to yet, populating..')
        # Skip as we have nothing to compare to
        return matchList
        # matchList = newMatchList


    change = False
    announcements = []
    # Check each match in the latest tournament
    for newMatch in newMatchList:
        # Compare the latest match list against our current list
        for match in matchList:
            # Compare match ID's
            if match['identifier'] == newMatch['identifier']:
                # print('Matched game {}'.format(match['identifier']))
                if 'None' in str(newMatch['winner-id']):
                    # print('-- 1 --')
                    # print('-- previous match | player 1 id: ' + match['player1-id'])
                    # print('-- previous match | player 2 id: ' + match['player2-id'])
                    # print('-- new match | player 1 id: ' + newMatch['player1-id'])
                    # print('-- new match | player 2 id: ' + newMatch['player2-id'])
                    if (newMatch['player1-id'] != match['player1-id'] or
                     newMatch['player2-id'] != match['player2-id']):
                        if ('None' not in str(newMatch['player1-id']) and
                            'None' not in str(newMatch['player2-id'])):
                            tournament = challonge.tournaments.show(newMatch['tournament-id'])
                            player1 = challonge.participants.show(tournament['name'], newMatch['player1-id'])
                            player2 = participant = challonge.participants.show(tournament['name'], newMatch['player2-id'])

                            newMatchString = ('Match beginning: ```\n{} VS. {}\n\n'
                            'All players please report to tournament rooms within '
                            '30 minutes.\nIf there are any issue please seek a LAG'
                            ' staff member.```'.format(player1['name'], player2['name']))

                            # announcements.append(newMatchString)
                            print('Found match beginning, sending to coach..')
                            coach.forward_message(coach.server, newMatchString)
                            # coach.loop.create_task(mid_man(newMatchString, server_list))

                elif ('None' not in str(newMatch['winner-id']) and
                        newMatch['winner-id'] != match['winner-id']):
                    # print('-- 2 --')
                    # print('-- previous match | winner id: ' + match['winner-id'])
                    # print('-- new match | winner id: ' + newMatch['winner-id'])

                    tournament = challonge.tournaments.show(newMatch['tournament-id'])
                    winner = challonge.participants.show(tournament['name'], newMatch['winner-id'])
                    loser = participant = challonge.participants.show(tournament['name'], newMatch['loser-id'])
                    change = True

                    matchWinStr = ('Match has been won!\n```Tournament: {}'
                            '\nWinner : {}\nLoser : {}```'.format(tournament['name'],
                             winner['name'], loser['name']))

                    # print(matchWinStr)

                    # announcements.append(newMatchString)
                    print('Found match win, sending to coach..')
                    coach.forward_message(coach.server, matchWinStr)
                    # loop.create_task(mid_man(matchWinStr, server_list))

                # else:
                    # print('-- 3 --')
                    # print('-- previous match | winner id: ' + match['winner-id'])
                    # print('-- new match | winner id: ' + newMatch['winner-id'])

            # Cannot match ID's
            # else:
            #     print('No match')

    # Found a change
    if change == True:
        print("Found a change!")
        # Return new match list
        return newMatchList
    # Return previous match list
    return matchList

    # print('Found a change: ' + tournName)
    # print('Printing local cache..')
    # print(str(tournNames))

    # # Found a change
    # if change == True:
    #
    #     # Save new match list
    #     tournNames[tournName] = newMatchList
    #     # self.tournamentCache[config.CHAL_POLL_TOURN_ID] =
    #
    # # Return message to be sent
    # return announcements

'''
Background task that will check Challonge tournaments
for updates
'''
# Poll Challonge
class Poller():

    def __init__(self, coach):
        self.coach = coach
        self.loop = asyncio.get_event_loop()

    # loop for definition call
    # loop = asyncio.get_event_loop()

    # Background loop - change sleep time to configure run frequency
    async def background_scan(self):
        while not self.coach.is_closed:
            await asyncio.sleep(config.CHAL_POLL_FREQUENCY)
            print('{} - Performing background task to scan tournaments'.format(time.strftime('%H:%M:%S')))
            for tournament in tournNames:
                # tournNames[str(i)] = diff(str(i), self.coach.servers, tournNames[str(i)])
                # Diff
                print('')
                print('Checking ' + tournament + '..')
                tournNames[tournament] = diff(self.coach, str(tournament), self.coach.servers, tournNames[tournament])
                # announcements = str(self.coach, diff(str(i), self.coach.servers, tournNames[str(i)]))
                # announcements = str(diff(str(i), self.coach.servers, tournNames[str(i)]))
                # self.loop.create_task(self.coach.forward_message(self.coach.server, announcements))
                # # loop.create_task(mid_man(diff(str(i), self.coach.servers, tournNames[str(i)])))
                # announcements = diff(str(i), self.coach.servers, tournNames[str(i)])
                # # print('Announcements: ' + str(announcements))
                # # self.loop.create_task(self.coach.forward_message(self.coach.server, announcements))
                # # self.loop.create_task(self.coach.forward_message('202327470052081665', 'Kosta'))
            print('{} - Background tasks to scan tournaments - Complete'.format(time.strftime('%H:%M:%S')))

# loop.create_task(background_scan())
