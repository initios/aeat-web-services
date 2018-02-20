import datetime as dt

import factory


class EXSHeader(factory.Factory):
    class Meta:
        model = dict

    RefNumHEA4 = 'LRN000000041'
    TotNumOfIteHEA305 = '3'
    TotNumOfPacHEA306 = '50'
    TotGroMasHEA307 = '10'
    DecPlaHEA394 = 'Madrid'
    SpeCirIndHEA1 = 'A'
    TraChaMetOfPayHEA1 = 'C'
    ComRefNumHEA = 'a828rt'
    DecDatTimHEA114 = factory.LazyAttribute(lambda x: dt.datetime.now())
    CusSubPlaHEA66 = '4611ZZZ999'


class EXSModificationHeader(EXSHeader):
    class Meta:
        model = dict

    DocNumHEA5 = 'MRNCODE12345'


class EXSCancellationHeader(EXSHeader):
    class Meta:
        model = dict

    DocNumHEA5 = 'MRNCODE12345'


class TraderConsignor(factory.Factory):
    class Meta:
        model = dict

    NamCO17 = 'JUAN CARLOS'
    StrAndNumCO122 = 'Almansa'
    PosCodCO123 = '28007'
    CitCO124 = 'Madrid'
    CouCO125 = 'ES'
    TINCO159 = 'ESA08005688'


class TraderConsignee(factory.Factory):
    class Meta:
        model = dict

    NamCE17 = 'LUÍS'
    StrAndNumCE122 = 'Cruz'
    PosCodCE123 = '28005'
    CitCE124 = 'Madrid'
    CouCE125 = 'ES'
    TINCE159 = 'ESA08005688'


class ProducedDocumentsCertificates(factory.Factory):
    class Meta:
        model = dict

    DocTypDC21 = 'Y022'
    DocRefDC23 = 'ESAEOC1'


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
    MarNumOfPacGSL21LNG = 'ES'


class PreviousDocument(factory.Factory):
    class Meta:
        model = dict

    DocTypPD11 = 'XSUM'
    DocRefPD12 = '4611099999900002'


class CustomsOfficeLodgement(factory.Factory):
    class Meta:
        model = dict

    RefNumCOL1 = 'ES004611'


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
    PREDOCGODITM1 = factory.SubFactory(PreviousDocument)

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
    TINPLD1 = 'ESA08005688'


class SealsIdentity(factory.Factory):
    class Meta:
        model = dict

    SeaIdSEAID530 = '1'


class BaseMessageMixin(factory.Factory):
    MesSenMES3 = factory.Sequence(lambda n: 'VAT00000%d' % n)
    DatOfPreMES9 = factory.LazyAttribute(lambda x: dt.datetime.now().date())
    TimOfPreMES10 = factory.LazyAttribute(lambda x: dt.datetime.now().time())
    MesIdeMES19 = factory.Sequence(lambda n: 'TESTID000%d' % n)

    HEAHEA = factory.SubFactory(EXSHeader)
    TRACONCO1 = factory.SubFactory(TraderConsignor)
    TRACONCE1 = factory.SubFactory(TraderConsignee)
    PERLODSUMDEC = factory.SubFactory(PersonLodgingSummaryDeclaration)
    CUSOFFLON = factory.SubFactory(CustomsOfficeLodgement)

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


class EXSPresentationFactory(BaseMessageMixin, factory.Factory):
    class Meta:
        model = dict

    HEAHEA = factory.SubFactory(EXSHeader)


class EXSModificationFactory(BaseMessageMixin, factory.Factory):
    class Meta:
        model = dict

    HEAHEA = factory.SubFactory(EXSModificationHeader)


class EXSCancellationFactory(BaseMessageMixin, factory.Factory):
    class Meta:
        model = dict

    HEAHEA = factory.SubFactory(EXSCancellationHeader)
