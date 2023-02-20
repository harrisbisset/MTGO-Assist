import sqlite3
import sys
import json
import ast

#gets data from database to be displayed on table
def openData():
    userConnection = sqlite3.connect("./database/mtgoAssist.db")
    cursor = userConnection.cursor()
    try:
        matches = cursor.execute("SELECT * FROM matches ORDER BY matchID DESC limit 20;").fetchall()
        
        results = {}

        for matchTuple in matches:
            results[matchTuple[0]] = [{}]
            for data in matchTuple:
                if isinstance(data, int) == False:
                    data = json.loads(data)
                    results[matchTuple[0]][0][list(data.keys())[0]] = data[list(data.keys())[0]]

        print(json.dumps(results))
    except:
        pass
    finally:
        cursor.close()
        userConnection.close()



#gets user averages
def getUserData():
    userConnection = sqlite3.connect("./database/mtgoAssist.db")
    cursor = userConnection.cursor()

    matches = cursor.execute("SELECT winner FROM matches;").fetchall()
    print(matches)
    results = {}

    for num, match in enumerate(matches):
        results[num] = match[0]
        print(match[0])

        # print(json.dumps(results)
    print(results)
    print(type(results ))

    cursor.close()
    userConnection.close()

print(getUserData())

# if __name__ == "main":
#     pass
# else:
#     if sys.argv[1] == 'loaded':
#         openData()
#     if sys.argv[1] == 'profile':
#         getUserData()


test = """[('{"winner": ["Corzalan", "Corzalan"]}',), ('{"winner": ["sc00nes", "-Sire", "sc00nes"]}',), ('{"winner": ["-Sire", "cbouz", "NA"]}',), ('{"winner": ["lindoso01", "lindoso01"]}',), ('{"winner": ["-Sire", "callowaysmith1", "-Sire"]}',), ('{"winner": ["Cesta", "Cesta"]}',), ('{"winner": ["Brivenix", "NA", "NA"]}',), ('{"winner": ["Magic4ever_MTGO", "Magic4ever_MTGO"]}',), ('{"winner": ["Pacto_das_Guildas", "Pacto_das_Guildas"]}',), ('{"winner": ["-Sire", "NA", "-Sire"]}',), ('{"winner": ["-Sire", "-Sire"]}',), ('{"winner": ["CaligulaFanBoi", "CaligulaFanBoi"]}',), ('{"winner": ["-Sire", "-Sire"]}',), ('{"winner": ["Foresterf", "Foresterf"]}',), ('{"winner": ["-Sire", "-Sire"]}',), ('{"winner": ["NA", "NA", "PauperFeito"]}',), ('{"winner": ["-Sire", "-Sire"]}',), ('{"winner": ["-Sire", "-Sire"]}',), ('{"winner": ["-Sire", "bergamo83", "-Sire"]}',), ('{"winner": ["ResponsiblyStupid", "ResponsiblyStupid"]}',), ('{"winner": ["lindoso01"]}',), ('{"winner": ["-Sire", "-Sire"]}',), ('{"winner": ["Beicodegeia", "Beicodegeia"]}',), ('{"winner": ["Arsmith8", "-Sire", "Arsmith8"]}',), ('{"winner": ["Corzalan", "Corzalan"]}',), ('{"winner": ["sc00nes", "-Sire", "sc00nes"]}',), ('{"winner": ["-Sire", "cbouz", "NA"]}',), ('{"winner": ["lindoso01", "lindoso01"]}',), ('{"winner": ["-Sire", "callowaysmith1", "-Sire"]}',), ('{"winner": ["Cesta", "Cesta"]}',), ('{"winner": ["Brivenix", "NA", "NA"]}',), ('{"winner": ["Magic4ever_MTGO", "Magic4ever_MTGO"]}',), ('{"winner": ["Pacto_das_Guildas", "Pacto_das_Guildas"]}',), ('{"winner": ["-Sire", "NA", "-Sire"]}',), ('{"winner": ["-Sire", "-Sire"]}',), ('{"winner": ["CaligulaFanBoi", "CaligulaFanBoi"]}',), ('{"winner": ["-Sire", "-Sire"]}',), ('{"winner": ["Foresterf", "Foresterf"]}',), ('{"winner": ["-Sire", "-Sire"]}',), ('{"winner": ["NA", "NA", "PauperFeito"]}',), ('{"winner": ["-Sire", "-Sire"]}',), ('{"winner": ["-Sire", "-Sire"]}',), ('{"winner": ["-Sire", "bergamo83", "-Sire"]}',), ('{"winner": ["ResponsiblyStupid", "ResponsiblyStupid"]}',), ('{"winner": ["lindoso01"]}',), ('{"winner": ["-Sire", "-Sire"]}',), ('{"winner": ["Beicodegeia", "Beicodegeia"]}',), ('{"winner": ["Arsmith8", "-Sire", "Arsmith8"]}',), ('{"winner": ["Hoarse_Duck", "Hoarse_Duck"]}',)]"""
