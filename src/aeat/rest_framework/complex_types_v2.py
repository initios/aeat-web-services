from django.conf import settings
from rest_framework import serializers as rf

from .fields import AEATDateField, AEATDateTimeField, AEATTimeField, NotRequiredStr, RequiredStr


class EXSHeader(rf.Serializer):
    '''HEAHEAType EXS'''
    RefNumHEA4 = RequiredStr(max_length=22, help_text='Reference Number. EG LRN000000041')
    TotNumOfIteHEA305 = rf.IntegerField(required=True, min_value=0, max_value=5,
                                        help_text='Total number of items. EG: 3')
    TotNumOfPacHEA306 = NotRequiredStr(max_length=7,
                                       help_text='Total number of packages. EG: 50')
    TotGroMasHEA307 = NotRequiredStr(help_text='Total gross mass. EG 10')
    DecPlaHEA394 = RequiredStr(help_text='Declaration place. EG Madrid')
    SpeCirIndHEA1 = NotRequiredStr(help_text='Specific Circumstance Indicator. EG A')
    TraChaMetOfPayHEA1 = NotRequiredStr(help_text='Transport charges / Method of Payment. EG C')
    ComRefNumHEA = NotRequiredStr(max_length=70, help_text='Commercial Reference Numer. EG a828rt')
    DecDatTimHEA114 = AEATDateTimeField(
        required=True, help_text='Declaration date and time. EG 201207041455')
    CusSubPlaHEA66 = RequiredStr(max_length=17, help_text='Customs sub place. EG 4611ZZZ999')


class EXSHeaderModification(EXSHeader, rf.Serializer):
    '''HEAHEAType EXS including MRN'''
    DocNumHEA5 = RequiredStr(help_text='EXS MRN to modify.')
    DocOpeHEA = rf.ReadOnlyField(default='M')


class EXSHeaderCancellation(EXSHeader, rf.Serializer):
    '''HEAHEAType EXS including MRN'''
    DocNumHEA5 = RequiredStr(help_text='EXS MRN to modify.')
    DocOpeHEA = rf.ReadOnlyField(default='A')


class Package(rf.Serializer):
    '''PACGS2Type'''
    KinOfPacGS23 = RequiredStr(max_length=2, help_text='Kind of packages')
    NumOfPacGS24 = NotRequiredStr(max_length=5, help_text='Number of packages')
    NumOfPieGS25 = NotRequiredStr(max_length=5, help_text='Number of pieces')
    MarNumOfPacGS21 = NotRequiredStr(max_length=140, help_text='Marks & numbers of packages')


class PreviousDocument(rf.Serializer):
    DocTypPD11 = RequiredStr(help_text='Previous Document Type. EG XSUM')
    DocRefPD12 = RequiredStr(help_text='Previous Document Reference. EG 4611099999900002')


class CustomsOfficeLodgement(rf.Serializer):
    RefNumCOL1 = RequiredStr(help_text='Reference Number. EG ES004611')


class ProducedDocumentsCertificates(rf.Serializer):
    '''PRODOCDC2Type'''
    DocTypDC21 = RequiredStr(max_length=4, help_text='Document type. EG Y022')
    DocRefDC23 = RequiredStr(max_length=35, help_text='Document reference. EG ESAEOC1')
    DocRefDCLNG = NotRequiredStr(help_text='Document reference LNG')


class CommodityCode(rf.Serializer):
    '''COMCODGODITMType'''
    ComNomCMD1 = RequiredStr(min_length=4, max_length=8,
                             help_text='Combined Nomenclature. EG 123456')


class Container(rf.Serializer):
    '''CONNR2Type'''
    ConNumNR21 = RequiredStr(max_length=17, help_text='Container number')


class GoodsItem(rf.Serializer):
    '''GOOITEGDSType'''
    IteNumGDS7 = rf.IntegerField(required=True, help_text='Item Number. EG 1')
    GooDesGDS23 = NotRequiredStr(help_text='Goods description. EG DESCRIPCION  PARTIDA1')
    GroMasGDS46 = NotRequiredStr(help_text='Gross mass. EG 100')
    MetOfPayGDI12 = NotRequiredStr(help_text='Transport charges / Method of payment')
    ComRefNumGIM1 = NotRequiredStr(help_text='Commercial Reference Number. EG REFERENCIACOMER1')
    UNDanGooCodGDI1 = NotRequiredStr(help_text='UN dangerous goods code (Numeric 4). Min=0')
    PlaLoaGOOITE333 = NotRequiredStr(help_text='Place of loading. Max 35. Min=0')
    PlaLoaGOOITE333LNG = NotRequiredStr(help_text='Place of loading LNG. Min=0')
    PlaUnlGOOITE333 = NotRequiredStr(help_text='Place of unloading. Max 35. Min=0')
    PlaUnlGOOITE333LNG = NotRequiredStr(help_text='Place of unloading LNG. Min=0')
    PREDOCGODITM1 = PreviousDocument(required=True)
    PRODOCDC2 = ProducedDocumentsCertificates(required=False, many=True)
    COMCODGODITM = CommodityCode(required=False)
    CONNR2 = Container(many=True, required=False)
    PACGS2 = Package(many=True, required=False)


class PersonLodgingSummaryDeclaration(rf.Serializer):
    '''PERLODSUMDECType'''
    NamPLD1 = NotRequiredStr(help_text='Name')
    StrAndNumPLD1 = NotRequiredStr(help_text='Street and number')
    PosCodPLD1 = NotRequiredStr(help_text='Postal code')
    CitPLD1 = NotRequiredStr(help_text='City')
    CouCodPLD1 = NotRequiredStr(help_text='Country code')
    TINPLD1 = RequiredStr(min_length=3, max_length=17,
                          help_text='Trader indentification number')


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


class Itinerary(rf.Serializer):
    '''ITIType'''
    CouOfRouCodITI1 = RequiredStr(help_text='Country of routing code')


class SealsIdentity(rf.Serializer):
    '''SEAID529Type'''
    SeaIdSEAID530 = RequiredStr(max_length=20, help_text='Seals identity')


class BaseMixin(rf.Serializer):
    '''Common attributes'''
    Id = NotRequiredStr(source='MesIdeMES19')
    NifDeclarante = NotRequiredStr(read_only=True, default=settings.AEAT_VAT_NUMBER)
    NombreDeclarante = NotRequiredStr(read_only=True, default=settings.AEAT_LEGAL_NAME)

    MesTypMES20 = rf.ReadOnlyField(default='CC615A', help_text='Message type')
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
    CUSOFFLON = CustomsOfficeLodgement(required=True)
    ITI = Itinerary(required=False, many=True)
    PERLODSUMDEC = PersonLodgingSummaryDeclaration(required=False)
    SEAID529 = SealsIdentity(required=False, many=True)
