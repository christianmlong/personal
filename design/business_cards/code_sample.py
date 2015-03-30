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




    def bla_bla_bla(self):

# Use code below this line
# ===========================================================

        if self.allowed_collision_exception:
            self._run_with_exception(self._test_for_collision,
                                     self.allowed_collision_exception,
                                    )
        else:
            self._test_for_collision()

    if self.allowed_collision_exception:
        self.run_with_exception(self.test_for_collision,
                                self.allowed_collision_exception,
                               )
    else:
        self.test_for_collision()

    def test_for_completeness(self):
        """
        Check all the keys in self.out.ruleset.reference_dict against the whole set
        of possibilities. Make sure that all possible cases are covered by one of
        the reference keys in self.out.ruleset.reference_dict.
        """
        key_space = list(itertools.product(*self.out.ruleset.dimensions))
        reference_keys = self.out.ruleset.reference_dict.keys()

        for reference_key in reference_keys:
            # Each reference key is a tuple. The elements of the tuple are integers
            # or tuples of integers. Wrap all the integer elements inside tuples, so
            # all the elements of prepared_ref_key are iterable.
            prepared_ref_key = itertools.imap(self.wrapScalarValueAndSort,
                                              reference_key,
                                             )

            # Take the distilled reference key and explode it in to keys which are
            # tuples of integers.
            for exploded_key in itertools.product(*prepared_ref_key):
                # If we have overlap in the keys, this will catch it.
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
                    raise pickpack_errors.ApplicationError("Exploded key not found %s " % str(exploded_key))


# ===========================================================
# Use code above this line

            # etc etc
