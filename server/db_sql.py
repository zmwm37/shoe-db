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
        '''
        cur = self.conn.cursor()

        insert_query = '''
            INSERT INTO shoe_links (
                shoe_id1, 
                shoe_id2,
                weight)
            VALUES (?, ? , ?)
        '''
        for i, row in shoe_links.iterrows():
            cur.execute(insert_query, 
                (row['shoe_id1'], row['shoe_id2'], row['size']))
    

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
        
            