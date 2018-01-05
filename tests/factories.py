import datetime as dt

import factory


class ENSPresentationHeader(factory.Factory):
    class Meta:
        model = dict

    RefNumHEA4 = 'LRN000000041'
    TraModAtBorHEA76 = '5'
    IdeOfMeaOfTraCroHEA85 = '1111111'
    IdeOfMeaOfTraCroHEA85LNG = 'ES'
    TotNumOfIteHEA305 = '3'
    TotNumOfPacHEA306 = '50'
    TotGroMasHEA307 = '10'
    DecPlaHEA394 = 'Madrid'
    DecPlaHEA394LNG = 'ES'
    SpeCirIndHEA1 = 'A'
    TraChaMetOfPayHEA1 = 'C'
    ComRefNumHEA = 'a828rt'
    ConRefNumHEA = '7777b'
    PlaLoaGOOITE334 = 'ESMadrid'
    PlaLoaGOOITE334LNG = 'ES'
    PlaUnlGOOITE334 = 'ESSegovia'
    CodPlUnHEA357LNG = 'ES'
    DecDatTimHEA114 = factory.LazyAttribute(lambda x: dt.datetime.now().strftime('%Y%m%d%H%M'))


class TraderConsignor(factory.Factory):
    class Meta:
        model = dict

    NamCO17 = 'JUAN CARLOS'
    StrAndNumCO122 = 'Almansa'
    PosCodCO123 = '28007'
    CitCO124 = 'Madrid'
    CouCO125 = 'ES'
    NADLNGCO = 'ES'
    TINCO159 = 'ESA08005688'


class TraderConsignee(factory.Factory):
    class Meta:
        model = dict

    NamCE17 = 'LUÍS'
    StrAndNumCE122 = 'Cruz'
    PosCodCE123 = '28005'
    CitCE124 = 'Madrid'
    CouCE125 = 'ES'
    NADLNGCE = 'ES'
    TINCE159 = 'ESA08005688'


class ProducedDocumentsCertificates(factory.Factory):
    class Meta:
        model = dict

    DocTypDC21 = 'Y022'
    DocRefDC23 = 'ESAEOC1'
    DocRefDCLNG = 'ES'


class SpecialMentions(factory.Factory):
    class Meta:
        model = dict

    AddInfCodMT23 = 'xxx'


class CommodityCode(factory.Factory):
    class Meta:
        model = dict

    ComNomCMD1 = '123456'


class Container(factory.Factory):
    class Meta:
        model = dict

    ConNumNR21 = '1'


class Package(factory.Factory):
    class Meta:
        model = dict

    KinOfPacGS23 = 'NE'
    NumOfPacGS24 = '0'
    NumOfPieGS25 = '10'
    MarNumOfPacGSL21 = 'PAQUETES1'
    MarNumOfPacGSL21LNG = 'ES'


class GoodsItem(factory.Factory):
    class Meta:
        model = dict

    IteNumGDS7 = '1'
    GooDesGDS23 = 'DESCRIPCION  PARTIDA1'
    GooDesGDS23LNG = 'ES'
    GroMasGDS46 = '100'
    ComRefNumGIM1 = 'REFERENCIACOMER1'

    SPEMENMT2 = factory.SubFactory(SpecialMentions)
    COMCODGODITM = factory.SubFactory(CommodityCode)

    @factory.post_generation
    def CONNR2(self, create, extracted, **kwargs):
        if extracted:
            # A list of groups were passed in, use them
            self['CONNR2'] = extracted
        else:
            self['CONNR2'] = [Container()]

    @factory.post_generation
    def PRODOCDC2(self, create, extracted, **kwargs):
        if extracted:
            # A list of groups were passed in, use them
            self['PRODOCDC2'] = extracted
        else:
            self['PRODOCDC2'] = [ProducedDocumentsCertificates()]

    @factory.post_generation
    def PACGS2(self, create, extracted, **kwargs):
        if extracted:
            # A list of groups were passed in, use them
            self['PACGS2'] = extracted
        else:
            self['PACGS2'] = [Package()]


class PersonLodgingSummaryDeclaration(factory.Factory):
    class Meta:
        model = dict

    NamPLD1 = 'PEDRO'
    StrAndNumPLD1 = 'CASTELLANA'
    PosCodPLD1 = '28003'
    CitPLD1 = 'MADRID'
    CouCodPLD1 = 'ES'
    PERLODSUMDECLNG = 'ES'
    TINPLD1 = 'ESA08005688'


class SealsIdentity(factory.Factory):
    class Meta:
        model = dict

    SeaIdSEAID530 = '1'
    SeaIdSEAID530LNG = 'ES'


class CustomsOfficeFirstEntry(factory.Factory):
    class Meta:
        model = dict

    RefNumCUSOFFFENT731 = 'ES009999'
    ExpDatOfArrFIRENT733 = factory.LazyAttribute(lambda x: dt.datetime.now().strftime('%Y%m%d%H%M'))


class CustomsOfficeSubsequentEntry(factory.Factory):
    class Meta:
        model = dict

    RefNumSUBENR909 = 'FR000010'


class TraderEntryCarrier(factory.Factory):
    class Meta:
        model = dict

    NamTRACARENT604 = 'ROSA'
    StrNumTRACARENT607 = 'MONCLOA'
    PstCodTRACARENT606 = '28007'
    CtyTRACARENT603 = 'MADRID'
    CouCodTRACARENT605 = 'ES'
    TRACARENT601LNG = 'ES'
    TINTRACARENT602 = 'ESA08005688'


class ENSPresentationFactory(factory.Factory):
    class Meta:
        model = dict

    MesSenMES3 = factory.Sequence(lambda n: 'VAT00000%d' % n)
    MesRecMES6 = 'NICA.ES'
    DatOfPreMES9 = factory.LazyAttribute(lambda x: dt.datetime.now().strftime('%y%m%d'))
    TimOfPreMES10 = factory.LazyAttribute(lambda x: dt.datetime.now().strftime('%H%M'))
    MesIdeMES19 = factory.Sequence(lambda n: 'Id000%d' % n)
    MesTypMES20 = 'CC315A'

    HEAHEA = factory.SubFactory(ENSPresentationHeader)
    TRACONCO1 = factory.SubFactory(TraderConsignor)
    TRACONCE1 = factory.SubFactory(TraderConsignee)
    PERLODSUMDEC = factory.SubFactory(PersonLodgingSummaryDeclaration)
    CUSOFFFENT730 = factory.SubFactory(CustomsOfficeFirstEntry)
    TRACARENT601 = factory.SubFactory(TraderEntryCarrier)

    @factory.post_generation
    def GOOITEGDS(self, create, extracted, **kwargs):
        if extracted:
            # A list of groups were passed in, use them
            self['GOOITEGDS'] = extracted
        else:
            self['GOOITEGDS'] = [GoodsItem()]

    @factory.post_generation
    def SEAID529(self, create, extracted, **kwargs):
        if extracted:
            # A list of groups were passed in, use them
            self['SEAID529'] = extracted
        else:
            self['SEAID529'] = [SealsIdentity()]

    @factory.post_generation
    def CUSOFFSENT740(self, create, extracted, **kwargs):
        if extracted:
            # A list of groups were passed in, use them
            self['CUSOFFSENT740'] = extracted
        else:
            self['CUSOFFSENT740'] = [CustomsOfficeSubsequentEntry()]


class ENSQueryFactory(factory.Factory):
    class Meta:
        model = dict

    TraModAtBorHEA76 = '1'
    ExpDatOfArr = '20110809'
    ConRefNum = '9294408'
