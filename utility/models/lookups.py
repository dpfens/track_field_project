from django.db import models


class Search(models.Lookup):
   lookup_name = 'search'

   def as_mysql(self, compiler, connection):
       lhs, lhs_params = self.process_lhs(compiler, connection)
       rhs, rhs_params = self.process_rhs(compiler, connection)
       params = lhs_params + rhs_params
       statement = 'MATCH (%s) AGAINST (%s IN NATURAL LANGUAGE MODE)' % (lhs, rhs)
       return statement, params


class ExpansionSearch(models.Lookup):
   lookup_name = 'expansionsearch'

   def as_mysql(self, compiler, connection):
       lhs, lhs_params = self.process_lhs(compiler, connection)
       rhs, rhs_params = self.process_rhs(compiler, connection)
       params = lhs_params + rhs_params
       statement = 'MATCH (%s) AGAINST (%s WITH QUERY EXPANSION)' % (lhs, rhs)
       return statement, params


class BooleanSearch(models.Lookup):
   lookup_name = 'boolsearch'

   def as_mysql(self, compiler, connection):
       lhs, lhs_params = self.process_lhs(compiler, connection)
       rhs, rhs_params = self.process_rhs(compiler, connection)
       params = lhs_params + rhs_params
       statement = 'MATCH (%s) AGAINST (%s IN BOOLEAN MODE)' % (lhs, rhs)
       return statement, params


class SoundsLike(models.Lookup):
   lookup_name = 'sounds_like'

   def as_mysql(self, compiler, connection):
       lhs, lhs_params = self.process_lhs(compiler, connection)
       rhs, rhs_params = self.process_rhs(compiler, connection)
       params = lhs_params + rhs_params
       statement = '%s SOUNDS LIKE %s' % (lhs, rhs)
       return statement, params


models.CharField.register_lookup(Search)
models.TextField.register_lookup(Search)

models.CharField.register_lookup(ExpansionSearch)
models.TextField.register_lookup(ExpansionSearch)

models.CharField.register_lookup(BooleanSearch)
models.TextField.register_lookup(BooleanSearch)

models.CharField.register_lookup(SoundsLike)
models.TextField.register_lookup(SoundsLike)
