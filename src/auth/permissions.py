def has_permission(
        user,
        resource: str,
        action: str
) -> bool:

    for role in user.roles:

        for permission in role.permissions:

            if (
                permission.resource == resource
                and
                permission.action == action
            ):
                return True

    return False