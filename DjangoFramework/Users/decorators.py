from django.contrib.auth.decorators import user_passes_test

# decrate functions with this if it should be superuser only
superuser_required = user_passes_test(lambda u: u.is_superuser)

# decrate functions with this that only passport editors can use
passport_edit_required = user_passes_test(
    lambda u: u.is_authenticated and (u.role.type == 'MANAGER' or u.role.type == 'PASSPORT_ADMIN'))
