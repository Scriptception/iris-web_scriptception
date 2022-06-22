from flask import session
from sqlalchemy import and_

from app.models.authorization import CaseAccessLevel
from app.models.authorization import Group
from app.models.authorization import GroupCaseAccess
from app.models.authorization import OrganisationCaseAccess
from app.models.authorization import Permissions
from app.models.authorization import UserCaseAccess
from app.models.authorization import UserGroup
from app.models.authorization import UserOrganisation


def ac_get_mask_full_permissions():
    """
    Return access mask for full permissions
    """
    am = 0
    for perm in Permissions._member_names_:
        am |= Permissions[perm].value

    return am


def ac_get_mask_analyst():
    """
    Return a standard access mask for analysts
    """
    am = 0
    am |= Permissions.read_case_data.value
    am |= Permissions.write_case_data.value
    am |= Permissions.delete_case_data.value

    return am


def ac_permission_to_list(permission):
    """
    Return a list of permissions from a permission mask
    """
    perms = []
    for perm in Permissions._member_names_:
        if permission & Permissions[perm].value:
            perms.append({
                'name': perm,
                'value': Permissions[perm].value
            })

    return perms


def ac_mask_from_val_list(permissions):
    """
    Return a permission mask from a list of permissions
    """
    am = 0
    for perm in permissions:
        am |= int(perm)

    return am


def ac_get_all_permissions():
    """
    Return a list of all permissions
    """
    perms = []
    for perm in Permissions._member_names_:
        perms.append({
            'name': perm,
            'value': Permissions[perm].value
        })

    return perms


def ac_get_detailed_effective_permissions_from_groups(groups):
    """
    Return a list of permissions from a list of groups
    """
    perms = {}
    for group in groups:
        perm = group.group_permissions

        for std_perm in Permissions._member_names_:

            if perm & Permissions[std_perm].value:
                if Permissions[std_perm].value not in perms:
                    perms[Permissions[std_perm].value] = {
                        'name': std_perm,
                        'value': Permissions[std_perm].value,
                        'inherited_from': [group.group_name]
                    }

                else:
                    if group.group_name not in perms[Permissions[std_perm].value]['inherited_from']:
                        perms[Permissions[std_perm].value]['inherited_from'].append(group.group_name)

    return perms


def ac_get_effective_permissions_from_groups(groups):
    """
    Return a permission mask from a list of groups
    """
    final_perm = 0
    for group in groups:
        final_perm &= group.group_permissions

    return final_perm


def ac_get_effective_permissions_of_user(user):
    """
    Return a permission mask from a user
    """
    groups_perms = UserGroup.query.with_entities(
        Group.group_permissions,
    ).filter(
        UserGroup.user_id == user.id
    ).join(
        UserGroup.group
    ).all()

    final_perm = 0
    for group in groups_perms:
        final_perm |= group.group_permissions

    return final_perm


def ac_user_case_access(user_id, cid):
    """
    Returns the user access level to a case
    """
    oca = OrganisationCaseAccess.query.filter(
        and_(OrganisationCaseAccess.case_id == cid,
             UserOrganisation.user_id == user_id,
             OrganisationCaseAccess.org_id == UserOrganisation.org_id)
    ).first()

    if oca:
        return oca.access_level

    gca = GroupCaseAccess.query.filter(
        and_(GroupCaseAccess.case_id == cid,
             UserGroup.user_id == user_id,
             UserGroup.group_id == GroupCaseAccess.group_id)
    ).first()

    if gca:
        return gca.access_level

    uca = UserCaseAccess.query.filter(
        and_(UserCaseAccess.case_id == cid,
             UserCaseAccess.user_id == user_id)
    ).first()

    if uca:
        return uca.access_level

    return 0


def ac_get_mask_case_access_level_full():
    am = 0
    for ac in CaseAccessLevel._member_names_:
        am |= CaseAccessLevel[ac].value

    return am


def ac_user_has_permission(user, permission):
    """
    Return True if user has permission
    """
    return ac_get_effective_permissions_of_user(user) & permission.value == permission


def ac_current_user_has_permission(permission):
    """
    Return True if current user has permission
    """
    return session['permissions'] & permission.value == permission
