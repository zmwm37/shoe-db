from os import path

def to_json_list(cursor):
    results = cursor.fetchall()
    headers = [d[0] for d in cursor.description]
    return [dict(zip(headers, row)) for row in results]

class DB:
    def __init__(self, connection):
        self.conn = connection
    

    def execute_script(self, script_file):
        with open(script_file, "r") as script:
            c = self.conn.cursor()
            # Only using executescript for running a series of SQL commands.
            c.executescript(script.read())
            self.conn.commit()


    def create_script(self):
        """
        Calls the schema/create.sql file
        """
        script_file = path.join("schema", "create.sql")
        if not path.exists(script_file):
            raise InspError("Create Script not found")
        self.execute_script(script_file)


    def load_links(self, shoe_links):
        '''
        Load shoe link and weights into database
        '''
        cur = self.conn.cursor()

        insert_query = '''
            INSERT INTO shoe_links (
                shoe_id1, 
                shoe_id2,
                weight)
            VALUES (?, ? , ?)
        '''
        for _, row in shoe_links.iterrows():
            cur.execute(insert_query, 
                (row['shoe_id1'], row['shoe_id2'], row['size']))
    

    def check_link(self, shoe_id1, shoe_id2):
        '''
        Checks if link already exists in table, return boolean
        '''
        cur = self.conn.cursor()
        check_query = '''
            SELECT * from shoe_links
            WHERE (shoe_id1 = ? AND shoe_id2 = ?)
                OR (shoe_id1 = ? AND shoe_id2 = ?);
        '''
        cur.execute(check_query, [shoe_id1, shoe_id2, shoe_id2, shoe_id1])

        return len(to_json_list(cur)) > 0

    
    def add_weight(self, shoe_id1, shoe_id2):
        '''
        Add to shoe pair weight if present, otherwise create new shoe pair
        '''
        cur = self.conn.cursor()
        if self.check_link(shoe_id1, shoe_id2):
            add_query = '''
                UPDATE shoe_links
                weight = weight + 1
                WHERE (shoe_id1 = ? AND shoe_id2 = ?)
                    OR (shoe_id1 = ? AND shoe_id2 = ?);
            '''
            cur.exeute(add_query, [shoe_id1, shoe_id2, shoe_id1, shoe_id2])
        else:
            add_query = '''
                INSERT INTO shoe_links (
                    shoe_id1, 
                    shoe_id2,
                    weight
                ) VALUES (?, ?, 1)
            '''
            cur.exeucte(add_query, [min(shoe_id1, shoe_id2), max(shoe_id1, shoe_id2)])
        
        self.conn.commit()


    def delete_weight(self, shoe_id1, shoe_id2):
        '''
        Remove shoe pair weight, triggered by user deleting 
        '''
        # TODO 
        pass


    def get_rec(self, shoe_id):
        '''
        '''
        cur = self.conn.cursor()
        shoe_query = '''
            SELECT *, RANK() OVER(ORDER BY weight DESC) as rank
            FROM (SELECT shoe_id2 as shoe_id, weight FROM shoe_links
                WHERE shoe_id1 = ?
                UNION
                SELECT shoe_id1 as shoe_id, weight FROM shoe_links
                WHERE shoe_id2 = ?) as a
            ORDER BY weight DESC;
        '''
        cur.execute(shoe_query, (shoe_id, shoe_id))
        results = to_json_list(cur)
        return results
        
            