from django.contrib.auth.models import Group, Permission

def create_user_groups(sender, **kwargs):
    groups_permissions = {
        "Admins": ["add_book", "change_book", "delete_book", "view_book"],
        "Editors": ["add_book", "change_book", "view_book"],
        "Viewers": ["view_book"],
    }

    for group_name, perms in groups_permissions.items():
        group, created = Group.objects.get_or_create(name=group_name)
        for perm_codename in perms:
            try:
                permission = Permission.objects.get(codename=perm_codename)
                group.permissions.add(permission)
            except Permission.DoesNotExist:
                print(f"Permission '{perm_codename}' not found. Run migrations first.")
