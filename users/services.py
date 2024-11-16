from django.contrib.auth.models import User, Group, Permission

def asign_group_user(user:object, name_group:str)->object:
    group, created = Group.objects.get_or_create(name=name_group)
    user.groups.add(group)
    return group

def asign_group_member(user:object)->object:
    group, created = Group.objects.get_or_create(name="arrendadores")
    user.groups.add(group)
    return group

def asign_group_customer(user:object)->object:
    group, created = Group.objects.get_or_create(name="arrendatario")
    user.groups.add(group)
    return group

def add_group_permission(name_permission:str, name_group:str)->object:
    group, created = Group.objects.get_or_create(name=name_group)
    permission = Permission.objects.get(name=name_permission)
    group.permissions.add(permission)
    return group