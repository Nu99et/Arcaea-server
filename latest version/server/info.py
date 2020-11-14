import sqlite3
import server.arcworld
import json


def int2b(x):
    # int与布尔值转换
    if x is None or x == 0:
        return False
    else:
        return True


def get_recent_score(c, user_id):
    # 得到用户最近一次的成绩，返回列表
    c.execute('''select * from user where user_id = :x''', {'x': user_id})
    x = c.fetchone()
    if x is not None:
        if x[11] is not None:
            c.execute('''select best_clear_type from best_score where user_id=:u and song_id=:s and difficulty=:d''', {
                'u': user_id, 's': x[11], 'd': x[12]})
            y = c.fetchone()
            if y is not None:
                best_clear_type = y[0]
            else:
                best_clear_type = x[21]

            return [{
                "rating": x[22],
                "modifier": x[19],
                "time_played": x[20],
                "health": x[18],
                "best_clear_type": best_clear_type,
                "clear_type": x[21],
                "miss_count": x[17],
                "near_count": x[16],
                "perfect_count": x[15],
                "shiny_perfect_count": x[14],
                "score": x[13],
                "difficulty": x[12],
                "song_id": x[11]
            }]
    return []


def get_user_character(c, user_id):
    # 得到用户拥有的角色列表，返回列表
    c.execute('''select * from user_char where user_id = :user_id''',
              {'user_id': user_id})
    x = c.fetchall()
    if x != []:
        s = []
        for i in x:
            char_name = ''
            c.execute(
                '''select name from character where character_id = :x''', {'x': i[1]})
            y = c.fetchone()
            if y is not None:
                char_name = y[0]
            
            if char_name == "Yume":
                s.append({
                    "is_uncapped_override": int2b(i[14]),
                    "is_uncapped": int2b(i[13]),
                    "uncap_cores": [],
                    "char_type": i[12],
                    "skill_id_uncap": i[11],
                    "skill_requires_uncap": int2b(i[10]),
                    "skill_unlock_level": i[9],
                    "skill_id": i[8],
                    "overdrive": i[7],
                    "prog": i[6],
                    "frag": i[5],
                    "level_exp": i[4],
                    "exp": i[3],
                    "level": i[2],
                    "name": char_name,
                    "character_id": i[1],
                    "voice": [0, 1, 2, 3, 100, 1000, 1001]
                })
            else:
                s.append({
                    "is_uncapped_override": int2b(i[14]),
                    "is_uncapped": int2b(i[13]),
                    "uncap_cores": [],
                    "char_type": i[12],
                    "skill_id_uncap": i[11],
                    "skill_requires_uncap": int2b(i[10]),
                    "skill_unlock_level": i[9],
                    "skill_id": i[8],
                    "overdrive": i[7],
                    "prog": i[6],
                    "frag": i[5],
                    "level_exp": i[4],
                    "exp": i[3],
                    "level": i[2],
                    "name": char_name,
                    "character_id": i[1]
                })

        return s
    else:
        return []


def get_user_friend(c, user_id):
    # 得到用户的朋友列表，返回列表
    c.execute('''select user_id_other from friend where user_id_me = :user_id''', {
              'user_id': user_id})
    x = c.fetchall()
    s = []
    if x != [] and x[0][0] is not None:

        for i in x:
            c.execute('''select exists(select * from friend where user_id_me = :x and user_id_other = :y)''',
                      {'x': i[0], 'y': user_id})
            if c.fetchone() == (1,):
                is_mutual = True
            else:
                is_mutual = False

            c.execute('''select * from user where user_id = :x''', {'x': i[0]})
            y = c.fetchone()
            if y is not None:
                s.append({
                    "is_mutual": is_mutual,
                    "is_char_uncapped_override": int2b(y[9]),
                    "is_char_uncapped": int2b(y[8]),
                    "is_skill_sealed": int2b(y[7]),
                    "rating": y[5],
                    "join_date": int(y[3]),
                    "character": y[6],
                    "recent_score": get_recent_score(c, i[0]),
                    "name": y[1],
                    "user_id": i[0]
                })

    return s


def get_value_0(c, user_id):
    # 构造value id=0的数据，返回字典
    c.execute('''select * from user where user_id = :x''', {'x': user_id})
    x = c.fetchone()
    r = {}
    if x is not None:
        user_character = get_user_character(c, user_id)
        characters = []
        for i in user_character:
            characters.append(i['character_id'])

        r = {"is_aprilfools": False,
             "curr_available_maps": [],
             "character_stats": user_character,
             "friends": get_user_friend(c, user_id),
             "settings": {
                 "favorite_character": x[23],
                 "is_hide_rating": int2b(x[10]),
                 "max_stamina_notification_enabled": int2b(x[24])
             },
             "user_id": user_id,
             "name": x[1],
             "user_code": x[4],
             "display_name": x[1],
             "ticket": x[26],
             "character": x[6],
             "is_locked_name_duplicate": False,
             "is_skill_sealed": int2b(x[7]),
             "current_map": x[25],
             "prog_boost": 0,
             "next_fragstam_ts": -1,
             "max_stamina_ts": 1586274871917,
             "stamina": 12,
             "world_unlocks": [],
             "world_songs": ["babaroque", "shadesoflight", "kanagawa", "lucifer", "anokumene", "ignotus", "rabbitintheblackroom", "qualia", "redandblue", "bookmaker", "darakunosono", "espebranch", "blacklotus", "givemeanightmare", "vividtheory", "onefr", "gekka", "vexaria3", "infinityheaven3", "fairytale3", "goodtek3", "suomi", "rugie", "faintlight", "harutopia", "goodtek", "dreaminattraction", "syro", "diode", "freefall", "grimheart", "blaster", "cyberneciacatharsis", "monochromeprincess", "revixy", "vector", "supernova", "nhelv", "purgatorium3", "dement3", "crossover", "guardina", "axiumcrisis", "worldvanquisher", "sheriruth", "pragmatism", "gloryroad", "etherstrike", "corpssansorganes", "lostdesire", "blrink", "essenceoftwilight", "lapis"],
             "singles": get_user_singles(c, user_id), # ["dataerror", "yourvoiceso", "crosssoul", "impurebird", "auxesia", "modelista", "yozakurafubuki", "surrender", "metallicpunisher", "carminescythe", "bethere", "callmyname", "fallensquare", "dropdead", "alexandrite", "astraltale", "phantasia", "empireofwinter", "libertas", "dottodot", "dreadnought", "mirzam", "heavenlycaress", "filament", "avantraze", "battlenoone", "saikyostronger", "izana", "einherjar", "laqryma", "amygdata", "altale", "feelssoright", "scarletcage", "teriqma", "mahoroba", "badtek", "maliciousmischance", "buchigireberserker", "galaxyfriends", "buchigireberserker2", "xeraphinite"],
             "packs": get_user_packs(c, user_id), # ["vs", "extend", "dynamix", "prelude", "core", "yugamu", "omatsuri", "zettai", "mirai", "shiawase", "chunithm", "nijuusei", "groovecoaster", "rei", "tonesphere" ,"lanota"],
             "characters": characters,
             "cores": [],
             "recent_score": get_recent_score(c, user_id),
             "max_friend": 50,
             "rating": x[5],
             "join_date": int(x[3])
             }

    return r

def take_memories(user_id, price):
    conn = sqlite3.connect('./database/arcaea_database.db')
    c = conn.cursor()

    c.execute('''SELECT memories FROM user WHERE user_id = :user_id''', {'user_id': user_id})
    orig_mmrs = c.fetchone()[0]

    c.execute('UPDATE user SET memories = {0} WHERE user_id = :user_id'.format(str(orig_mmrs - price)), {'user_id': user_id})
    conn.commit()
    conn.close()

    return

def get_user_singles(c, user_id):
    # 返回用户的单曲持有信息 类型为列表
    c.execute('''SELECT single_id FROM purchase_single WHERE user_id = :user_id''', {'user_id': user_id})
    x = c.fetchall()
    r = []

    for p in x:
        r.append(p[0])

    return r    

def get_user_packs(c, user_id):
    # 返回用户的曲包持有信息 类型为列表
    c.execute('''SELECT pack_id FROM purchase WHERE user_id = :user_id''', {'user_id': user_id})
    x = c.fetchall()
    r = []

    for p in x:
        r.append(p[0])

    return r

def add_single(user_id, single_id):
    # 为用户添加单曲
    conn = sqlite3.connect('./database/arcaea_database.db')
    c = conn.cursor()

    c.execute('''INSERT INTO purchase_single VALUES (:user_id, :single_id)''', {'user_id': user_id, 'single_id': single_id})
    conn.commit()
    conn.close()
    
    return

def add_song_pack(user_id, pack_id):
    # 为用户添加曲包
    conn = sqlite3.connect('./database/arcaea_database.db')
    c = conn.cursor()
    
    c.execute('''INSERT INTO purchase VALUES (:user_id, :pack_id)''', {'user_id': user_id, 'pack_id': pack_id})
    conn.commit()
    conn.close()

    return

def get_song_pack_info_by_id(pack_id):
    with open('./database/songpacks.json') as f:
        obj = json.loads(f.read())
        f.close()
    
    r = {}
    for pack in obj['packs']:
        if pack['name'] == pack_id:
            r = pack
            break

    return r

def get_single_info_by_id(single_id):
    with open('./database/singles.json') as f:
        obj = json.loads(f.read())
        f.close()
    
    r = {}
    for single in obj['singles']:
        if single['name'] == single_id:
            r = single
            break
    
    return r

def get_song_pack_infos():
    # 返回 songpacks.json 曲包信息 类型为列表
    with open('./database/songpacks.json') as f:
        obj = json.loads(f.read())
        f.close()
    
    r = []
    for pack in obj['packs']:
        p = {
            "name": pack['name'],
            "items": [],
            "price": pack['price'],
            "orig_price": pack['orig_price'],
        }

        if 'discount_from' in pack and 'discount_to' in pack:
            p['discount_from'] = pack['discount_from']
            p['discount_to'] = pack['discount_to']

        for item in pack['items']:
            p['items'].append({
                "id": item['id'],
                "type": item['type'],
                "is_available": item['is_available']
            })
        
        r.append(p)
    
    return r

def get_single_infos():
    # 返回 singles.json 单曲信息 类型为列表
    with open('./database/singles.json') as f:
        obj = json.loads(f.read())
        f.close()
    
    r = []
    for single in obj['singles']:
        s = {
            "name": single['name'],
            "items": [],
            "price": single['price'],
            "orig_price": single['orig_price']
        }

        if 'discount_from' in single and 'discount_to' in single:
            s['discount_from'] = single['discount_from']
            s['discount_to'] = single['discount_to']

        for item in single['items']:
            s['items'].append({
                "id": item['id'],
                "type": item['type'],
                "is_available": item['is_available']
            })
        
        r.append(s)
    
    return r


def arc_aggregate_small(user_id):
    # 返回用户数据
    conn = sqlite3.connect('./database/arcaea_database.db')
    c = conn.cursor()
    r = {"success": True,
         "value": [{
             "id": 0,
             "value": get_value_0(c, user_id)
         }]}

    conn.commit()
    conn.close()
    return r


def arc_aggregate_big(user_id):
    # 返回用户数据和地图歌曲信息
    # 因为没有整理地图和曲包数据（不需要世界模式），所以直接复制了

    conn = sqlite3.connect('./database/arcaea_database.db')
    c = conn.cursor()
    r = {"success": True,
         "value": [{
             "id": 0,
             "value": get_value_0(c, user_id)
         }, {
             "id": 1,
             "value": get_song_pack_infos()
         }, {
             "id": 2,
             "value": {}
         }, {
             "id": 3,
             "value": {
                 "max_stamina": 12,
                 "stamina_recover_tick": 1800000,
                 "core_exp": 250,
                 "curr_ts": 1599547606825,
                 "level_steps": [{
                     "level": 1,
                     "level_exp": 0
                 }, {
                     "level": 2,
                     "level_exp": 50
                 }, {
                     "level": 3,
                     "level_exp": 100
                 }, {
                     "level": 4,
                     "level_exp": 150
                 }, {
                     "level": 5,
                     "level_exp": 200
                 }, {
                     "level": 6,
                     "level_exp": 300
                 }, {
                     "level": 7,
                     "level_exp": 450
                 }, {
                     "level": 8,
                     "level_exp": 650
                 }, {
                     "level": 9,
                     "level_exp": 900
                 }, {
                     "level": 10,
                     "level_exp": 1200
                 }, {
                     "level": 11,
                     "level_exp": 1600
                 }, {
                     "level": 12,
                     "level_exp": 2100
                 }, {
                     "level": 13,
                     "level_exp": 2700
                 }, {
                     "level": 14,
                     "level_exp": 3400
                 }, {
                     "level": 15,
                     "level_exp": 4200
                 }, {
                     "level": 16,
                     "level_exp": 5100
                 }, {
                     "level": 17,
                     "level_exp": 6100
                 }, {
                     "level": 18,
                     "level_exp": 7200
                 }, {
                     "level": 19,
                     "level_exp": 8500
                 }, {
                     "level": 20,
                     "level_exp": 10000
                 }, {
                     "level": 21,
                     "level_exp": 11500
                 }, {
                     "level": 22,
                     "level_exp": 13000
                 }, {
                     "level": 23,
                     "level_exp": 14500
                 }, {
                     "level": 24,
                     "level_exp": 16000
                 }, {
                     "level": 25,
                     "level_exp": 17500
                 }, {
                     "level": 26,
                     "level_exp": 19000
                 }, {
                     "level": 27,
                     "level_exp": 20500
                 }, {
                     "level": 28,
                     "level_exp": 22000
                 }, {
                     "level": 29,
                     "level_exp": 23500
                 }, {
                     "level": 30,
                     "level_exp": 25000
                 }],
                 "world_ranking_enabled": False,
                 "is_byd_chapter_unlocked": True
             }
         }, {
             "id": 4,
             "value": []
         }, {
             "id": 5,
             "value": {
                 "current_map": server.arcworld.get_current_map(user_id),
                 "user_id": user_id,
                 "maps": server.arcworld.get_world_all(user_id)
             }
         }
         ]}

    conn.commit()
    conn.close()
    return r
