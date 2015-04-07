"""
Tests for the Shopfloor Monitor service

"""
# pylint: disable=too-many-lines,too-many-public-methods,line-too-long,missing-docstring

import requests
from nose import tools

from CML_Pickpack.pickpack_modules import pickpack_constants
from CML_Pickpack.pickpack_modules.test import utility_functions_for_testing

if pickpack_constants.SHOW_FULL_DIFF:
    # Force Nose to output the full diff
    from unittest import TestCase
    TestCase.maxDiff = None



class ShopfloorMonitorOrderNumbersService(object):
    def call_service(self,
                     shipping_station,
                     order_type,
                     expected_result,
                    ):
        """
        Call the Shopfloor Monitor service
        """
        parameters = {'scale' : shipping_station,
                      'show_backorder' : self.show_backorder,                   # pylint: disable=no-member
                      'order_type' : order_type,
                     }
        response = requests.get('http://partsappdev.joco.com:8082/shopfloor_monitor/j_status_order_numbers',
                                params = parameters,
                               )
        actual_result = utility_functions_for_testing.read_json_from_response(response)

        last_print_data = {u'last_print_data': {u'last_print_formatted_order_number': u'AA001/00',
                                                u'entry_date_of_last_printed_order': u'12/11/2014',
                                                u'entry_time_of_last_printed_order': u'8:10 AM',
                                                u'last_print_date': u'12/11/2014',
                                                u'last_print_time': u'8:49 AM',
                                               }
                          }
        expected_result.update(last_print_data)

        tools.assert_equal(actual_result, expected_result)


class ShopfloorMonitorOrderNumbersServiceOrdinary(ShopfloorMonitorOrderNumbersService):
    def __init__(self):
        ShopfloorMonitorOrderNumbersService.__init__(self)
        self.show_backorder = 'false'


class TestShopfloorMonitorOrderNumbersServiceOrdinary(ShopfloorMonitorOrderNumbersServiceOrdinary):
    def __init__(self):
        ShopfloorMonitorOrderNumbersServiceOrdinary.__init__(self)

    def test1(self):
        shipping_station = 'wcc'
        order_type = 'today_sure'
        expected_result = {
            u'should_ship_today': {
                u'ready_to_print': ['AA007/00', 'AA008/00', 'AA009/00', 'AA010/00', 'AA011/00', 'AA012/00', 'AA013/00'],
                u'packed': [],
                u'pick_slip_printed': ['AA014/00', 'AA015/00', 'AA016/00', 'AA017/00', 'AA018/00', 'AA019/00', 'AA020/00', 'AA021/00', 'AA022/00', 'AA023/00']},
            u'can_ship_tomorrow': {
                u'ready_to_print': ['AA000/00', 'AA001/00', 'AA002/00'],
                u'packed': ['AA006/00'],
                u'pick_slip_printed': ['AA003/00', 'AA004/00', 'AA005/00'],
            },
        }
        self.call_service(shipping_station,
                          order_type,
                          expected_result,
                         )

    def test2(self):
        shipping_station = 'wcc'
        order_type = 'signature_service'
        expected_result = {
            u'should_ship_today': {
                u'ready_to_print': ['AA101/00', 'AA102/00', 'AA103/00', 'AA104/00', 'AA105/00', 'AA106/00', 'AA107/00', 'AA108/00', 'AA109/00', 'AA110/00', 'AA111/00', 'AA112/00', 'AA113/00', 'AA114/00', 'AA115/00', 'AA116/00', 'AA117/00', 'AA118/00', 'AA119/00', 'AA120/00', 'AA121/00', 'AA122/00', 'AA123/00', 'AA124/00', 'AA125/00', 'AA126/00', 'AA127/00', 'AA128/00', 'AA129/00', 'AA130/00', 'AA131/00', 'AA132/00', 'AA133/00', 'AA134/00', 'AA135/00', 'AA136/00', 'AA137/00', 'AA138/00', 'AA139/00', 'AA140/00', 'AA141/00', 'AA142/00', 'AA143/00', 'AA144/00', 'AA145/00', 'AA146/00', 'AA147/00', 'AA148/00', 'AA149/00', 'AA150/00', 'AA151/00', 'AA152/00', 'AA153/00', 'AA154/00', 'AA155/00', 'AA156/00', 'AA157/00', 'AA158/00', 'AA159/00', 'AA160/00', '... 415 more'],
                u'packed': ['AA586/00', 'AA587/00', 'AA588/00'],
                u'pick_slip_printed': ['AA576/00', 'AA577/00', 'AA578/00', 'AA579/00', 'AA580/00', 'AA581/00', 'AA582/00', 'AA583/00', 'AA584/00', 'AA585/00']},
            u'can_ship_tomorrow': {
                u'ready_to_print': ['AA024/00', 'AA025/00', 'AA026/00', 'AA027/00', 'AA028/00', 'AA029/00', 'AA030/00', 'AA031/00', 'AA032/00', 'AA033/00', 'AA034/00', 'AA035/00', 'AA036/00', 'AA037/00', 'AA038/00', 'AA039/00', 'AA040/00', 'AA041/00', 'AA042/00', 'AA043/00', 'AA044/00', 'AA045/00', 'AA046/00', 'AA047/00', 'AA048/00', 'AA049/00', 'AA050/00', 'AA051/00', 'AA052/00', 'AA053/00', 'AA054/00', 'AA055/00', 'AA056/00', 'AA057/00', 'AA058/00', 'AA059/00', 'AA060/00', 'AA061/00', 'AA062/00', 'AA063/00', 'AA064/00', 'AA065/00', 'AA066/00'],
                u'packed': ['AA100/00'],
                u'pick_slip_printed': ['AA067/00', 'AA068/00', 'AA069/00', 'AA070/00', 'AA071/00', 'AA072/00', 'AA073/00', 'AA074/00', 'AA075/00', 'AA076/00', 'AA077/00', 'AA078/00', 'AA079/00', 'AA080/00', 'AA081/00', 'AA082/00', 'AA083/00', 'AA084/00', 'AA085/00', 'AA086/00', 'AA087/00', 'AA088/00', 'AA089/00', 'AA090/00', 'AA091/00', 'AA092/00', 'AA093/00', 'AA094/00', 'AA095/00', 'AA096/00', 'AA097/00', 'AA098/00', 'AA099/00'],
            },
        }
        self.call_service(shipping_station,
                          order_type,
                          expected_result,
                         )

    def test3(self):
        shipping_station = 'wcc'
        order_type = 'service_file'
        expected_result = {
            u'should_ship_today': {
                u'ready_to_print': ['AA605/00', 'AA606/00', 'AA607/00', 'AA608/00', 'AA609/00', 'AA610/00', 'AA611/00', 'AA612/00'],
                u'packed': [],
                u'pick_slip_printed': ['AA613/00', 'AA614/00', 'AA615/00', 'AA616/00', 'AA617/00', 'AA618/00', 'AA619/00', 'AA620/00', 'AA621/00', 'AA622/00', 'AA623/00', 'AA624/00', 'AA625/00', 'AA626/00'],
            },
        }
        self.call_service(shipping_station,
                          order_type,
                          expected_result,
                         )

    def test4(self):
        shipping_station = 'wcc'
        order_type = 'normal'
        expected_result = {
            u'should_ship_today': {
                u'ready_to_print': ['AA633/00', 'AA640/00', 'AA635/00', 'AA700/00', 'AA637/00', 'AA638/00', 'AA639/00', 'AA710/00', 'AA641/00', 'AA642/00', 'AA643/00', 'AA644/00', 'AA645/00', 'AA646/00', 'AA647/00', 'AA648/00', 'AA649/00', 'AA650/00', 'AA651/00', 'AA652/00', 'AA653/00', 'AA654/00', 'AA655/00', 'AA656/00', 'AA657/00', 'AA658/00', 'AA659/00', 'AA660/00', 'AA661/00', 'AA662/00', 'AA663/00', 'AA664/00', 'AA665/00', 'AA666/00', 'AA667/00', 'AA668/00', 'AA669/00', 'AA670/00', 'AA671/00', 'AA672/00', 'AA673/00', 'AA674/00', 'AA675/00', 'AA676/00', 'AA677/00', 'AA678/00', 'AA679/00', 'AA680/00', 'AA681/00', 'AA682/00', 'AA683/00', 'AA684/00', 'AA685/00', 'AA686/00', 'AA687/00', 'AA688/00', 'AA689/00', 'AA690/00', 'AA691/00', 'AA692/00', '... 161 more'],
                u'packed': ['AA875/00', 'AA876/00', 'AA877/00'],
                u'pick_slip_printed': ['AA854/00', 'AA855/00', 'AA856/00', 'AA857/00', 'AA858/00', 'AA859/00', 'AA860/00', 'AA861/00', 'AA862/00', 'AA863/00', 'AA864/00', 'AA865/00', 'AA866/00', 'AA867/00', 'AA868/00', 'AA869/00', 'AA870/00', 'AA871/00', 'AA872/00', 'AA873/00', 'AA874/00']},
            u'can_ship_tomorrow': {
                u'ready_to_print': ['AA627/00', 'AA628/00', 'AA629/00'],
                u'packed': [],
                u'pick_slip_printed': ['AA630/00', 'AA700/00', 'AA632/00'],
            },
        }
        self.call_service(shipping_station,
                          order_type,
                          expected_result,
                         )


    def test5(self):
        shipping_station = 'all'
        order_type = 'signature_service'
        expected_result = {
            u'should_ship_today': {
                u'ready_to_print': ['AA101/00', 'AA102/00', 'AA103/00', 'AA104/00', 'AA105/00', 'AA106/00', 'AA107/00', 'AA108/00', 'AA109/00', 'AA110/00', 'AA111/00', 'AA112/00', 'AA113/00', 'AA114/00', 'AA115/00', 'AA116/00', 'AA117/00', 'AA118/00', 'AA119/00', 'AA120/00', 'AA121/00', 'AA122/00', 'AA123/00', 'AA124/00', 'AA125/00', 'AA126/00', 'AA127/00', 'AA128/00', 'AA129/00', 'AA130/00', 'AA131/00', 'AA132/00', 'AA133/00', 'AA134/00', 'AA135/00', 'AA136/00', 'AA137/00', 'AA138/00', 'AA139/00', 'AA140/00', 'AA141/00', 'AA142/00', 'AA143/00', 'AA144/00', 'AA145/00', 'AA146/00', 'AA147/00', 'AA148/00', 'AA149/00', 'AA150/00', 'AA151/00', 'AA152/00', 'AA153/00', 'AA154/00', 'AA155/00', 'AA156/00', 'AA157/00', 'AA158/00', 'AA159/00', 'AA160/00', '... 471 more'],
                u'packed': ['AA586/00', 'AA587/00', 'AA588/00', 'AB046/00', 'AB047/00', 'AB279/00', 'AB280/00', 'AB281/00', 'AB282/00', 'AB283/00'],
                u'pick_slip_printed': ['AA576/00', 'AA577/00', 'AA578/00', 'AA579/00', 'AA580/00', 'AA581/00', 'AA582/00', 'AA583/00', 'AA584/00', 'AA585/00', 'AB029/00', 'AB030/00', 'AB031/00', 'AB032/00', 'AB033/00', 'AB034/00', 'AB035/00', 'AB036/00', 'AB037/00', 'AB038/00', 'AB039/00', 'AB040/00', 'AB041/00', 'AB042/00', 'AB043/00', 'AB044/00', 'AB045/00', 'AB277/00', 'AB278/00']},
            u'can_ship_tomorrow': {
                u'ready_to_print': ['AA024/00', 'AA025/00', 'AA026/00', 'AA027/00', 'AA028/00', 'AA029/00', 'AA030/00', 'AA031/00', 'AA032/00', 'AA033/00', 'AA034/00', 'AA035/00', 'AA036/00', 'AA037/00', 'AA038/00', 'AA039/00', 'AA040/00', 'AA041/00', 'AA042/00', 'AA043/00', 'AA044/00', 'AA045/00', 'AA046/00', 'AA047/00', 'AA048/00', 'AA049/00', 'AA050/00', 'AA051/00', 'AA052/00', 'AA053/00', 'AA054/00', 'AA055/00', 'AA056/00', 'AA057/00', 'AA058/00', 'AA059/00', 'AA060/00', 'AA061/00', 'AA062/00', 'AA063/00', 'AA064/00', 'AA065/00', 'AA066/00', 'AA914/00', 'AA915/00', 'AA916/00', 'AA917/00', 'AA918/00', 'AA919/00', 'AA920/00', 'AA921/00', 'AA922/00', 'AA923/00', 'AA924/00', 'AA925/00', 'AA926/00', 'AA927/00', 'AA928/00', 'AA929/00', 'AA930/00', '... 67 more'],
                u'packed': ['AA100/00', 'AA993/00', 'AA994/00', 'AA995/00', 'AA996/00', 'AA997/00', 'AA998/00', 'AA999/00', 'AB248/00', 'AB249/00'],
                u'pick_slip_printed': ['AA067/00', 'AA068/00', 'AA069/00', 'AA070/00', 'AA071/00', 'AA072/00', 'AA073/00', 'AA074/00', 'AA075/00', 'AA076/00', 'AA077/00', 'AA078/00', 'AA079/00', 'AA080/00', 'AA081/00', 'AA082/00', 'AA083/00', 'AA084/00', 'AA085/00', 'AA086/00', 'AA087/00', 'AA088/00', 'AA089/00', 'AA090/00', 'AA091/00', 'AA092/00', 'AA093/00', 'AA094/00', 'AA095/00', 'AA096/00', 'AA097/00', 'AA098/00', 'AA099/00', 'AA979/00', 'AA980/00', 'AA981/00', 'AA982/00', 'AA983/00', 'AA984/00', 'AA985/00', 'AA986/00', 'AA987/00', 'AA988/00', 'AA989/00', 'AA990/00', 'AA991/00', 'AA992/00'],
            },
        }
        self.call_service(shipping_station,
                          order_type,
                          expected_result,
                         )

    def test6(self):
        shipping_station = 'all'
        order_type = 'normal'
        expected_result = {
            u'should_ship_today': {
                u'ready_to_print': ['AA633/00', 'AA640/00', 'AA635/00', 'AA700/00', 'AA637/00', 'AA638/00', 'AA639/00', 'AA710/00', 'AA641/00', 'AA642/00', 'AA643/00', 'AA644/00', 'AA645/00', 'AA646/00', 'AA647/00', 'AA648/00', 'AA649/00', 'AA650/00', 'AA651/00', 'AA652/00', 'AA653/00', 'AA654/00', 'AA655/00', 'AA656/00', 'AA657/00', 'AA658/00', 'AA659/00', 'AA660/00', 'AA661/00', 'AA662/00', 'AA663/00', 'AA664/00', 'AA665/00', 'AA666/00', 'AA667/00', 'AA668/00', 'AA669/00', 'AA670/00', 'AA671/00', 'AA672/00', 'AA673/00', 'AA674/00', 'AA675/00', 'AA676/00', 'AA677/00', 'AA678/00', 'AA679/00', 'AA680/00', 'AA681/00', 'AA682/00', 'AA683/00', 'AA684/00', 'AA685/00', 'AA686/00', 'AA687/00', 'AA688/00', 'AA689/00', 'AA690/00', 'AA691/00', 'AA692/00', '... 301 more'],
                u'packed': ['AA875/00', 'AA876/00', 'AA877/00', 'AB219/00', 'AB355/00'],
                u'pick_slip_printed': ['AA854/00', 'AA855/00', 'AA856/00', 'AA857/00', 'AA858/00', 'AA859/00', 'AA860/00', 'AA861/00', 'AA862/00', 'AA863/00', 'AA864/00', 'AA865/00', 'AA866/00', 'AA867/00', 'AA868/00', 'AA869/00', 'AA870/00', 'AA871/00', 'AA872/00', 'AA873/00', 'AA874/00', 'AB211/00', 'AB212/00', 'AB213/00', 'AB214/00', 'AB215/00', 'AB216/00', 'AB217/00', 'AB218/00', 'AB334/00', 'AB335/00', 'AB336/00', 'AB337/00', 'AB338/00', 'AB339/00', 'AB340/00', 'AB341/00', 'AB342/00', 'AB343/00', 'AB344/00', 'AB345/00', 'AB346/00', 'AB347/00', 'AB348/00', 'AB349/00', 'AB350/00', 'AB351/00', 'AB352/00', 'AB353/00', 'AB354/00']},
            u'can_ship_tomorrow': {
                u'ready_to_print': ['AA627/00', 'AA628/00', 'AA629/00', 'AB089/00', 'AB090/00', 'AB091/00', 'AB092/00', 'AB093/00', 'AB094/00', 'AB095/00', 'AB096/00', 'AB097/00', 'AB098/00', 'AB099/00', 'AB100/00', 'AB101/00', 'AB102/00', 'AB103/00', 'AB104/00', 'AB298/00', 'AB299/00'],
                u'packed': [],
                u'pick_slip_printed': ['AA630/00', 'AA700/00', 'AA632/00'],
            },
        }
        self.call_service(shipping_station,
                          order_type,
                          expected_result,
                         )


class ShopfloorMonitorOrderNumbersServiceBackorder(ShopfloorMonitorOrderNumbersService):
    def __init__(self):
        ShopfloorMonitorOrderNumbersService.__init__(self)
        self.show_backorder = "true"


class TestShopfloorMonitorOrderNumbersServiceBackorder(ShopfloorMonitorOrderNumbersServiceBackorder):
    def __init__(self):
        ShopfloorMonitorOrderNumbersServiceBackorder.__init__(self)

    def test1(self):
        shipping_station = 'wcc'
        order_type = 'today_sure'
        expected_result = {
            u'backorder': {
                u'ready_to_print': ['CA000/01', 'CA001/01', 'CA002/01', 'CA003/01', 'CA004/01'],
                u'packed': [],
                u'pick_slip_printed': ['CA005/01'],
            },
        }
        self.call_service(shipping_station,
                          order_type,
                          expected_result,
                         )

    def test2(self):
        shipping_station = 'wcc'
        order_type = 'signature_service'
        expected_result = {
            u'backorder': {
                u'ready_to_print': ['CA024/01', 'CA025/01', 'CA026/01', 'CA027/01', 'CA028/01', 'CA029/01', 'CA030/01', 'CA031/01', 'CA032/01', 'CA033/01', 'CA034/01', 'CA035/01', 'CA036/01', 'CA037/01', 'CA038/01', 'CA039/01', 'CA040/01', 'CA041/01', 'CA042/01', 'CA043/01', 'CA044/01', 'CA045/01', 'CA046/01', 'CA047/01', 'CA048/01', 'CA049/01', 'CA050/01', 'CA051/01', 'CA052/01', 'CA053/01', 'CA054/01', 'CA055/01', 'CA056/01', 'CA057/01', 'CA058/01', 'CA059/01', 'CA060/01', 'CA061/01', 'CA062/01', 'CA063/01', 'CA064/01', 'CA065/01', 'CA066/01', 'CA067/01', 'CA068/01', 'CA069/01', 'CA070/01', 'CA071/01', 'CA072/01', 'CA073/01', 'CA074/01', 'CA075/01', 'CA076/01', 'CA077/01', 'CA078/01', 'CA079/01', 'CA080/01'],
                u'packed': ['CA097/01', 'CA098/01', 'CA099/01'],
                u'pick_slip_printed': ['CA081/01', 'CA082/01', 'CA083/01', 'CA084/01', 'CA085/01', 'CA086/01', 'CA087/01', 'CA088/01', 'CA089/01', 'CA090/01', 'CA091/01', 'CA092/01', 'CA093/01', 'CA094/01', 'CA095/01', 'CA096/01'],
            },
        }
        self.call_service(shipping_station,
                          order_type,
                          expected_result,
                         )

    def test3(self):
        shipping_station = 'wcc'
        order_type = 'service_file'
        expected_result = {
            u'backorder': {
                u'ready_to_print': ['CA605/01', 'CA606/01', 'CA607/01', 'CA608/01', 'CA609/01', 'CA610/01'],
                u'packed': ['CA625/01'],
                u'pick_slip_printed': ['CA611/01', 'CA612/01', 'CA613/01', 'CA614/01', 'CA615/01', 'CA616/01', 'CA617/01', 'CA618/01', 'CA619/01', 'CA620/01', 'CA621/01', 'CA622/01', 'CA623/01', 'CA624/01'],
            },
        }
        self.call_service(shipping_station,
                          order_type,
                          expected_result,
                         )

    def test4(self):
        shipping_station = 'wcc'
        order_type = 'normal'
        expected_result = {
            u'backorder': {
                u'ready_to_print': ['CA627/01', 'CA628/01', 'CA629/01', 'CA630/01'],
                u'packed': [],
                u'pick_slip_printed': ['CA700/01'],
            },
        }
        self.call_service(shipping_station,
                          order_type,
                          expected_result,
                         )


    def test5(self):
        shipping_station = 'all'
        order_type = 'signature_service'
        expected_result = {
            u'backorder': {
                u'ready_to_print': ['CA024/01', 'CA025/01', 'CA026/01', 'CA027/01', 'CA028/01', 'CA029/01', 'CA030/01', 'CA031/01', 'CA032/01', 'CA033/01', 'CA034/01', 'CA035/01', 'CA036/01', 'CA037/01', 'CA038/01', 'CA039/01', 'CA040/01', 'CA041/01', 'CA042/01', 'CA043/01', 'CA044/01', 'CA045/01', 'CA046/01', 'CA047/01', 'CA048/01', 'CA049/01', 'CA050/01', 'CA051/01', 'CA052/01', 'CA053/01', 'CA054/01', 'CA055/01', 'CA056/01', 'CA057/01', 'CA058/01', 'CA059/01', 'CA060/01', 'CA061/01', 'CA062/01', 'CA063/01', 'CA064/01', 'CA065/01', 'CA066/01', 'CA067/01', 'CA068/01', 'CA069/01', 'CA070/01', 'CA071/01', 'CA072/01', 'CA073/01', 'CA074/01', 'CA075/01', 'CA076/01', 'CA077/01', 'CA078/01', 'CA079/01', 'CA080/01', 'CA914/01', 'CA915/01', 'CA916/01', '... 91 more'],
                u'packed': ['CA097/01', 'CA098/01', 'CA099/01', 'CB248/01'],
                u'pick_slip_printed': ['CA081/01', 'CA082/01', 'CA083/01', 'CA084/01', 'CA085/01', 'CA086/01', 'CA087/01', 'CA088/01', 'CA089/01', 'CA090/01', 'CA091/01', 'CA092/01', 'CA093/01', 'CA094/01', 'CA095/01', 'CA096/01', 'CA989/01', 'CA990/01', 'CA991/01', 'CA992/01', 'CA993/01', 'CA994/01', 'CA995/01', 'CA996/01', 'CA997/01', 'CA998/01'],
            },
        }
        self.call_service(shipping_station,
                          order_type,
                          expected_result,
                         )

    def test6(self):
        shipping_station = 'all'
        order_type = 'normal'
        expected_result = {
            u'backorder': {
                u'ready_to_print': ['CA627/01', 'CA628/01', 'CA629/01', 'CA630/01', 'CB089/01', 'CB090/01', 'CB091/01', 'CB092/01', 'CB093/01', 'CB094/01', 'CB095/01', 'CB096/01', 'CB097/01', 'CB098/01', 'CB099/01', 'CB100/01', 'CB101/01', 'CB102/01', 'CB103/01', 'CB298/01', 'CB299/01', 'CB299/02'],
                u'packed': [],
                u'pick_slip_printed': ['CA700/01'],
            },
        }
        self.call_service(shipping_station,
                          order_type,
                          expected_result,
                         )
