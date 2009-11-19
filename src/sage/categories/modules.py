r"""
Modules
"""
#*****************************************************************************
#  Copyright (C) 2005      David Kohel <kohel@maths.usyd.edu>
#                          William Stein <wstein@math.ucsd.edu>
#                2008      Teresa Gomez-Diaz (CNRS) <Teresa.Gomez-Diaz@univ-mlv.fr>
#                2008-2009 Nicolas M. Thiery <nthiery at users.sf.net>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#******************************************************************************

from sage.categories.all import Bimodules, HomCategory
from category_types import Category_module
from sage.misc.cachefunc import cached_method

class Modules(Category_module):
    """
    The category of all modules over a base ring.

    R-left and R-right modules
    modules over a commutative ring
    ##  r*(x*s) = (r*x)*s

    EXAMPLES::

        sage: Modules(RationalField())
        Category of modules over Rational Field

        sage: Modules(Integers(9))
        Category of modules over Ring of integers modulo 9

        sage: Modules(Integers(9)).super_categories()
        [Category of bimodules over Ring of integers modulo 9 on the left and Ring of integers modulo 9 on the right]
        sage: Modules(Integers(9)).all_super_categories()
        [Category of modules over Ring of integers modulo 9,
         Category of bimodules over Ring of integers modulo 9 on the left and Ring of integers modulo 9 on the right,
         Category of left modules over Ring of integers modulo 9,
         Category of right modules over Ring of integers modulo 9,
         Category of commutative additive groups,
         Category of commutative additive monoids,
         Category of commutative additive semigroups,
         Category of sets,
         Category of objects]

        sage: Modules(ZZ).super_categories()
        [Category of bimodules over Integer Ring on the left and Integer Ring on the right]

        sage: Modules == RingModules
        True

        sage: Modules(ZZ[x]).is_abelian()   # see #6081
        True

    TESTS::

        sage: TestSuite(Modules(ZZ)).run()

    TODO:

     - When R is a field, Modules(R) could return VectorSpaces(R).
     - Implement a FreeModules(R) category, when so prompted by a concrete use case
    """

    @cached_method
    def super_categories(self):
        """
        EXAMPLES::

            sage: Modules(QQ).super_categories()
            [Category of bimodules over Rational Field on the left and Rational Field on the right]
        """
        R = self.base_ring()
        return [Bimodules(R,R)]

    class ParentMethods:
        pass

    class ElementMethods:

        def __mul__(left, right):
            """
            TESTS::

                sage: F = CombinatorialFreeModule(QQ, ["a", "b"])
                sage: x = F.term("a")
                sage: x * int(2)
                2*B['a']

            TODO: make a better unit test once Modules().example() is implemented
            """
            from sage.structure.element import get_coercion_model
            import operator
            return get_coercion_model().bin_op(left, right, operator.mul)

        def __rmul__(right, left):
            """
            TESTS::

                sage: F = CombinatorialFreeModule(QQ, ["a", "b"])
                sage: x = F.term("a")
                sage: int(2) * x
                2*B['a']

            TODO: make a better unit test once Modules().example() is implemented
            """
            from sage.structure.element import get_coercion_model
            import operator
            return get_coercion_model().bin_op(left, right, operator.mul)


    class HomCategory(HomCategory):
        """
        The category of homomorphisms sets Hom(X,Y) for X, Y modules
        """

        def extra_super_categories(self):
            """
            EXAMPLES::

                sage: Modules(ZZ).hom_category().extra_super_categories()
                [Category of modules over Integer Ring]
            """
            return [Modules(self.base_category.base_ring())]

        class ParentMethods:
            @cached_method
            def zero(self):
                """
                EXAMPLES::

                    sage: E = CombinatorialFreeModule(ZZ, [1,2,3])
                    sage: F = CombinatorialFreeModule(ZZ, [2,3,4])
                    sage: H = Hom(E, F)
                    sage: f = H.zero()
                    sage: f
                    Generic morphism:
                      From: Free module generated by {1, 2, 3} over Integer Ring
                      To:   Free module generated by {2, 3, 4} over Integer Ring
                    sage: f(E.term(2))
                    0
                    sage: f(E.term(3)) == F.zero()
                    True
                """
                return self(lambda x: self.codomain().zero())

    class EndCategory(HomCategory):
        """
        The category of endomorphisms sets End(X) for X module (this is not used yet)
        """

        def extra_super_categories(self):
            """
            EXAMPLES::

                sage: Hom(ZZ^3, ZZ^3).category().extra_super_categories() # todo: not implemented
                [Category of algebras over Integer Ring]
            """
            from algebras import Algebras
            return [Algebras(self.base_category.base_ring())]
