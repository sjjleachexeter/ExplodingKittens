from django.contrib.auth.decorators import user_passes_test

# decorate functions with this if it should be superuser only
superuser_required = user_passes_test(lambda u: u.is_superuser)

# decorate functions with this that only passport editors can use
passport_edit_required = user_passes_test(
    lambda u: u.is_authenticated and (u.role.type == 'MANAGER' or u.role.type == 'PASSPORT_ADMIN'))

# decorate functions with this that only game managers can use
game_manager_required = user_passes_test(
    lambda u: u.is_authenticated and (u.role.type == 'MANAGER' or u.role.type == 'GAMES_ADMIN'))
