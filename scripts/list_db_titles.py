import sqlite3

db=r"c:\Users\tuhin\OneDrive\Desktop\musicPlayer-django-main\db.sqlite3"
con=sqlite3.connect(db)
cur=con.cursor()
titles=['Hua Main Animal 320 Kbps','Leo - Trying','Post Malone - rockstar ft. 21 Savage 1']
for t in titles:
    cur.execute("select id,title,lyrics from App_song where title=?", (t,))
    rows=cur.fetchall()
    print(f"SEARCH_TITLE:{t} => {rows}")
# also print possible similar titles
for t in ['Hua Main','Leo - Trying','Post Malone - rockstar']:
    cur.execute("select id,title from App_song where title like ?", ('%'+t+'%',))
    rows=cur.fetchall()
    print(f"LIKE:{t} => {rows}")
con.close()
