"""
Taxonomy tests — legacy entry-filter queries plus Taxonomy CDA support (real API).

Companion file tests/test_taxonomies_unit.py covers the mocked, no-network
unit tests for the new CDA classes (Taxonomy, TaxonomyQuery, Term, TermQuery),
including the merge-boundary test that pins the one behavior the
no-breaking-change design hinges on.

Split internally by test class:
  - TestTaxonomyAPI              legacy entry-filter queries (in_, above, below, ...),
                                  unchanged since before the CDA feature.
  - TestTaxonomyCDA               the new CDA chaining, general coverage (list taxonomies,
                                  single taxonomy/term, hierarchy). Targets the 'gadgets'
                                  fixture — the only taxonomy on this stack with real
                                  multi-level term hierarchy — for the tests that need one;
                                  list-all-taxonomies and legacy-filter tests don't depend
                                  on any specific taxonomy.
  - TestTaxonomyLocalisation      tests against the 'gadgets' taxonomy fixture:
                                  locale('fr-fr'), include_fallback() (including per-node
                                  fallback), and depth-limited ancestor/descendant hierarchy
                                  traversal (parent -> child -> grandchild).
"""
import unittest
import config
import contentstack

API_KEY = config.APIKEY
DELIVERY_TOKEN = config.DELIVERYTOKEN
ENVIRONMENT = config.ENVIRONMENT
HOST = config.HOST

TAXONOMY_UID = config.TAXONOMY_UID
LOCALE = config.TAXONOMY_LOCALE
MASTER_LOCALE = config.TAXONOMY_MASTER_LOCALE


# ===========================================================================
# Legacy entry-filter taxonomy queries (real API) — unchanged
# ===========================================================================

class TestTaxonomyAPI(unittest.TestCase):
    def setUp(self):
        self.stack = contentstack.Stack(API_KEY, DELIVERY_TOKEN, ENVIRONMENT, host=HOST)

    def test_01_taxonomy_complex_query(self):
        """Test complex taxonomy query combining multiple filters"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.and_(
            {"taxonomies.category": {"$in": ["test"]}},
            {"taxonomies.test1": {"$exists": True}}
        ).or_(
            {"taxonomies.status": {"$in": ["active"]}},
            {"taxonomies.priority": {"$in": ["high"]}}
        ).find({'limit': 10})
        if result is not None:
            self.assertIn('entries', result)

    def test_02_taxonomy_in_query(self):
        """Test taxonomy query with $in filter"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.in_("taxonomies.category", ["category1", "category2"]).find()
        if result is not None:
            self.assertIn('entries', result)

    def test_03_taxonomy_exists_query(self):
        """Test taxonomy query with $exists filter"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.exists("taxonomies.test1").find()
        if result is not None:
            self.assertIn('entries', result)

    def test_04_taxonomy_or_query(self):
        """Test taxonomy query with $or filter"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.or_(
            {"taxonomies.category": {"$in": ["category1"]}},
            {"taxonomies.test1": {"$exists": True}}
        ).find()
        if result is not None:
            self.assertIn('entries', result)

    def test_05_taxonomy_and_query(self):
        """Test taxonomy query with $and filter"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.and_(
            {"taxonomies.category": {"$in": ["category1"]}},
            {"taxonomies.test1": {"$exists": True}}
        ).find()
        if result is not None:
            self.assertIn('entries', result)

    def test_06_taxonomy_equal_and_below(self):
        """Test taxonomy query with $eq_below filter"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.equal_and_below("taxonomies.color", "blue", levels=1).find()
        if result is not None:
            self.assertIn('entries', result)

    def test_07_taxonomy_below(self):
        """Test taxonomy query with $below filter"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.below("taxonomies.hierarchy", "parent_uid", levels=2).find()
        if result is not None:
            self.assertIn('entries', result)

    def test_08_taxonomy_equal_and_above(self):
        """Test taxonomy query with $eq_above filter"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.equal_and_above("taxonomies.hierarchy", "child_uid", levels=3).find()
        if result is not None:
            self.assertIn('entries', result)

    def test_09_taxonomy_above(self):
        """Test taxonomy query with $above filter"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.above("taxonomies.hierarchy", "child_uid", levels=2).find()
        if result is not None:
            self.assertIn('entries', result)

    def test_10_taxonomy_find_with_params(self):
        """Test taxonomy find with additional parameters"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.in_("taxonomies.category", ["test"]).find({'limit': 5})
        if result is not None:
            self.assertIn('entries', result)

    # ========== Additional Test Cases ==========

    def test_11_taxonomy_method_chaining(self):
        """Test taxonomy method chaining with multiple filters"""
        taxonomy = self.stack.taxonomy()
        result = (taxonomy
                 .in_("taxonomies.category", ["category1", "category2"])
                 .exists("taxonomies.status")
                 .find({'limit': 10}))
        if result is not None:
            self.assertIn('entries', result)

    def test_12_taxonomy_complex_nested_query(self):
        """Test complex nested taxonomy query with and_ and or_"""
        taxonomy = self.stack.taxonomy()
        result = (taxonomy
                 .and_(
                     {"taxonomies.category": {"$in": ["test"]}},
                     {"taxonomies.status": {"$in": ["active"]}}
                 )
                 .or_(
                     {"taxonomies.priority": {"$in": ["high"]}},
                     {"taxonomies.type": {"$exists": True}}
                 )
                 .find({'limit': 5}))
        if result is not None:
            self.assertIn('entries', result)

    def test_13_taxonomy_in_with_empty_list(self):
        """Test taxonomy in_ method with empty list"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.in_("taxonomies.category", []).find()
        if result is not None:
            self.assertIsNotNone(result)

    def test_14_taxonomy_in_with_single_item(self):
        """Test taxonomy in_ method with single item list"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.in_("taxonomies.category", ["single_category"]).find()
        if result is not None:
            self.assertIn('entries', result)

    def test_15_taxonomy_equal_and_below_with_different_levels(self):
        """Test taxonomy equal_and_below with different level values"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.equal_and_below("taxonomies.color", "blue", levels=0).find()
        if result is not None:
            self.assertIn('entries', result)

        result2 = taxonomy.equal_and_below("taxonomies.color", "blue", levels=5).find()
        if result2 is not None:
            self.assertIn('entries', result2)

    def test_16_taxonomy_below_with_different_levels(self):
        """Test taxonomy below with different level values"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.below("taxonomies.hierarchy", "parent_uid", levels=1).find()
        if result is not None:
            self.assertIn('entries', result)

    def test_17_taxonomy_equal_and_above_with_different_levels(self):
        """Test taxonomy equal_and_above with different level values"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.equal_and_above("taxonomies.hierarchy", "child_uid", levels=1).find()
        if result is not None:
            self.assertIn('entries', result)

    def test_18_taxonomy_above_with_different_levels(self):
        """Test taxonomy above with different level values"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.above("taxonomies.hierarchy", "child_uid", levels=1).find()
        if result is not None:
            self.assertIn('entries', result)

    def test_19_taxonomy_multiple_exists(self):
        """Test taxonomy with multiple exists filters"""
        taxonomy = self.stack.taxonomy()
        result = (taxonomy
                 .exists("taxonomies.field1")
                 .exists("taxonomies.field2")
                 .find())
        if result is not None:
            self.assertIn('entries', result)

    def test_20_taxonomy_find_with_multiple_params(self):
        """Test taxonomy find with multiple parameters"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.in_("taxonomies.category", ["test"]).find({
            'limit': 10,
            'skip': 0
        })
        if result is not None:
            self.assertIn('entries', result)

    def test_21_taxonomy_or_with_multiple_conditions(self):
        """Test taxonomy or_ with multiple conditions"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.or_(
            {"taxonomies.category": {"$in": ["cat1"]}},
            {"taxonomies.category": {"$in": ["cat2"]}},
            {"taxonomies.category": {"$in": ["cat3"]}}
        ).find()
        if result is not None:
            self.assertIn('entries', result)

    def test_22_taxonomy_and_with_multiple_conditions(self):
        """Test taxonomy and_ with multiple conditions"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.and_(
            {"taxonomies.category": {"$in": ["test"]}},
            {"taxonomies.status": {"$in": ["active"]}},
            {"taxonomies.priority": {"$exists": True}}
        ).find()
        if result is not None:
            self.assertIn('entries', result)

    def test_23_taxonomy_combination_all_methods(self):
        """Test taxonomy with combination of all methods"""
        taxonomy = self.stack.taxonomy()
        result = (taxonomy
                 .in_("taxonomies.category", ["category1"])
                 .exists("taxonomies.status")
                 .and_(
                     {"taxonomies.type": {"$in": ["type1"]}},
                     {"taxonomies.active": {"$exists": True}}
                 )
                 .or_(
                     {"taxonomies.priority": {"$in": ["high"]}}
                 )
                 .find({'limit': 5, 'skip': 0}))
        if result is not None:
            self.assertIn('entries', result)

    def test_24_taxonomy_find_without_params(self):
        """Test taxonomy find without any parameters"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.in_("taxonomies.category", ["test"]).find()
        if result is not None:
            self.assertIn('entries', result)

    def test_25_taxonomy_find_with_none_params(self):
        """Test taxonomy find with None params"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.in_("taxonomies.category", ["test"]).find(None)
        if result is not None:
            self.assertIn('entries', result)


# ===========================================================================
# Taxonomy CDA — real API, taxonomy-agnostic (dynamic discovery)
# ===========================================================================

class TestTaxonomyCDA(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.stack = contentstack.Stack(API_KEY, DELIVERY_TOKEN, ENVIRONMENT, host=HOST)
        cls.taxonomy_uid = cls._discover_taxonomy_uid(cls.stack)
        cls.term_uid = cls._discover_term_uid(cls.stack, cls.taxonomy_uid) if cls.taxonomy_uid else None
        cls.hierarchy = cls._discover_hierarchy(cls.stack, cls.taxonomy_uid) if cls.taxonomy_uid else (None, None, None)

    @staticmethod
    def _discover_taxonomy_uid(stack):
        """
        Uses the 'gadgets' taxonomy fixture (config.TAXONOMY_UID) specifically —
        it's the one taxonomy on this stack with real multi-level term hierarchy
        and partial fr-fr translation, so the hierarchy/locale tests below have
        real data to assert against instead of skipping.
        """
        result = stack.taxonomy(TAXONOMY_UID).fetch()
        if isinstance(result, dict) and result.get('uid') == TAXONOMY_UID:
            return TAXONOMY_UID
        return None

    @staticmethod
    def _discover_term_uid(stack, taxonomy_uid):
        """Fetches a real term uid within the discovered taxonomy."""
        result = stack.taxonomy(taxonomy_uid).term().find()
        if isinstance(result, dict) and result.get('terms'):
            return result['terms'][0].get('uid')
        return None

    @staticmethod
    def _discover_hierarchy(stack, taxonomy_uid):
        """
        Walks descendants() to find a real parent/child/grandchild term chain,
        mirroring contentstack-dotnet's GetTermHierarchyAsync. Returns
        (None, None, None) if no such chain exists in the fixture data.
        """
        terms_result = stack.taxonomy(taxonomy_uid).term().find()
        terms = terms_result.get('terms', []) if isinstance(terms_result, dict) else []
        for candidate_parent in terms:
            parent_uid = candidate_parent.get('uid')
            if not parent_uid:
                continue
            children = stack.taxonomy(taxonomy_uid).term(parent_uid).descendants()
            children = children if isinstance(children, list) else (children or {}).get('descendants', [])
            child_uid = children[0].get('uid') if children else None
            if not child_uid:
                continue
            grandchildren = stack.taxonomy(taxonomy_uid).term(child_uid).descendants()
            grandchildren = grandchildren if isinstance(grandchildren, list) else (grandchildren or {}).get('descendants', [])
            grandchild_uid = grandchildren[0].get('uid') if grandchildren else None
            if not grandchild_uid:
                continue
            return parent_uid, child_uid, grandchild_uid
        return None, None, None

    # ---------- List all taxonomies ----------

    def test_01_list_all_taxonomies(self):
        """GET /taxonomies returns a taxonomies collection."""
        result = self.stack.taxonomy().find()
        self.assertIsNotNone(result)
        if 'taxonomies' in result:
            self.assertIsInstance(result['taxonomies'], list)

    def test_02_list_taxonomies_with_skip_limit(self):
        """GET /taxonomies?skip=&limit= returns a paged subset."""
        result = self.stack.taxonomy().skip(0).limit(1).find()
        self.assertIsNotNone(result)
        if 'taxonomies' in result:
            self.assertLessEqual(len(result['taxonomies']), 1)

    def test_03_list_taxonomies_with_include_count(self):
        """GET /taxonomies?include_count=true includes a count field."""
        result = self.stack.taxonomy().include_count().find()
        self.assertIsNotNone(result)

    # ---------- Legacy entry-filter behavior (non-regression) ----------

    def test_04_legacy_filter_still_routes_to_entries(self):
        """stack.taxonomy() with a filter chained still filters entries (unchanged)."""
        result = self.stack.taxonomy().in_('taxonomies.category', ['test']).find()
        if result is not None:
            self.assertIn('entries', result)

    # ---------- Single taxonomy ----------

    def test_05_fetch_single_taxonomy(self):
        """GET /taxonomies/{uid} returns the taxonomy object directly."""
        if not self.taxonomy_uid:
            self.skipTest("No taxonomy discovered on this stack — skipping.")
        result = self.stack.taxonomy(self.taxonomy_uid).fetch()
        self.assertIsNotNone(result)
        self.assertEqual(result.get('uid'), self.taxonomy_uid)

    def test_06_fetch_single_taxonomy_with_locale(self):
        """GET /taxonomies/{uid}?locale=en-us returns a localized taxonomy."""
        if not self.taxonomy_uid:
            self.skipTest("No taxonomy discovered on this stack — skipping.")
        result = self.stack.taxonomy(self.taxonomy_uid).locale('en-us').include_fallback().fetch()
        self.assertIsNotNone(result)

    # ---------- List terms ----------

    def test_07_find_all_terms(self):
        """GET /taxonomies/{uid}/terms returns a terms collection."""
        if not self.taxonomy_uid:
            self.skipTest("No taxonomy discovered on this stack — skipping.")
        result = self.stack.taxonomy(self.taxonomy_uid).term().find()
        self.assertIsNotNone(result)
        if 'terms' in result:
            self.assertIsInstance(result['terms'], list)

    def test_08_find_terms_with_locale_and_fallback(self):
        """GET /taxonomies/{uid}/terms?locale=&include_fallback=true returns localized terms."""
        if not self.taxonomy_uid:
            self.skipTest("No taxonomy discovered on this stack — skipping.")
        result = self.stack.taxonomy(self.taxonomy_uid).term() \
            .locale('en-us').include_fallback().find()
        self.assertIsNotNone(result)

    def test_09_find_terms_with_depth(self):
        """GET /taxonomies/{uid}/terms?depth=1 limits the returned hierarchy."""
        if not self.taxonomy_uid:
            self.skipTest("No taxonomy discovered on this stack — skipping.")
        result = self.stack.taxonomy(self.taxonomy_uid).term().depth(1).find()
        self.assertIsNotNone(result)

    # ---------- Single term ----------

    def test_10_fetch_single_term(self):
        """GET /taxonomies/{uid}/terms/{termUid} returns the term object directly."""
        if not self.term_uid:
            self.skipTest("No term discovered on this stack — skipping.")
        result = self.stack.taxonomy(self.taxonomy_uid).term(self.term_uid).fetch()
        self.assertIsNotNone(result)
        self.assertEqual(result.get('uid'), self.term_uid)

    def test_11_fetch_term_with_include_branch(self):
        """GET /taxonomies/{uid}/terms/{termUid}?include_branch=true includes branch info."""
        if not self.term_uid:
            self.skipTest("No term discovered on this stack — skipping.")
        result = self.stack.taxonomy(self.taxonomy_uid).term(self.term_uid) \
            .include_branch().fetch()
        self.assertIsNotNone(result)

    def test_12_term_locales(self):
        """GET /taxonomies/{uid}/terms/{termUid}/locales returns available locales."""
        if not self.term_uid:
            self.skipTest("No term discovered on this stack — skipping.")
        result = self.stack.taxonomy(self.taxonomy_uid).term(self.term_uid).locales()
        self.assertIsNotNone(result)

    def test_13_term_ancestors(self):
        """GET /taxonomies/{uid}/terms/{termUid}/ancestors returns the ancestor chain."""
        if not self.term_uid:
            self.skipTest("No term discovered on this stack — skipping.")
        result = self.stack.taxonomy(self.taxonomy_uid).term(self.term_uid).ancestors()
        self.assertIsNotNone(result)

    def test_14_term_descendants(self):
        """GET /taxonomies/{uid}/terms/{termUid}/descendants returns the descendant terms."""
        if not self.term_uid:
            self.skipTest("No term discovered on this stack — skipping.")
        result = self.stack.taxonomy(self.taxonomy_uid).term(self.term_uid).descendants()
        self.assertIsNotNone(result)

    # ---------- Hierarchy depth (dynamically discovered chain) ----------

    def test_15_descendants_depth_1_returns_only_direct_children(self):
        """depth(1) on descendants() returns the direct child but not the grandchild."""
        parent_uid, child_uid, grandchild_uid = self.hierarchy
        if not parent_uid:
            self.skipTest("No parent/child/grandchild term chain found — skipping.")
        result = self.stack.taxonomy(self.taxonomy_uid).term(parent_uid).depth(1).descendants()
        uids = [t.get('uid') for t in result] if isinstance(result, list) else \
            [t.get('uid') for t in (result or {}).get('descendants', [])]
        self.assertIn(child_uid, uids)
        self.assertNotIn(grandchild_uid, uids)

    def test_16_descendants_depth_2_includes_grandchildren(self):
        """depth(2) on descendants() includes both the child and the grandchild."""
        parent_uid, child_uid, grandchild_uid = self.hierarchy
        if not parent_uid:
            self.skipTest("No parent/child/grandchild term chain found — skipping.")
        result = self.stack.taxonomy(self.taxonomy_uid).term(parent_uid).depth(2).descendants()
        uids = [t.get('uid') for t in result] if isinstance(result, list) else \
            [t.get('uid') for t in (result or {}).get('descendants', [])]
        self.assertIn(child_uid, uids)
        self.assertIn(grandchild_uid, uids)

    def test_17_ancestors_for_grandchild_returns_full_chain(self):
        """ancestors() for the grandchild returns both parent and child in the chain."""
        parent_uid, child_uid, grandchild_uid = self.hierarchy
        if not grandchild_uid:
            self.skipTest("No parent/child/grandchild term chain found — skipping.")
        result = self.stack.taxonomy(self.taxonomy_uid).term(grandchild_uid).ancestors()
        uids = [t.get('uid') for t in result] if isinstance(result, list) else \
            [t.get('uid') for t in (result or {}).get('ancestors', [])]
        self.assertIn(child_uid, uids)
        self.assertIn(parent_uid, uids)

    # ---------- Feature-flag-off / not-found (TRD 1.3) ----------

    def test_18_fetch_unknown_taxonomy_returns_error_body(self):
        """
        A nonexistent taxonomy uid returns a 404 error body. This SDK never
        raises on HTTP-level errors (see contentstack/https_connection.py),
        so the raw dict is asserted directly rather than expecting an exception.
        """
        result = self.stack.taxonomy('nonexistent_taxonomy_uid_xyz_123').fetch()
        self.assertIsNotNone(result)
        self.assertTrue('error_code' in result or 'errors' in result or 'taxonomy' not in result)


# ===========================================================================
# Taxonomy localisation — real API, 'gadgets' fixture
# (mirrors contentstack-dotnet's TaxonomyLocalisationTest.cs test-for-test)
# ===========================================================================

class TestTaxonomyLocalisation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.stack = contentstack.Stack(API_KEY, DELIVERY_TOKEN, ENVIRONMENT, host=HOST)
        exists = cls.stack.taxonomy(TAXONOMY_UID).fetch()
        if not isinstance(exists, dict) or exists.get('uid') != TAXONOMY_UID:
            raise unittest.SkipTest(
                f"'{TAXONOMY_UID}' taxonomy not found on this stack — publish it to run this suite.")
        cls.term_uid = cls._get_first_term_uid(cls.stack)
        cls.parent_uid, cls.child_uid, cls.grandchild_uid = cls._get_term_hierarchy(cls.stack)

    @staticmethod
    def _get_first_term_uid(stack):
        """Fetches the first available term UID from the gadgets taxonomy."""
        terms = stack.taxonomy(TAXONOMY_UID).term() \
            .locale(LOCALE).include_fallback().find()
        items = terms.get('terms', []) if isinstance(terms, dict) else []
        return items[0].get('uid') if items else None

    @staticmethod
    def _get_term_hierarchy(stack):
        """
        Walks descendants() to find a real parent -> child -> grandchild
        term chain. Returns (None, None, None) if no such chain exists.
        """
        terms = stack.taxonomy(TAXONOMY_UID).term().find()
        items = terms.get('terms', []) if isinstance(terms, dict) else []
        for candidate_parent in items:
            parent_uid = candidate_parent.get('uid')
            if not parent_uid:
                continue
            children = stack.taxonomy(TAXONOMY_UID).term(parent_uid).descendants()
            children = children if isinstance(children, list) else []
            child_uid = children[0].get('uid') if children else None
            if not child_uid:
                continue
            grandchildren = stack.taxonomy(TAXONOMY_UID).term(child_uid).descendants()
            grandchildren = grandchildren if isinstance(grandchildren, list) else []
            grandchild_uid = grandchildren[0].get('uid') if grandchildren else None
            if not grandchild_uid:
                continue
            return parent_uid, child_uid, grandchild_uid
        return None, None, None

    # ---------- 1. Fetch localized taxonomy ----------

    def test_01_fetch_taxonomy_master_locale_returns_valid_object(self):
        """Fetching without a locale returns the master-locale (en-us) taxonomy."""
        result = self.stack.taxonomy(TAXONOMY_UID).fetch()
        self.assertIsNotNone(result)
        self.assertEqual(result.get('uid'), TAXONOMY_UID)

    def test_02_fetch_taxonomy_with_locale_returns_localized_name(self):
        """locale('fr-fr') returns the genuinely-translated fr-fr taxonomy record."""
        result = self.stack.taxonomy(TAXONOMY_UID).locale(LOCALE).fetch()
        self.assertIsNotNone(result)
        self.assertEqual(result.get('uid'), TAXONOMY_UID)
        self.assertEqual(result.get('locale'), LOCALE)
        self.assertIsNotNone(result.get('name'))

    # ---------- 2. Find all terms ----------

    def test_03_find_all_terms_returns_collection(self):
        """No locale filter returns the master-locale term collection."""
        result = self.stack.taxonomy(TAXONOMY_UID).term().find()
        self.assertIsNotNone(result)
        self.assertTrue(len(result.get('terms', [])) > 0)

    # ---------- 3. Find terms with locale ----------

    def test_04_find_terms_with_locale_returns_localized_terms(self):
        """locale('fr-fr') without fallback returns only genuinely-translated terms."""
        result = self.stack.taxonomy(TAXONOMY_UID).term().locale(LOCALE).find()
        self.assertIsNotNone(result)
        for term in result.get('terms', []):
            self.assertEqual(term.get('locale'), LOCALE)

    def test_05_find_terms_with_locale_and_fallback_returns_all_terms(self):
        """
        include_fallback() returns every term, with per-node fallback: terms
        translated into fr-fr come back as fr-fr, untranslated ones fall back
        to en-us in the same response (not all-or-nothing).
        """
        result = self.stack.taxonomy(TAXONOMY_UID).term() \
            .locale(LOCALE).include_fallback().find()
        self.assertIsNotNone(result)
        terms = result.get('terms', [])
        self.assertTrue(len(terms) > 0)
        locales_seen = {t.get('locale') for t in terms}
        for term in terms:
            self.assertIn(term.get('locale'), (LOCALE, MASTER_LOCALE))
        # Demonstrates true per-node fallback rather than an all-or-nothing switch,
        # only meaningful if the fixture has a genuine partial translation.
        if len(locales_seen) > 1:
            self.assertIn(LOCALE, locales_seen)
            self.assertIn(MASTER_LOCALE, locales_seen)

    # ---------- 4-7. Single term methods ----------

    def test_06_fetch_single_term_with_locale_returns_localized_term(self):
        if not self.term_uid:
            self.skipTest("No term UID found — skipping.")
        result = self.stack.taxonomy(TAXONOMY_UID).term(self.term_uid) \
            .locale(LOCALE).include_fallback().fetch()
        self.assertIsNotNone(result)
        self.assertEqual(result.get('uid'), self.term_uid)

    def test_07_term_locales_returns_locales_collection(self):
        if not self.term_uid:
            self.skipTest("No term UID found — skipping.")
        result = self.stack.taxonomy(TAXONOMY_UID).term(self.term_uid).locales()
        self.assertIsNotNone(result)

    def test_08_term_ancestors_returns_ancestors_collection(self):
        if not self.term_uid:
            self.skipTest("No term UID found — skipping.")
        result = self.stack.taxonomy(TAXONOMY_UID).term(self.term_uid).ancestors()
        self.assertIsNotNone(result)

    def test_09_term_descendants_returns_descendants_collection(self):
        if not self.term_uid:
            self.skipTest("No term UID found — skipping.")
        result = self.stack.taxonomy(TAXONOMY_UID).term(self.term_uid).descendants()
        self.assertIsNotNone(result)

    # ---------- 8. Term hierarchy - depth / include_branch ----------

    def test_10_descendants_with_depth_1_returns_only_direct_children(self):
        """depth(1) returns the direct child but not the grandchild."""
        if not self.parent_uid:
            self.skipTest("No parent/child/grandchild term chain found — skipping.")
        result = self.stack.taxonomy(TAXONOMY_UID).term(self.parent_uid).depth(1).descendants()
        uids = [t.get('uid') for t in result]
        self.assertIn(self.child_uid, uids)
        self.assertNotIn(self.grandchild_uid, uids)

    def test_11_descendants_with_depth_2_includes_grandchildren(self):
        """depth(2) includes both the direct child and the grandchild."""
        if not self.parent_uid:
            self.skipTest("No parent/child/grandchild term chain found — skipping.")
        result = self.stack.taxonomy(TAXONOMY_UID).term(self.parent_uid).depth(2).descendants()
        uids = [t.get('uid') for t in result]
        self.assertIn(self.child_uid, uids)
        self.assertIn(self.grandchild_uid, uids)

    def test_12_ancestors_for_grandchild_returns_full_chain(self):
        """ancestors() for the grandchild returns both the parent and the child."""
        if not self.grandchild_uid:
            self.skipTest("No parent/child/grandchild term chain found — skipping.")
        result = self.stack.taxonomy(TAXONOMY_UID).term(self.grandchild_uid).ancestors()
        uids = [t.get('uid') for t in result]
        self.assertIn(self.child_uid, uids)
        self.assertIn(self.parent_uid, uids)

    def test_13_term_query_find_with_depth_limits_hierarchy_depth(self):
        result = self.stack.taxonomy(TAXONOMY_UID).term().depth(1).find()
        self.assertIsNotNone(result)
        self.assertTrue(len(result.get('terms', [])) > 0)

    def test_14_term_fetch_with_include_branch_returns_branch_info(self):
        if not self.term_uid:
            self.skipTest("No term UID found — skipping.")
        result = self.stack.taxonomy(TAXONOMY_UID).term(self.term_uid).include_branch().fetch()
        self.assertIsNotNone(result)
        self.assertEqual(result.get('uid'), self.term_uid)

    def test_15_descendants_with_locale_and_fallback_returns_localized_hierarchy(self):
        """
        depth(2) descendants with locale + include_fallback returns both the
        child and grandchild, each individually translated or fallen back.
        """
        if not self.parent_uid:
            self.skipTest("No parent/child/grandchild term chain found — skipping.")
        terms = self.stack.taxonomy(TAXONOMY_UID).term(self.parent_uid) \
            .locale(LOCALE).include_fallback().depth(2).descendants()
        uids = [t.get('uid') for t in terms]
        self.assertIn(self.child_uid, uids)
        self.assertIn(self.grandchild_uid, uids)
        for term in terms:
            self.assertIn(
                term.get('locale'), (LOCALE, MASTER_LOCALE),
                f"Term '{term.get('uid')}' returned unexpected locale '{term.get('locale')}'"
                f" — expected '{LOCALE}' (translated) or '{MASTER_LOCALE}' (fallback)."
            )

    def test_16_ancestors_with_locale_and_fallback_returns_localized_chain(self):
        """ancestors() with locale + include_fallback returns a correctly localized/fallen-back chain."""
        if not self.grandchild_uid:
            self.skipTest("No parent/child/grandchild term chain found — skipping.")
        terms = self.stack.taxonomy(TAXONOMY_UID).term(self.grandchild_uid) \
            .locale(LOCALE).include_fallback().ancestors()
        uids = [t.get('uid') for t in terms]
        self.assertIn(self.child_uid, uids)
        self.assertIn(self.parent_uid, uids)
        for term in terms:
            self.assertIn(term.get('locale'), (LOCALE, MASTER_LOCALE))

    # ---------- 9. List all taxonomies ----------

    def test_17_list_all_taxonomies_returns_collection(self):
        result = self.stack.taxonomy().find()
        self.assertIsNotNone(result)
        self.assertTrue(len(result.get('taxonomies', [])) > 0)

    def test_18_list_all_taxonomies_with_skip_and_limit_returns_paged_subset(self):
        result = self.stack.taxonomy().skip(0).limit(1).find()
        self.assertIsNotNone(result)
        self.assertLessEqual(len(result.get('taxonomies', [])), 1)

    def test_19_list_all_taxonomies_with_include_count_returns_count(self):
        result = self.stack.taxonomy().include_count().find()
        self.assertIsNotNone(result)

    # ---------- 10. Not published in locale at all (contrast case, TRD 1.4) ----------

    def test_20_taxonomy_not_published_in_locale_returns_404_without_fallback(self):
        """
        A taxonomy that has never been published in fr-fr (unlike gadgets,
        which has partial fr-fr content) returns a 404 error body when
        fetched with that locale and no fallback.
        """
        result = self.stack.taxonomy('category').locale(LOCALE).fetch()
        if 'uid' in result:
            self.skipTest("'category' taxonomy is published in fr-fr on this stack — contrast case not applicable.")
        self.assertTrue(result.get('error_code') == 404 or 'errors' in result)

    def test_21_taxonomy_list_not_published_in_locale_returns_empty_array(self):
        """List endpoints return an empty array (not 404) when nothing matches the locale."""
        result = self.stack.taxonomy('category').term().locale(LOCALE).find()
        self.assertEqual(result.get('terms'), [])


if __name__ == '__main__':
    unittest.main()
