import sqlite3


class FavoriteList:

    def __init__(self):
        self.conn = sqlite3.connect("usersql.db")
        create_table = """ CREATE TABLE IF NOT EXISTS favorites (
                                        username varchar,
                                        movieid INT,
                                        primary key (username, movieid)
                                        ); """
        cursor = self.conn.cursor()
        cursor.execute(create_table)

    def add_new_movie(self, username, movie_id):
        """Add a movie to user's favorites

        Parameters
        ----------
            username: str
            movie_id: int, movie's id
        """

        cursor = self.conn.cursor()
        sql = ''' INSERT INTO favorites(username, movieid)
                VALUES(?,?) '''

        try:
            cursor.execute(sql, (username, movie_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print("fail to add to list", e.args[0])

    def fetch_favorites(self, username):
        """Fetch all user's favorites

        Parameters
        ----------
            username: str

        Returns
        -------
            list of int,
                return a list of user's favorite movies' ids
                example: [101. 24. 122]

        """

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM favorites WHERE username=?", (username,))

        rows = cursor.fetchall();
        result = []
        for element in rows:
            result.append(element[1])
        return result

    def delete_favorite(self, username, movie_id):

        sql = "DELETE FROM favorites WHERE username=? AND movieid=?"
        cursor = self.conn.cursor()
        cursor.execute(sql, (username, movie_id))
        self.conn.commit()


# favorite_list = FavoriteList()
# favorite_list.add_new_movie("brandon", 234)
# favorite_list.add_new_movie("brandon", 235)
# favorite_list.delete_favorite("brandon", 234)
# favorite_list.add_new_movie("brandon", 237)
# a = favorite_list.fetch_favorites("brandon")
# print(a)
