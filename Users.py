import sqlite3


class User:

    def __init__(self):
        self.conn = sqlite3.connect("usersql.db")
        create_table = """ CREATE TABLE IF NOT EXISTS users (
                                        username varchar PRIMARY KEY,
                                        age varchar,
                                        language varchar,
                                        lastmovie varchar
                                    ); """
        cursor = self.conn.cursor()
        cursor.execute(create_table)

    def add_new_user(self, username, age, language="en-US"):
        """Add a new user to the database
            Skip if user already exists

        Parameters
        ----------
            username: str,
                user's username

            age: str
                whether user is above 18. You can put whatever you want. e.g The actual age, yes/no, true/false.
                But just to make sure this is consist with backend functionality

            language: str
                user's language. You can change to regular english e.g "English", "Chinese", or language code as right now
                Again, just make sure this is consist with backend functionality

        Example
        -------
            user.add_new_user("Stephen", "true", "en-US")
        """
        cursor = self.conn.cursor()
        user_info = (username, age, language)
        sql = ''' INSERT INTO users(username,age,language)
              VALUES(?,?,?) '''
        if self.fetch_user_info(username) is None:
            cursor.execute(sql, user_info)
            self.conn.commit()

    def fetch_user_info(self, username):
        """Fetch users information stored in the database

        Parameters
        ----------
            username: str,
                user's username

        Returns
        -------
            tuple,
                A tuple of users information that contains (username, age, language, last_movie)
                If user does not exist, returns None.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))

        rows = cursor.fetchall()
        if len(rows) > 0:
            return rows[0]
        return None

    def delete_user(self, username):
        """Delete a user

        Parameters
        ----------
            username: str
                user's username
        """
        sql = "DELETE FROM users WHERE username=?"
        cursor = self.conn.cursor()
        cursor.execute(sql, (username,))
        self.conn.commit()

    def update_last_movie(self, username, last_movie):
        """Update user's lastest state

        Parameters
        ----------
            username: str
                user's username
            last_movie: str
                user's last state. Can be "popular", [genre], or [movie id] as string
        """
        sql = ''' UPDATE users
                  SET lastmovie=?
                  WHERE username=? '''
        cursor = self.conn.cursor()

        try:
            cursor.execute(sql, (last_movie, username))
            self.conn.commit()
        except sqlite3.Error as e:
            print("fail to update last movie", e.args[0])


# ==============================================
# Example inputs
# user = User()
# user.add_new_user("brandon", "yes", "en-US")
# print(user.fetch_user_info("brandons"))
# user.delete_user("brandon")
# print(userinfo)
# user.update_last_movie("brandon", "action")