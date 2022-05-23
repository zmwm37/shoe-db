import json
import sqlite3
import pandas as pd
from db_sql import DB


DATABASE = None

def load_json(file):
    d = open(file)
    data = json.load(d)

    return data


def get_db_conn(db_name, DATABASE=None):
    """ 
    gets connection to database
    """
    if not DATABASE:
        DATABASE = sqlite3.connect(db_name)
        return DATABASE
    else:
        return DATABASE


def create_links(user_shoes):
    '''
    Given a list of users and their shoes, create links between shoes
    '''
    shoe_links = []
    shoe_set = set()
    for user_dict in user_shoes:
        shoes = user_dict['shoes']
        shoe_ids = [k for d in shoes for k in d.keys()]
        
        for i, id in enumerate(shoe_ids):
            shoe_set.add(id)
            for other_id in shoe_ids:
                if id != other_id:
                    # all combinations used here for sql version, would only
                    # need permutations for graph
                    shoe_links.append((id, other_id))
    shoe_links = pd.DataFrame(shoe_links, columns = ['shoe_id1', 'shoe_id2'])
    shoe_links_agg = shoe_links.groupby(['shoe_id1', 'shoe_id2'], as_index = False).size()

                
    return pd.DataFrame(shoe_set, columns = ['shoe_id']), \
        shoe_links, \
        shoe_links_agg


def create_shoe_graph(shoes, shoe_links, db_info):
    '''
    Provided a list of shoes and shoe link tuples, create a Neo4j graph
    '''
    #uri, user, pwd = db_info
    #conn = db.Neo4jConnection(uri=uri, user=user, pwd=pwd)
    # TODO
    pass


def create_shoe_links_table():
    db = DB(get_db_conn('shoes.db', DATABASE))
    db.create_script()
    return {"message": "created"}


def load_shoe_links(shoe_links):
    db = DB(get_db_conn('shoes.db', DATABASE))
    db.load_links(shoe_links)
    db.conn.commit()
    return {'message': 'loaded'}
    

def create_shoe_recs(current_shoes):
    '''Provided current shoe id(s), return a sorted list of recomended shoes'''
    # TODO 
    rec_dict = {}
    db = DB(get_db_conn('shoes.db', DATABASE))
    for id in current_shoes:
        recs = db.get_rec(id)
        rec_dict[id] = recs
    return rec_dict


def create_static_recs():
    '''
    '''
    # TODO 
    pass
    
