BASE_ENS = 'https://www2.agenciatributaria.gob.es/ADUA/internet/es/aeat/dit/adu/aden/'

ADUANET_SERVICES = {
    'ens_fork': {
        'verbose_name': 'Servicio Solicitud Desvío ENS V5.0',
        'wsdl': f'{BASE_ENS}enswsv5/IE323V5.wsdl',
        'operation': 'IE323V5',
        'port_production': 'IE323V5',
        'port_test': 'IE323V5Pruebas',
        'service': 'IE323V5Service',
        'signed': True,
    },
    'ens_modification': {
        'verbose_name': 'Servicio Modificación ENS V5.0',
        'wsdl': f'{BASE_ENS}enswsv5/IE313V5.wsdl',
        'operation': 'IE313V5',
        'port_production': 'IE313V5',
        'port_test': 'IE313V5Pruebas',
        'service': 'IE313V5Service',
        'signed': True,
    },
    'ens_presentation': {
        'verbose_name': 'Servicio de Presentación ENS V5.0',
        'wsdl': f'{BASE_ENS}enswsv5/IE315V5.wsdl',
        'operation': 'IE315V5',
        'port_production': 'IE315V5',
        'port_test': 'IE315V5Pruebas',
        'service': 'IE315V5Service',
        'signed': True,
    },
    'ens_query': {
        'verbose_name': "Servicio Consulta de ENS's",
        'wsdl': f'{BASE_ENS}ensws/ConsENSV3.wsdl',
        'operation': 'ConsENSV3',
        'port_production': 'ConsENSV3',
        'port_test': 'ConsENSV3Pruebas',
        'service': 'ConsENSV3Service',
        'signed': False,
    },

    'exs_common': {
        'verbose_name': "Servicio de envío de EXIT Sumary (EXS) v1",
        'wsdl': 'https://www2.agenciatributaria.gob.es/ADUA/internet/es/aeat/dit/adu/adrx/ws/IE615V1.wsdl',  # NOQA
        'operation': 'IE615V1',
        'port_production': 'IE615V1',
        'port_test': 'IE615V1Pruebas',
        'service': 'IE615V1Service',
        'signed': True,
    },
}
