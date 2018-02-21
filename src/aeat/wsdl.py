BASE_ENS = 'https://www2.agenciatributaria.gob.es/ADUA/internet/es/aeat/dit/adu/aden/'

ADUANET_SERVICES = {
    # 'ens_fork': {
    #     'verbose_name': 'Servicio Solicitud Desvío ENS V5.0',
    #     'wsdl': f'{BASE_ENS}enswsv5/IE323V5.wsdl',
    #     'operation': 'IE323V5',
    #     'port_production': 'IE323V5',
    #     'port_test': 'IE323V5Pruebas',
    #     'service': 'IE323V5Service',
    # },
    # 'ens_modification': {
    #     'verbose_name': 'Servicio Modificación ENS V5.0',
    #     'wsdl': f'{BASE_ENS}enswsv5/IE313V5.wsdl',
    #     'operation': 'IE313V5',
    #     'port_production': 'IE313V5',
    #     'port_test': 'IE313V5Pruebas',
    #     'service': 'IE313V5Service',
    # },
    'ens_presentation': {
        'verbose_name': 'Servicio de Presentación ENS V5.0',
        'url_production': 'https://www1.agenciatributaria.gob.es/L/inwinvoc/es.aeat.dit.adu.aden.enswsv5.IE315V5SOAP',  # NOQA
        'url_test': 'https://www1.agenciatributaria.gob.es/L/inwinvoc/es.aeat.dit.adu.aden.enswsv5.IE315P5SOAP',  # NOQA
    },

    # 'exs_common': {
    #     'verbose_name': "Servicio de envío de EXIT Sumary (EXS) v2",
    #     'wsdl': 'https://www2.agenciatributaria.gob.es/ADUA/internet/es/aeat/dit/adu/adrx/ws/IE615V2.wsdl',  # NOQA
    #     'operation': 'IE615V2',
    #     'port_production': 'IE615V2',
    #     'port_test': 'IE615V2Pruebas',
    #     'service': 'IE615V2Service',
    # },
}
