###########################################################
#         _                       _                       #
#        | |                     (_)                      #
#   _ __ | |_ __ _ _ __ _ __ ___  _  __ _  __ _ _ __      #
#  | '_ \| __/ _` | '__| '_ ` _ \| |/ _` |/ _` | '_ \     #
#  | |_) | || (_| | |  | | | | | | | (_| | (_| | | | |    #
#  | .__/ \__\__,_|_|  |_| |_| |_|_|\__, |\__,_|_| |_|    #
#  | |                               __/ |                #
#  |_|                              |___/                 #
#                                                         #
# Copyright (C) 2019, Vilhelm Prytz <vilhelm@prytznet.se> #
# https://github.com/VilhelmPrytz/ptarmigan               #
#                                                         #
###########################################################

import mysql.connector

import json
import os.path

# read configuration
with open("config.json") as f:
    config = json.load(f)["mysql"]

def database_connection():
    try:
        cnx = mysql.connector.connect(user=config["username"], password=config["password"],
                              host=config["host"],
                              database=config["database"])
    except mysql.connector.Error as err:
        raise Exception(f"unable to communicate with database {err}")

    cursor = cnx.cursor()
    return cnx, cursor

def sql_query(query):
    """Performs specified SQL query on MySQL database
    
    arguments: query, SQL-query to be executed
    returns: dictionary, status key with boolean value and result key with string value
    """

    query_result = {"status": True}

    cnx, cursor = database_connection()

    try:
        query_result["result"] = cursor.execute(query)
    except Exception as err:
        query_result["status"] = False
        query_result["result"] = str(err)

        return query_result

    try:
        query_result["result"] = cursor.fetchall()
    except Exception:
        if not query_result["result"]:
            query_result["result"] = None

    cnx.commit()
    cursor.close()
    cnx.cursor()

    return query_result