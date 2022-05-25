import server

def format_results(shoe_rec, shoe_info):
    '''
    Takes output of shoe_rec and formats
    '''
    rec_shoe_info = shoe_info[shoe_rec['shoe_id']]
    print(f"{shoe_rec['rank']} ({shoe_rec['weight']} matches) - {rec_shoe_info['brand']} {rec_shoe_info['model']}")


def test_users_5():
    '''
    Return recommendations for users_5.json input.
    '''
    users = server.load_json('../data/users_5.json')
    shoes, shoe_links, sla = server.create_links(users)
    server.create_shoe_links_table()
    server.load_shoe_links(sla)
    for i in range(1, 8):
        print(f'Test for shoe id {i}')
        print(server.create_shoe_recs([i]))


def test_users_20(shoe_id=None, test_static = False):
    '''
    Return formatted recommendations for users_20.json input.
    '''
    users = server.load_json('../data/users_20.json')
    shoe_info = server.load_json('../data/shoe_info.json')[0]
    shoes, shoe_links, sla = server.create_links(users)
    server.create_shoe_links_table()
    server.load_shoe_links(sla)
    if shoe_id:
        input_shoe = shoe_info[str(shoe_id)]
        print(f"RECOMMENDATION FOR ~~~ {input_shoe['brand']}: {input_shoe['model']} ~~~")
        print('-------------')
        shoe_recs = server.create_shoe_recs([shoe_id])[shoe_id]
        for shoe in shoe_recs:
            format_results(shoe, shoe_info)
        print('-------------')
    else:
        for i in range(1, 11):
            input_shoe = shoe_info[str(i)]
            print(f"RECOMMENDATION FOR ~~~ {input_shoe['brand']}: {input_shoe['model']} ~~~")
            print('-------------')
            shoe_recs = server.create_shoe_recs([i])[i]
            for shoe in shoe_recs:
                format_results(shoe, shoe_info)
            print('-------------')
    
    if test_static:
        print("STATIC DICTIONARY OF ALL SHOE RECS")
        print(server.create_static_recs(shoes))


