BASE_ENS = 'https://www2.agenciatributaria.gob.es/ADUA/internet/es/aeat/dit/adu/aden/'

ADUANET_SERVICES = {
    'ens_fork': {
        'verbose_name': 'Servicio Solicitud Desvío ENS V4.0',
        'wsdl': f'{BASE_ENS}enswsv4/IE323V4.wsdl',
        'operation': 'IE323V4',
        'port_production': 'IE323V4',
        'port_test': 'IE323V4Pruebas',
        'service': 'IE323V4Service',
        'signed': True,
    },
    'ens_modification': {
        'verbose_name': 'Servicio Modificación ENS V4.0',
        'wsdl': f'{BASE_ENS}enswsv4/IE313V4.wsdl',
        'operation': 'IE313V4',
        'port_production': 'IE313V4',
        'port_test': 'IE313V4Pruebas',
        'service': 'IE313V4Service',
        'signed': True,
    },
    'ens_presentation': {
        'verbose_name': 'Servicio de Presentación ENS V4.0',
        'wsdl': f'{BASE_ENS}enswsv4/IE315V4.wsdl',
        'operation': 'IE315V4',
        'port_production': 'IE315V4',
        'port_test': 'IE315V4Pruebas',
        'service': 'IE315V4Service',
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

    # EXS shares the same WSDL
    'exs_common': {
        'verbose_name': "Presentación de Declaración Sumaria de Salida",
        'wsdl': 'https://www2.agenciatributaria.gob.es/ADUA/internet/es/aeat/dit/adu/adrx/ws/IE615V2.wsdl',  # NOQA
        'operation': 'IE615V2',
        'port_production': 'IE615V2',
        'port_test': 'IE615V2Pruebas',
        'service': 'IE615V2Service',
        'signed': True,
    },
}
