from datetime import datetime
import pandas as pd
from geoserver.catalog import Catalog

import cfg


def main():
    cat = Catalog(cfg.GSERVER_URL, cfg.GSERVER_USER, cfg.GSERVER_PASS, validate_ssl_certificate=False )

    # print("пробуем достать workspaces")
    # wrksps = cat.get_workspaces()
    # # Достать все Stores которые смотрят в PG
    # pg_stores = [s.name for s in cat.get_stores()
    #              if s.resource_type == 'dataStore' and s.connection_parameters.get("dbtype") == "postgis"]
    # res = []
    # res2 = []
    # for i in range(len(wrksps)):
    #     # print(i, wrksps[i])
    #     stors = cat.get_stores(wrksps[i])
    #     # stors = cat.get_stores()
    #     wrksps_name = wrksps[i].name
    #     res2.clear()
    #
    #     if not len(stors):
    #         res2.append(wrksps_name)
    #
    #     for j in range(len(stors)):
    #         # res2.clear()
    #         res2.append(wrksps_name)
    #         res2.append(stors[j].name)
    #         res2.append(stors[j].type)
    #         res2.append(stors[j].connection_parameters['host'])
    #         res2.append(stors[j].connection_parameters['port'])
    #         res2.append(stors[j].connection_parameters['database'])
    #         res2.append(stors[j].connection_parameters['schema'])
    #         res2.append(stors[j].connection_parameters['user'])
    #         res2.append(stors[j].connection_parameters['dbtype'])
    #         res2.append(stors[j].connection_parameters['max connections'])
    #     res.append(res2.copy())
    #
    # df = pd.DataFrame(res, columns=['wrksps_name', 'store_name', 'type', 'host', 'port', 'database', 'schema', 'user', 'dbtype', 'max connections'])
    # df.to_csv(cfg.FILE_CSV_NAME)


    resurses = cat.get_resources()
    res = []
    res2 = []
    for resu in resurses:
        res2.clear()

        l_name = resu.name
        l_title = resu.title
        l_projection = resu.projection
        w_name = resu.workspace.name
        w_name_full = f"{w_name}:{l_name}"
        s_name = resu.store.name if resu.store else ''
        if hasattr(resu.store, 'connection_parameters'): # отрабатываем подключения через PostgreSQL
            s_host = resu.store.connection_parameters['host']
            s_port = resu.store.connection_parameters['port']
            s_database = resu.store.connection_parameters['database']
            s_schema = resu.store.connection_parameters['schema']
            s_user = resu.store.connection_parameters['user']
            s_dbtype = resu.store.connection_parameters['dbtype']
        else:
            s_host = ''
            s_port = ''
            s_database = ''
            s_schema = ''
            s_user = ''
            s_dbtype = ''

        res2.append(l_name)
        res2.append(l_title)
        res2.append(l_projection)
        res2.append(w_name)
        res2.append(w_name_full)
        res2.append(s_name)
        res2.append(s_host)
        res2.append(s_port)
        res2.append(s_database)
        res2.append(s_schema)
        res2.append(s_user)
        res2.append(s_dbtype)
        res.append(res2.copy())

        print(f"{l_name}, "
              f"{l_title} , "
              f"{w_name} , ")

    df = pd.DataFrame(res,
                      columns=['r_name', 'r_title', 'r_projection', 'w_name', 'w_name_full','s_name', 's_host', 's_port', 's_database', 's_schema',
                               's_user', 's_dbtype'])

    df.to_csv(cfg.FILE_CSV_NAME)
    df.to_excel(cfg.FILE_XLS_NAME)


if __name__ == '__main__':
    time1 = datetime.now()
    print('Starting at :' + str(time1))
    main()

