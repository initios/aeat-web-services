from django.conf import settings
from rest_framework import serializers as rf

from .fields import AEATDateField, AEATDateTimeField, AEATTimeField, NotRequiredStr, RequiredStr


class ENSPresentationHeader(rf.Serializer):
    '''HEAHEAType'''
    RefNumHEA4 = RequiredStr(max_length=22, help_text='Reference Number. EG LRN000000041')
    TraModAtBorHEA76 = RequiredStr(max_length=2, help_text='Transport mode at border. EG 5.')
    IdeOfMeaOfTraCroHEA85 = NotRequiredStr(
        max_length=27, help_text='Identity of means of transport crossing border. EG 1111111')
    IdeOfMeaOfTraCroHEA85LNG = NotRequiredStr(help_text='Identity of means of transport '
                                                        'crossing border LNG. EG ES')
    TotNumOfIteHEA305 = rf.IntegerField(required=True, min_value=0, max_value=5,
                                        help_text='Total number of items. EG: 3')
    TotNumOfPacHEA306 = NotRequiredStr(max_length=7,
                                       help_text='Total number of packages. EG: 50')
    TotGroMasHEA307 = NotRequiredStr(help_text='Total gross mass. EG 10')
    DecPlaHEA394 = RequiredStr(help_text='Declaration place. EG Madrid')
    DecPlaHEA394LNG = RequiredStr(help_text='Declaration place LNG. EG ES')
    SpeCirIndHEA1 = NotRequiredStr(help_text='Specific Circumstance Indicator. EG A')
    TraChaMetOfPayHEA1 = NotRequiredStr(help_text='Transport charges / Method of Payment. EG C')
    ComRefNumHEA = NotRequiredStr(max_length=70, help_text='Commercial Reference Numer. EG a828rt')
    ConRefNumHEA = NotRequiredStr(max_length=35, help_text='Conveyance reference number. EG 7777b')
    PlaLoaGOOITE334 = NotRequiredStr(max_length=35, help_text='Place of loading. EG ESMadrid')
    PlaLoaGOOITE334LNG = NotRequiredStr(help_text='Place of loading LNG. EG ES')
    PlaUnlGOOITE334 = NotRequiredStr(max_length=35, help_text='Place of unloading. EG ESSegovia')
    CodPlUnHEA357LNG = NotRequiredStr(help_text='Place of unloading LNG. EG ES')
    DecDatTimHEA114 = AEATDateTimeField(
        required=True, help_text='Declaration date and time. EG 201207041455')


class ENSModificationHeader(rf.Serializer):
    '''HEAHEAType with mandatory MRNType'''
    TraModAtBorHEA76 = RequiredStr(max_length=2, help_text='Transport mode at border. EG 5.')
    IdeOfMeaOfTraCroHEA85 = NotRequiredStr(
        max_length=27, help_text='Identity of means of transport crossing border. EG 1111111')
    IdeOfMeaOfTraCroHEA85LNG = NotRequiredStr(help_text='Identity of means of transport '
                                                        'crossing border LNG. EG ES')
    TotNumOfIteHEA305 = rf.IntegerField(required=True, min_value=0, max_value=5,
                                        help_text='Total number of items. EG: 3')
    TotNumOfPacHEA306 = NotRequiredStr(max_length=7,
                                       help_text='Total number of packages. EG: 50')
    TotGroMasHEA307 = NotRequiredStr(help_text='Total gross mass. EG 10')
    SpeCirIndHEA1 = NotRequiredStr(help_text='Specific Circumstance Indicator. EG A')
    TraChaMetOfPayHEA1 = NotRequiredStr(help_text='Transport charges / Method of Payment. EG C')
    ComRefNumHEA = NotRequiredStr(max_length=70, help_text='Commercial Reference Numer. EG a828rt')
    ConRefNumHEA = NotRequiredStr(max_length=35, help_text='Conveyance reference number. EG 7777b')
    PlaLoaGOOITE334 = NotRequiredStr(max_length=35, help_text='Place of loading. EG ESMadrid')
    PlaLoaGOOITE334LNG = NotRequiredStr(help_text='Place of loading LNG. EG ES')
    PlaUnlGOOITE334 = NotRequiredStr(max_length=35, help_text='Place of unloading. EG ESSegovia')
    CodPlUnHEA357LNG = NotRequiredStr(help_text='Place of unloading LNG. EG ES')

    # Specific Modification fields
    DocNumHEA5 = RequiredStr(help_text='Document/reference number')
    AmdPlaHEA598 = RequiredStr(help_text='Amendment place')
    DatTimAmeHEA113 = AEATDateTimeField(
        required=True, help_text='Declaration date and time. EG 201207041455')


class TraderConsignor(rf.Serializer):
    '''TRACONCO1Type'''
    NamCO17 = NotRequiredStr(help_text='Name. EG JUAN CARLOS')
    StrAndNumCO122 = NotRequiredStr(help_text='Street and number. EG Almansa')
    PosCodCO123 = NotRequiredStr(help_text='Postal code. EG 28007')
    CitCO124 = NotRequiredStr(help_text='City. EG Madrid')
    CouCO125 = NotRequiredStr(help_text='Country code. EG ES')
    NADLNGCO = NotRequiredStr(help_text='NAD LNG. EG ES')
    TINCO159 = NotRequiredStr(help_text='TIN (Trader identification number). EG ESA08005688')


class TraderConsignee(rf.Serializer):
    '''TRACONCE1Type'''
    NamCE17 = NotRequiredStr(help_text='Name. EG luis')
    StrAndNumCE122 = NotRequiredStr(help_text='Street and number. EG cruz')
    PosCodCE123 = NotRequiredStr(help_text='Postal code. EG 28005')
    CitCE124 = NotRequiredStr(help_text='City. EG Madrid')
    CouCE125 = NotRequiredStr(help_text='Country code. EG ES')
    NADLNGCE = NotRequiredStr(help_text='NAD LNG. EG ES')
    TINCE159 = NotRequiredStr(help_text='TIN (Trader identification number). EG ESA08005688')


class ProducedDocumentsCertificates(rf.Serializer):
    '''PRODOCDC2Type'''
    DocTypDC21 = RequiredStr(max_length=4, help_text='Document type. EG Y022')
    DocRefDC23 = RequiredStr(max_length=35, help_text='Document reference. EG ESAEOC1')
    DocRefDCLNG = NotRequiredStr(help_text='Document reference LNG')


class SpecialMentions(rf.Serializer):
    '''SPEMENMT2Type'''
    AddInfCodMT23 = RequiredStr(max_length=5, help_text='Additional information coded')


class CommodityCode(rf.Serializer):
    '''COMCODGODITMType'''
    ComNomCMD1 = RequiredStr(min_length=4, max_length=8,
                             help_text='Combined Nomenclature. EG 123456')


class Container(rf.Serializer):
    '''CONNR2Type'''
    ConNumNR21 = RequiredStr(max_length=17, help_text='Container number')


class Package(rf.Serializer):
    '''PACGS2Type'''
    KinOfPacGS23 = RequiredStr(max_length=2, help_text='Kind of packages')
    NumOfPacGS24 = NotRequiredStr(max_length=5, help_text='Number of packages')
    NumOfPieGS25 = NotRequiredStr(max_length=5, help_text='Number of pieces')
    MarNumOfPacGSL21 = NotRequiredStr(max_length=140,
                                      help_text='Marks & numbers of packages (long)')
    MarNumOfPacGSL21LNG = NotRequiredStr(help_text='Marks & numbers of packages (long) LNG')


class GoodsItem(rf.Serializer):
    '''GOOITEGDSType'''
    IteNumGDS7 = rf.IntegerField(required=True, help_text='Item Number. EG 1')
    GooDesGDS23 = NotRequiredStr(help_text='Goods description. EG DESCRIPCION  PARTIDA1')
    GooDesGDS23LNG = NotRequiredStr(help_text='Goods description LNG. EG ES')
    GroMasGDS46 = NotRequiredStr(help_text='Gross mass. EG 100')
    MetOfPayGDI12 = NotRequiredStr(help_text='Transport charges / Method of payment')
    ComRefNumGIM1 = NotRequiredStr(help_text='Commercial Reference Number. EG REFERENCIACOMER1')
    UNDanGooCodGDI1 = NotRequiredStr(help_text='UN dangerous goods code (Numeric 4). Min=0')
    PlaLoaGOOITE333 = NotRequiredStr(help_text='Place of loading. Max 35. Min=0')
    PlaLoaGOOITE333LNG = NotRequiredStr(help_text='Place of loading LNG. Min=0')
    PlaUnlGOOITE333 = NotRequiredStr(help_text='Place of unloading. Max 35. Min=0')
    PlaUnlGOOITE333LNG = NotRequiredStr(help_text='Place of unloading LNG. Min=0')

    PRODOCDC2 = ProducedDocumentsCertificates(required=False, many=True)
    SPEMENMT2 = SpecialMentions(required=False)
    # TRACONCO2 - not in aeat example. It may not be needed
    COMCODGODITM = CommodityCode(required=False)
    # TRACONCE2 - not in aeat example. It may not be needed
    CONNR2 = Container(many=True, required=False)
    # IDEMEATRAGI970 - not in aeat example. It may not be needed
    PACGS2 = Package(many=True, required=False)
    # PRTNOT640 - not in aeat example. It may not be needed


class Itinerary(rf.Serializer):
    '''ITIType'''
    CouOfRouCodITI1 = RequiredStr(help_text='Country of routing code')


class PersonLodgingSummaryDeclaration(rf.Serializer):
    '''PERLODSUMDECType'''
    NamPLD1 = NotRequiredStr(help_text='Name')
    StrAndNumPLD1 = NotRequiredStr(help_text='Street and number')
    PosCodPLD1 = NotRequiredStr(help_text='Postal code')
    CitPLD1 = NotRequiredStr(help_text='City')
    CouCodPLD1 = NotRequiredStr(help_text='Country code')
    PERLODSUMDECLNG = NotRequiredStr(help_text='Language code')
    TINPLD1 = RequiredStr(min_length=3, max_length=17,
                          help_text='Trader indentification number')


class SealsIdentity(rf.Serializer):
    '''SEAID529Type'''
    SeaIdSEAID530 = RequiredStr(max_length=20, help_text='Seals identity')
    SeaIdSEAID530LNG = NotRequiredStr(help_text='Seals identity LNG')


class CustomsOfficeFirstEntry(rf.Serializer):
    '''CUSOFFFENT730Type'''
    RefNumCUSOFFFENT731 = RequiredStr(max_length=8, help_text='Reference number')
    ExpDatOfArrFIRENT733 = AEATDateTimeField(
        required=True, help_text='Expected date and time of arrival')


class CustomsOfficeSubsequentEntry(rf.Serializer):
    '''CUSOFFSENT740Type'''
    RefNumSUBENR909 = RequiredStr(max_length=8, help_text='Reference number')


class TraderEntryCarrier(rf.Serializer):
    '''TRACARENT601Type'''
    NamTRACARENT604 = NotRequiredStr(help_text='Name')
    StrNumTRACARENT607 = NotRequiredStr(help_text='Street and number')
    PstCodTRACARENT606 = NotRequiredStr(help_text='Postal code')
    CtyTRACARENT603 = NotRequiredStr(help_text='City')
    CouCodTRACARENT605 = NotRequiredStr(help_text='Country code')
    TRACARENT601LNG = NotRequiredStr(help_text='Language code')
    TINTRACARENT602 = NotRequiredStr(help_text='Trader identification number')


class TraderRepresentative(rf.Serializer):
    '''TRAREPType'''
    NamTRE1 = NotRequiredStr(help_text='Name')
    StrAndNumTRE1 = NotRequiredStr(help_text='Street and number')
    PosCodTRE1 = NotRequiredStr(help_text='Postal code')
    CitTRE1 = NotRequiredStr(help_text='City')
    CouCodTRE1 = NotRequiredStr(help_text='Country code')
    TRAREPLNG = NotRequiredStr(help_text='NAD LNG')
    TINTRE1 = NotRequiredStr(help_text='Trader indentification number')


class NotifyParty(rf.Serializer):
    '''NOTPAR670Type'''
    NamNOTPAR672 = NotRequiredStr(help_text='Name')
    StrNumNOTPAR673 = NotRequiredStr(help_text='Street and number')
    PosCodNOTPAR676 = NotRequiredStr(help_text='Postal code')
    CitNOTPAR674 = NotRequiredStr(help_text='City')
    CouCodNOTPAR675 = NotRequiredStr(help_text='Country code')
    NOTPAR670LNG = NotRequiredStr(help_text='NAD LNG')
    TINNOTPAR671 = NotRequiredStr(help_text='Trader indentification number')


class BaseMixin(rf.Serializer):
    '''Common attributes'''
    Id = NotRequiredStr(source='MesIdeMES19')
    NifDeclarante = NotRequiredStr(read_only=True, default=settings.AEAT_VAT_NUMBER)
    NombreDeclarante = NotRequiredStr(read_only=True, default=settings.AEAT_LEGAL_NAME)

    MesSenMES3 = NotRequiredStr(max_length=35, read_only=True,
                                default=settings.AEAT_VAT_NUMBER,
                                help_text='Message Sender (VAT Number). EG. 89890001K')
    MesRecMES6 = NotRequiredStr(max_length=35, default='NICA.ES', read_only=True,
                                help_text='EG NICA.ES (default)')
    DatOfPreMES9 = AEATDateField(required=True, allow_null=False,
                                 help_text='Date of preparation. EG 101010 (YYMMDD)')
    TimOfPreMES10 = AEATTimeField(required=True, allow_null=False,
                                  help_text='Time of preparation. EG 1010 (HHMM)')
    MesIdeMES19 = RequiredStr(max_length=14, help_text='Message identification. '
                                                       'EG 09ES112222110 (like Id)')

    TRACONCO1 = TraderConsignor(required=True)
    TRACONCE1 = TraderConsignee(required=True)
    GOOITEGDS = GoodsItem(required=True, many=True)
    ITI = Itinerary(required=False, many=True)
    TRAREP = TraderRepresentative(required=False)
    PERLODSUMDEC = PersonLodgingSummaryDeclaration(required=False)
    SEAID529 = SealsIdentity(required=False, many=True)
    CUSOFFFENT730 = CustomsOfficeFirstEntry(required=True)
    CUSOFFSENT740 = CustomsOfficeSubsequentEntry(required=False, many=True)
    TRACARENT601 = TraderEntryCarrier(required=False)
