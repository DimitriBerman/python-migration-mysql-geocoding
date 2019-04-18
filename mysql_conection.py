import mysql.connector as mysql
import soup
import unicodedata

def get_mysql_connection(mysql_config):
    return mysql.connect(**mysql_config)

def fetchall_query(mysql_config, query):
    cnx = get_mysql_connection(mysql_config)
    cursor = cnx.cursor()
    cursor.execute(query)       
    
    records = cursor.fetchall()

    cnx.close() 
    return records

def execute_query(mysql_config, query):#, data):
    cnx = get_mysql_connection(mysql_config)
    cursor = cnx.cursor()

    cursor.execute(query)#, data)       
    
    cnx.commit()
    cnx.close() 

def get_user_metas(mysql_config):
    userMetaQuery = 'SELECT user_id, meta_key, meta_value \
                    FROM wp_usermeta \
                    WHERE 	meta_key IN ("user_direccion", "user_zona", "user_ubicacion", "user_cod_postal", "user_latitud", "user_longitud") \
                        AND meta_value IS NOT NULL \
                        AND meta_value <> \'\' \
                    GROUP BY 	user_id, 	meta_key, 	meta_value'# LIMIT 0,8'
    records = fetchall_query(mysql_config, userMetaQuery)
    userMetas = []
    userMeta = {}
    isDiffUser = True
    lastUserId = -1
    for r in records:
        user_id = r[0]
        meta_key = r[1]
        meta_value = r[2]
        
        isDiffUser = lastUserId <> user_id
        
        if isDiffUser:
            userMeta = {}
            userMeta["user_id"] = user_id
        
        isString = isinstance(meta_value, basestring)
        
        if isString:
            meta_value = unicodedata.normalize("NFKD", meta_value).encode('ascii', 'ignore')

        if meta_value <> '':
            userMeta[meta_key] = meta_value
                
        if isDiffUser:
            userMetas.append(userMeta)
        
        lastUserId = user_id
    return userMetas

def insert_coordinates_usermeta(mysql_config, user_metas):
    insert_userMetaQuery = "INSERT INTO wp_usermeta (user_id,meta_key,meta_value) VALUES "
    isFirst = True

    if len(user_metas) <= 0:
        print("nothing to insert")
        return

    for um in user_metas:
        if isFirst is False:
            insert_userMetaQuery += ", "
        
        insert_userMetaQuery += "(%s,'user_latitud',%s),(%s,'user_longitud',%s)" % (um["user_id"],um["latitude"],um["user_id"],um["longitude"])
        
        if isFirst:
            isFirst = False;
            
    insert_userMetaQuery += ";"

    print(insert_userMetaQuery) 

    execute_query(mysql_config, insert_userMetaQuery)