# based on
# https://github.com/GeoNode/geoserver-restconfig
# https://github.com/geosolutions-it/geoserver-restconfig/blob/master/examples/postgislayers.py
# https://github.com/arthurdjn/geoserver-py
# more about ...
# https://docs.geoserver.org/latest/en/user/rest/workspaces.html
# https://docs.geoserver.org/latest/en/api/#1.0.0/layers.yaml
# https://github.com/gicait/geoserver-rest

from datetime import datetime
import pandas as pd
from geoserver.catalog import Catalog
import os
import cfg


def main():
    cat = Catalog(cfg.GSERVER_URL, cfg.GSERVER_USER, cfg.GSERVER_PASS, validate_ssl_certificate=False )

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
            s_native_name = resu.native_name
            if hasattr(resu, 'native_bbox'):
                s_native_srs = resu.native_bbox[4]
            else:
                s_native_srs = ''

        else:
            s_host = ''
            s_port = ''
            s_database = ''
            s_schema = ''
            s_user = ''
            s_dbtype = ''
            s_native_name = ''
            s_native_srs = ''

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
        res2.append(s_native_name)
        res2.append(s_user)
        res2.append(s_dbtype)
        res2.append(s_native_srs)

        res.append(res2.copy())

        print(f"{l_name}, "
              f"{l_title} , "
              f"{w_name} , ")

    df = pd.DataFrame(res,
                      columns=['l_name',
                               'l_title',
                               'l_projection',
                               'w_name',
                               'w_name_full',
                               's_name',
                               's_host',
                               's_port',
                               's_database',
                               's_schema',
                               's_native_name',
                               's_user',
                               's_dbtype',
                               's_native_srs']
                      )

    if os.path.isfile(cfg.FILE_CSV_NAME) and os.access(cfg.FILE_CSV_NAME, os.R_OK):
        # print("File exists and is readable")
        os.remove(cfg.FILE_CSV_NAME)
    df.to_csv(cfg.FILE_CSV_NAME)

    if os.path.isfile(cfg.FILE_XLS_NAME) and os.access(cfg.FILE_XLS_NAME, os.R_OK):
        os.remove(cfg.FILE_XLS_NAME)
    df.to_excel(cfg.FILE_XLS_NAME)


if __name__ == '__main__':
    time1 = datetime.now()
    print('Starting at :' + str(time1))
    main()



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
