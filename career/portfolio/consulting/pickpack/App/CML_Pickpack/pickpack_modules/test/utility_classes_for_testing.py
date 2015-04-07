"""
Utility and support classes for testing

    utility_classes_for_testing.py

"""

import pprint, itertools, collections
from nose import tools

from CML_Pickpack.pickpack_modules import pickpack_data_mock
from CML_Pickpack.pickpack_modules import pickpack_errors
from CML_Pickpack.pickpack_modules import pickpack_constants
from CML_Pickpack.pickpack_modules import pickpack_utility_classes
from CML_Pickpack.pickpack_modules.warn.main import calculateShipmentWarnings
#from CML_Pickpack.pickpack_modules.test import utility_functions_for_testing


class BaseRuleset(object):
    """
    Base class  for test classes that test Rulesets
    """
    def __init__(self):
        pass


class BaseSpecialRuleset(BaseRuleset):
    """
    Base for test classes that test SpecialRuleset classes
    """
    def __init__(self):
        BaseRuleset.__init__(self)


class BaseItemRuleset(BaseRuleset):
    """
    Base for test classes that test ItemRuleset classes
    """
    # out stands for "Object under test". In derived classes, we define this at
    # class level, so we only build it once, and reuse it many times, just as is
    # done in the real application.
    out = None

    Air = 100000
    Ground = 100001

    def __init__(self):
        BaseRuleset.__init__(self)

    def _run_apply_rules(self,
                         counter,
                         expected_result_air,
                         expected_result_ground,
                        ):
        self._run(counter,
                  self.Air,
                  expected_result_air,
                 )
        self._run(counter,
                  self.Ground,
                  expected_result_ground,
                 )

    def _run(self,
             counter,
             ship_code,
             expected_result,
            ):
        actual_result = self.out.apply_rules(counter,
                                             ship_code,
                                            )

        if actual_result is None:
            raise pickpack_errors.ApplicationError("Error: Warning is None")

        tools.assert_is_instance(actual_result, expected_result)

    @staticmethod
    def _run_with_exception(function_to_run,
                            expected_exception_msg,
                            *args,
                            **kwargs
                           ):

        with tools.assert_raises(pickpack_errors.ApplicationError) as context_mgr:
            function_to_run(*args,
                            **kwargs
                           )

        exception = context_mgr.exception
        print
        print "exception.message"
        print exception.message
        tools.assert_equal(exception.message,
                           expected_exception_msg,
                          )


class BaseItemRulesetTester(BaseItemRuleset):
    """
    Common tests to run against all Rulesets
    """
    def __init__(self):
        BaseItemRuleset.__init__(self)


class MultiDictBackedRuleset(BaseItemRulesetTester):
    """
    Some Rulesets just use a plain old python dict as their data store. Others
    use a custom object, an instance of MultiDict. This is the base class for
    classes that test Rulesets that use MultiDict as a data store.
    """
    def __init__(self):
        BaseItemRulesetTester.__init__(self)
        self.allowed_completeness_exception = None
        self.allowed_collision_exception = None

    def test_for_completeness(self):
        if self.allowed_completeness_exception:
            self._run_with_exception(self._test_for_completeness,
                                     self.allowed_completeness_exception,
                                    )
        else:
            self._test_for_completeness()

    def test_for_collision(self):
        if self.allowed_collision_exception:
            self._run_with_exception(self._test_for_collision,
                                     self.allowed_collision_exception,
                                    )
        else:
            self._test_for_collision()

    def _test_for_completeness(self):
        """
        This is called only in tests. It checks all the keys in
        self.out.ruleset.reference_dict against the whole set of combinatorial
        possibilities. It makes sure that all possible cases are covered by one
        of the reference keys in self.out.ruleset.reference_dict.
        """
        combinatorial_space = list(itertools.product(*self.out.ruleset.combinatorial_dimensions))
        reference_keys = self.out.ruleset.reference_dict.keys()
        rule_names = {}
        reference_counter = 0

        for reference_key in reference_keys:
            # Each reference key is a tuple. The elements of the tuple are
            # integers or tuples of integers. Here we wrap all the integer
            # elements inside tuples, so all the elements of prepared_ref_key
            # are iterable.
            prepared_ref_key = itertools.imap(self.wrapScalarValueAndSort,
                                              reference_key,
                                             )

            # Here we take the "distilled" reference key and explode it in to
            # keys which are tuples of integers (all the elements are integers,
            # no elements are tuples).
            for exploded_key in itertools.product(*prepared_ref_key):
                # If we have overlap in the keys, this will catch it and output
                # some useful information.
                base_key = self.out.ruleset[exploded_key]
                try:
                    # Test items have a "marker_value"
                    marker_value = base_key.marker_value
                except AttributeError:
                    # Production items do not have "marker_value"
                    marker_value = base_key
                diagnosic_info = (marker_value,
                                  reference_counter,
                                  reference_keys[reference_counter],
                                 )
                if rule_names.has_key(exploded_key):
                    rule_names[exploded_key].append(diagnosic_info)
                else:
                    rule_names[exploded_key] = [diagnosic_info]

                try:
                    combinatorial_space.remove(exploded_key)
                except ValueError:
                    print "Duplicate exploded key. Rule that was violated: %s" % self.out.ruleset[exploded_key].marker_value
                    #raise pickpack_errors.ApplicationError("Exploded key not found %s " % str(exploded_key))
            # end innner loop

            reference_counter += 1
        # end outer loop

        print "Duplicate exploded keys, and their source"
        duplicate_found = False
        for key, value in rule_names.items():
            if len(value) > 1:
                print "Key %s" % str(key)
                print "Value"
                pprint.pprint(value, width = 100)
                duplicate_found = True
        if duplicate_found:
            raise pickpack_errors.ApplicationError("Duplicate reference keys found")

        if len(combinatorial_space) != 0:
            raise pickpack_errors.ApplicationError("The reference keys do not cover the entire combinatorial space. %s slots left over." % len(combinatorial_space))

    def _test_for_collision(self):
        """
        This is called only in tests. It checks all the keys in
        self.out.ruleset.reference_dict. It raises an error if any two keys are
        found that are not mutually exclusive. That is, if a candidate key could
        match more than one reference key in self.out.ruleset.reference_dict.
        """

        def _compare(reference_key_element1,
                     reference_key_element2,
                    ):
            if (isinstance(reference_key_element1, frozenset)
                and isinstance(reference_key_element2, frozenset)
               ):
                result = not reference_key_element1.isdisjoint(reference_key_element2)
            elif (isinstance(reference_key_element1, frozenset)
                  and isinstance(reference_key_element2, int)
                 ):
                result = reference_key_element2 in reference_key_element1
            elif (isinstance(reference_key_element1, int)
                  and isinstance(reference_key_element2, frozenset)
                 ):
                result = reference_key_element1 in reference_key_element2
            elif (isinstance(reference_key_element1, int)
                  and isinstance(reference_key_element2, int)
                 ):
                result = (reference_key_element1 == reference_key_element2)
            else:
                raise pickpack_errors.ApplicationError("Invalid reference key elements %s %s" % (str(reference_key_element1),
                                                                            str(reference_key_element2),
                                                                           )
                                 )
            return result

        reference_keys = self.out.ruleset.reference_dict.keys()

        for reference_key1, reference_key2 in itertools.combinations(reference_keys, 2):
            if len(reference_key1) != len(reference_key2):
                raise pickpack_errors.ApplicationError("All keys must be the same length %s %s" % (reference_key1, reference_key2))

            match = all(_compare(r1, r2) for r1, r2 in itertools.izip(reference_key1, reference_key2))
            if match:
                raise pickpack_errors.ApplicationError("These two keys are not mutually exclusive %s %s" % (reference_key1, reference_key2))

    @staticmethod
    def wrapScalarValueAndSort(value):
        """
        If a single (scalar) value was passed in, wrap it inside a one-element
        tuple. If a sequence was passed in, return it unchanged. If a set or
        frozenset was passed, in turn it in to a list, and sort it.
        """
        if isinstance(value, (bool, int, float, str, long)):
            return [value]
        elif isinstance(value, (set, frozenset)):
            a = list(value)
            # Sort the list so the test always runs with inputs in the same order.
            a.sort()
            return a
        else:
            return value


class BaseMainTester(object):
    """
    Base class for test classes for warn.main
    """
    def __init__(self):
        pass

    def _try_it(self,
                order_info,
                packing_list,
                expected_warnings,
                expected_inline_images,
                expected_warning_categories,
                no_warning = False,
                ctx = None,
                #add_seasonal_warning = False,
               ):
        """
        Run a test, expecting a result

        If no warning is expected, do not provide values for expected_warnings
        and expected_inline_images. Instead, specify no_warning = True.
        """
        if no_warning:
            if (expected_warnings is not None
                or expected_inline_images is not None
               ):
                raise pickpack_errors.ApplicationError(
                    "no_warning is True, but values were supplied"
                    " for expected_warnings or expected_inline_images"
                )

        #if add_seasonal_warning:
        #    # In season, modify expected_warnings in place.
        #    self.add_seasonal_warning(expected_warnings)

        # Make sure our mock data does not have duplicate row ids.
        bag = collections.Counter(packing_list.get_column("line_no"))
        duplicate_row_ids = [i for i in bag if bag[i] > 1]
        if duplicate_row_ids:
            raise pickpack_errors.ApplicationError("Duplicate row ids found %s" % duplicate_row_ids)

        actual_result = calculateShipmentWarnings(packing_list,
                                                  order_info['carrier_code'],
                                                  order_info['customer_number'],
                                                  #order_info['order_entry_initials'],
                                                  order_info.get('calcualted_order_weight', 10),
                                                  order_info.get('service_level', 'N'),
                                                  order_info.get('ship_to_state', 'WI'),
                                                  order_info.get('ship_to_country', pickpack_constants.UNITED_STATES_COUNTRY_CODE),
                                                  order_info.get('customer_sold_to_country', pickpack_constants.UNITED_STATES_COUNTRY_CODE),
                                                  ctx,
                                                 )
        (actual_warnings,
         actual_inline_images,
         actual_warning_categories,
        ) = self._parse_actual_result(actual_result)

        if no_warning:
            tools.assert_equal(actual_warnings, [])
            tools.assert_is_none(actual_inline_images)
            tools.assert_is_none(actual_warning_categories)
        else:
            tools.assert_equal(actual_warnings, expected_warnings)
            tools.assert_equal(actual_inline_images, expected_inline_images)
            tools.assert_equal(actual_warning_categories, expected_warning_categories)

    def try_it_exception(self,
                         order_info,
                         list_of_items,
                         expected_exception_msg,
                        ):
        """
        Run a test, expecting an exception
        """
        with tools.assert_raises(pickpack_errors.ApplicationError) as context_mgr:
            self._try_it(order_info,
                         pickpack_utility_classes.PackingListContainer(list_of_items),
                         None,
                         None,
                         None,
                        )

        exception = context_mgr.exception
        tools.assert_equal(exception.message,
                           expected_exception_msg,
                          )

    def try_it_order_id_scan(self,
                             order_id_scan,
                             expected_warnings = None,
                             expected_inline_images = None,
                             expected_warning_categories = None,
                             no_warning = False,
                             #add_seasonal_warning = False,
                            ):
        """
        Accepts a pretend order id scan, from pickpack_data_mock. Order id is a
        seven-character string, made up of the five-character order number, plus
        the order generation left-zero-padded to two characters. No slash
        separates the number and the generation. This is the format of the
        barcode on the pick slip.

        If no warning is expected, do not provide values for expected_warnings
        and expected_inline_images. Instead, specify no_warning = True.
        """
        # APlus order numbers are alphanumeric. So, we bust the whole order id
        # string to uppercase.
        order_id_scan = order_id_scan.upper()

        mock_order = pickpack_data_mock.MOCK_DATA[order_id_scan]

        packing_list = pickpack_data_mock.getPackingList(mock_order)

        self._try_it(mock_order['order_info'],
                     packing_list,
                     expected_warnings,
                     expected_inline_images,
                     expected_warning_categories,
                     no_warning = no_warning,
                     #add_seasonal_warning = add_seasonal_warning,
                    )

    def try_it_list_of_items(self,
                             order_info,
                             list_of_items,
                             expected_warnings,
                             expected_inline_images,
                             expected_warning_categories,
                             #add_seasonal_warning = False,
                            ):
        """
        Accepts order info, including a list of line items. Runs a test,
        expecting a result.
        """
        self._try_it(order_info,
                     pickpack_utility_classes.PackingListContainer(list_of_items),
                     expected_warnings,
                     expected_inline_images,
                     expected_warning_categories,
                     no_warning = False,
                     #add_seasonal_warning = add_seasonal_warning,
                    )

    @staticmethod
    def _parse_actual_result(result):
        (warnings,
         inline_images,
         categories,
        ) = result

        actual_warnings = [[warning.note_text,
                            warning.image_names,
                           ] for warning in warnings
                          ]

        return (actual_warnings,
                inline_images,
                categories,
               )

    #@staticmethod
    #def ecommerce_promotion_is_active():
    #    """
    #    Passthrough
    #    """
    #    return utility_functions_for_testing.ecommerce_promotion_is_active()

    #def add_seasonal_warning(self, expected_warnings):
    #    """
    #    If it is the season for seasonal notifications such as the Gas Rebate
    #    form, then add those seasonal warnings to the list of expected_warnings.
    #    Modifies the expected_warnings list in place.
    #    """
    #    if self.ecommerce_promotion_is_active():
    #        expected_warnings.append(['Include Gas Purchase Mail-In Rebate Form.', 'dollar_sign'])


# Note: If we don't use nose's twisted integration, the defereds will raise
# errors, but nose will not count them in the overall pass/fail.
#
#class HandleableServerException(object):
#    """
#    Sometimes the server returns an error message to the client that the client
#    can handle gracefully. Test the server side generation of such errors.
#    """
#
#    def __init__(self,
#                 order_id_scan,
#                 expected_error_message,
#                ):
#        self.order_id_scan = order_id_scan
#        self.expected_error_message = expected_error_message
#
#    def try_handleable_server_error(self):
#        """
#        Run a test, expecting a handleable server error.
#        """
#        deferred = pickpack_data_mock.getPackingList_deferred(self.order_id_scan,
#                                                              None,
#                                                             )
#        deferred.addCallback(self.try_handleable_server_error_deferred)
#        return deferred
#
#    def try_handleable_server_error_deferred(self,
#                                             result,
#                                            ):
#        """
#        Handle the result of the deferred. Make sure it matches the expected
#        result.
#        """
#        actual_error_message = result['server_error']
#        tools.assert_equal(self.expected_error_message,
#                           actual_error_message,
#                          )
