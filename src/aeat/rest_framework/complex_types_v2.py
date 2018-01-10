from django.conf import settings

from rest_framework import serializers as rf

from .fields import AEATDateField, AEATTimeField, AEATDateTimeField, NotRequiredStr, RequiredStr


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


class Package(rf.Serializer):
    '''PACGS2Type'''
    KinOfPacGS23 = RequiredStr(max_length=2, help_text='Kind of packages')
    NumOfPacGS24 = NotRequiredStr(max_length=5, help_text='Number of packages')
    NumOfPieGS25 = NotRequiredStr(max_length=5, help_text='Number of pieces')
    MarNumOfPacGSL21 = NotRequiredStr(max_length=140,
                                      help_text='Marks & numbers of packages (long)')


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

    # PRODOCDC2 = ProducedDocumentsCertificates(required=False, many=True)
    # COMCODGODITM = CommodityCode(required=False)
    # CONNR2 = Container(many=True, required=False)
    PACGS2 = Package(many=True, required=False)


class BaseV2Mixin(rf.Serializer):
    '''Common attributes'''
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

    # TRACONCO1 = TraderConsignor(required=True)
    # TRACONCE1 = TraderConsignee(required=True)
    GOOITEGDS = GoodsItem(required=True, many=True)
    # ITI = Itinerary(required=False, many=True)
    # TRAREP = TraderRepresentative(required=False)
    # PERLODSUMDEC = PersonLodgingSummaryDeclaration(required=False)
    # SEAID529 = SealsIdentity(required=False, many=True)
    # CUSOFFFENT730 = CustomsOfficeFirstEntry(required=True)
    # CUSOFFSENT740 = CustomsOfficeSubsequentEntry(many=True)
    # TRACARENT601 = TraderEntryCarrier(required=False)
