import server

def test_users_5():
    users = server.load_json('../data/users_5.json')
    shoes, shoe_links, sla = server.create_links(users)
    server.create_shoe_links_table()
    server.load_shoe_links(sla)
    for i in range(1, 8):
        print(f'Test for shoe id {i}')
        print(server.create_shoe_recs([i]))


def test_users_20():
    users = server.load_json('../data/users_20.json')
    shoes, shoe_links, sla = server.create_links(users)
    server.create_shoe_links_table()
    server.load_shoe_links(sla)
    for i in range(1, 11):
        print(f'Test for shoe id {i}')
        print(server.create_shoe_recs([i]))

