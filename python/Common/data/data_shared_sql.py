"""
data_shared_sql.py

Provides SQL statements for common queries.


Christian M. Long, developer

Initial implementation: September 5, 2007
Initial language: Python 2.5.1
Current language: Python 2.7.1  www.python.org
"""

# Import shared modules
from Common.data import data_access
#from Common.utility import utl_decorators

# Import data connection object
from Common.data.data_connection import data_connection_object as db






def getItemNumberByUPC(upc):
    """
    Returns item number from database based on UPC.
    """
    sql = """
          select   trim(upitno) item_number
          from     itupc
          where    upbrit = ?
          """
    #params = [upc]
    return data_access.fetchScalarValue(db.persistentAplusDbConnection,
                                        sql,
                                        upc,
                                       )

def getUPCByItemNumber(item_number):
    """
    Returns UPC from database based on item number.
    """
    sql = """
          select   trim(upbrit) upc
          from     itupc
          where    upitno = ?
          """
    data = data_access.fetchZeroOrOneRow(db.persistentAplusDbConnection,
                                         sql,
                                         item_number,
                                        )
    if data is None:
        return None
    else:
        return data[0]

#
#@utl_decorators.memoizeFunction
#def getCountryName(country_of_origin_code):
#    """
#    Given a three-digit APlus country code, get the country name from the SQL
#    Server country_iso table.
#
#    This function is memoized, so it caches the values it fetches, to reduce
#    server queries.
#    """
#    # Note: pymssql connection to sales database uses the 'pyformat' paramstyle.
#    sql = """
#          select countrynameshort
#          from country_iso
#          where apluscntry_nbr = %(1)s
#          """
#    return data_access.fetchScalarValue(db.persistentSalesDbConnection,
#                                        sql,
#                                        country_of_origin_code,
#                                       )

def getCountryName(country_of_origin_code):
    """
    Given a three-digit APlus country code, get the country name.

    Instead of querying the databse, this function uses an embedded version of
    the SQL Server country_iso table.
    """

    # Here's the sql
    #   select apluscntry_nbr, countrynameshort
    #   from country_iso
    #   order by apluscntry_nbr

    country_iso_table = {
        000 : "VARIOUS",
        031 : "AZERBAIJAN",
        051 : "ARMENIA",
        070 : "BOSNIA/HERZEGOV",
        100 : "UNITED STATES",
        101 : "GREENLAND",
        122 : "CANADA",
        161 : "ST PIERRE/MIQUELON",
        191 : "CROATIA",
        201 : "MEXICO",
        205 : "GUATEMALA",
        208 : "BELIZE",
        211 : "EL SALVADOR",
        215 : "HONDURAS",
        219 : "NICARAGUA",
        223 : "COSTA RICA",
        225 : "PANAMA",
        232 : "BERMUDA",
        236 : "BAHAMAS",
        239 : "CUBA",
        241 : "JAMAICA",
        243 : "TURKS/CAICO ISL",
        244 : "CAYMAN ISL",
        245 : "HAITI",
        247 : "DOMINICAN REP",
        268 : "GEORGIA",
        272 : "BARBADOS",
        274 : "TRINIDAD/TOBAGO",
        275 : "PALESTINIAN TERR",
        277 : "NETHERLANDS ANT",
        283 : "GUADELOUPE",
        301 : "COLOMBIA",
        307 : "VENEZUELA",
        312 : "GUYANA",
        315 : "SURINAME",
        317 : "FRENCH GUIANA",
        331 : "ECUADOR",
        333 : "PERU",
        335 : "BOLIVIA",
        337 : "CHILE",
        348 : "HUNGARY",
        351 : "BRAZIL",
        353 : "PARAGUAY",
        355 : "URUGUAY",
        357 : "ARGENTINA",
        372 : "FALKLAND ISL",
        384 : "COTE D'IVOIRE",
        398 : "KAZAKHSTAN",
        400 : "ICELAND",
        401 : "SWEDEN",
        403 : "NORWAY",
        405 : "FINLAND",
        409 : "DENMARK",
        412 : "UNITED KINGDOM",
        419 : "IRELAND",
        421 : "NETHERLANDS",
        423 : "BELGIUM",
        427 : "FRANCE",
        428 : "GERMANY",
        433 : "AUSTRIA",
        435 : "CZECH REPUBLIC",
        441 : "SWITZERLAND",
        447 : "ESTONIA",
        449 : "LATVIA",
        451 : "LITHUANIA",
        455 : "POLAND",
        461 : "RUSSIAN FED",
        462 : "UKRAINE",
        464 : "MOLDOVA",
        470 : "SPAIN",
        471 : "PORTUGAL",
        472 : "GIBRALTAR",
        473 : "MALTA",
        475 : "ITALY",
        481 : "ALBANIA",
        484 : "GREECE",
        485 : "ROMANIA",
        487 : "BULGARIA",
        489 : "TURKEY",
        491 : "CYPRUS",
        502 : "SYRIAN ARAB REP",
        504 : "LEBANON",
        505 : "IRAQ",
        507 : "IRAN",
        508 : "ISRAEL",
        511 : "JORDAN",
        513 : "KUWAIT",
        517 : "SAUDI ARABIA",
        518 : "QATAR",
        520 : "UNITED ARAB EMI",
        521 : "YEMEN",
        523 : "OMAN",
        525 : "BAHRAIN",
        531 : "AFGHANISTAN",
        533 : "INDIA",
        535 : "PAKISTAN",
        536 : "NEPAL",
        538 : "BANGLADESH",
        542 : "SRI LANKA",
        546 : "MYANMAR",
        549 : "THAILAND",
        552 : "VIETNAM",
        553 : "LAO PPL DEM REP",
        555 : "CAMBODIA",
        557 : "MALAYSIA",
        559 : "SINGAPORE",
        560 : "INDONESIA",
        561 : "BRUNEI DARUSSAL",
        565 : "PHILIPPINES",
        566 : "MACAO",
        568 : "MALDIVES",
        570 : "CHINA",
        574 : "MONGOLIA",
        579 : "NORTH KOREA",
        580 : "SOUTH KOREA",
        582 : "HONG KONG",
        583 : "TAIWAN",
        588 : "JAPAN",
        598 : "PAPUA NEW GUINEA",
        602 : "AUSTRALIA",
        604 : "GUINEA-BISSAU",
        614 : "NEW ZEALAND",
        615 : "SAMOA",
        641 : "FR POLYNESIA",
        678 : "SAO TOME/PRINCIPE",
        681 : "MARSHALL ISL",
        682 : "MICRONESIA, FED",
        683 : "PALAU",
        688 : "SERBIA",
        714 : "MOROCCO",
        721 : "ALGERIA",
        723 : "TUNISIA",
        725 : "Libya",
        729 : "EGYPT",
        732 : "SUDAN",
        737 : "WESTERN SAHARA",
        738 : "GUINEA, EQUAT",
        741 : "MAURITANIA",
        742 : "CAMEROON",
        744 : "SENEGAL",
        745 : "MALI",
        746 : "GUINEA",
        747 : "SIERRA LEONE",
        748 : "SWAZILAND",
        749 : "GHANA",
        750 : "GAMBIA",
        751 : "NIGER",
        752 : "TOGO",
        753 : "NIGERIA",
        754 : "CENTRAL AFRICAN",
        755 : "GABON",
        756 : "CHAD",
        758 : "ST HELENA",
        760 : "BURKINA FASO",
        761 : "BENIN",
        762 : "ANGOLA",
        763 : "CONGO, DEM REP",
        765 : "LIBERIA",
        766 : "CONGO",
        767 : "BURUNDI",
        769 : "RWANDA",
        770 : "SOMALIA",
        774 : "ETHIOPIA",
        777 : "DJIBOUTI",
        778 : "UGANDA",
        779 : "KENYA",
        780 : "SEYCHELLES",
        781 : "INDIAN BR TERR",
        783 : "TANZANIA",
        785 : "MAURITIUS",
        787 : "MOZAMBIQUE",
        788 : "MADAGASCAR",
        789 : "COMOROS",
        790 : "REUNION",
        791 : "SOUTH AFRICA",
        792 : "NAMIBIA",
        793 : "BOTSWANA",
        794 : "ZAMBIA",
        795 : "TURKMENISTAN",
        796 : "ZIMBABWE",
        797 : "MALAWI",
        799 : "LESOTHO",
        860 : "UZBEKISTAN",
        903 : "PUERTO RICO",
        911 : "VIRGIN ISL USA",
        935 : "GUAM",
        951 : "AMERICAN SAMOA",
        961 : "MARIANA ISL, N",
        980 : "USA MIN OUT ISL",
        # Not listed
        # ANDORRA
        # ANTIGUA/BARBUDA
        # ANGUILLA
        # ANTARCTICA
        # ARUBA
        # ALAND ISLANDS
        # ST BARTH?LEMY
        # BONAIRE
        # BHUTAN
        # BOUVET ISL
        # BELARUS
        # COCOS (KEELING)
        # COOK ISL
        # CAPE VERDE
        # CURA?AO
        # CHRISTMAS ISL
        # DOMINICA
        # ERITREA
        # FIJI
        # FAROE ISL
        # GRENADA
        # GUERNSEY
        # S GEORGIA/SANDW
        # HEARD ISLAND
        # ISLE OF MAN
        # JERSEY
        # KYRGYZSTAN
        # KIRIBATI
        # ST KITTS/NEVIS
        # ST LUCIA
        # LIECHTENSTEIN
        # LUXEMBOURG
        # MONACO
        # MONTENEGRO
        # ST MARTIN
        # MACEDONIA
        # MARTINIQUE
        # MONTSERRAT
        # NEW CALEDONIA
        # NORFOLK ISL
        # NAURU
        # NIUE
        # PITCAIRN
        # SOLOMON ISL
        # SLOVENIA
        # SVALBARD AND JA
        # SLOVAKIA
        # SAN MARINO
        # SOUTH SUDAN
        # SINT MAARTEN
        # FRENCH S TERR
        # TAJIKISTAN
        # TOKELAU
        # TIMOR-LESTE
        # TONGA
        # TUVALU
        # VATICAN CITY ST
        # ST VINCENT
        # VIRGIN ISL BR
        # CUETA
        # POLAR REGIONS
        # MELILLA
        # MAYOTTE
        # VANUATU
        # WALLIS/FUTUNA
    }

    lookup_key = int(country_of_origin_code)
    country_name = country_iso_table.get(lookup_key, "")
    return country_name
