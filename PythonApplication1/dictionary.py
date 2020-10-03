import mysql.connector

con = mysql.connector.connect(
user = "ardit700_student",
password = "ardit700_student",
host = "108.167.140.122",
database = "ardit700_pm1database"
)
cursor = con.cursor()

def translate(word):
    query = cursor.execute("SELECT Definition FROM Dictionary WHERE Expression = '%s'" % word)
    results = cursor.fetchall()
    if results:
        return results
    else:
        query = cursor.execute("SELECT Definition FROM Dictionary WHERE Expression = '%s'" % word.lower())
        results = cursor.fetchall()
        if results:
            return results
        else:
            query = cursor.execute("SELECT Expression FROM Dictionary WHERE Expression LIKE '%{}%'".format(word.lower()))
            results = cursor.fetchall()
            if results:
                print("Did you mean '%s'?" % (results[0][0]))
                while True:
                    yn = input("Y/N? ").lower()
                    if yn == 'y' or yn == 'n':
                        break 
                if yn == 'y':
                    query = cursor.execute("SELECT Definition FROM Dictionary WHERE Expression = '%s'" % results[0][0])
                    results = cursor.fetchall()
                    return results
                else:
                    return []
            else:
                return []

while True:
    word = input("Word: ")
    if word == "\end":
        break
    definitions = translate(word)
    if len(definitions) == 0:
        print("word does not exist")
    elif len(definitions) == 1:
        print(definitions[0][0])
    else:
        i = 1
        for d in definitions:
            print("%s: %s" % (i, d[0]))
            i = i + 1
