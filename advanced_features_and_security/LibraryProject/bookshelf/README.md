# Django Access Control System using Groups and Permissions

## Overview
This Django app implements a system where access to model instances is controlled via user permissions and groups. Users are assigned to groups, and each group has specific permissions related to actions such as viewing, creating, editing, and deleting objects.

## Model Permissions
- `can_view`: Allows users to view book details.
- `can_create`: Allows users to create new books.
- `can_edit`: Allows users to edit existing books.
- `can_delete`: Allows users to delete books.

## Groups and Permissions
- **Viewers**: Users who have the `can_view` permission.
- **Editors**: Users who have the `can_view`, `can_create`, and `can_edit` permissions.
- **Admins**: Users who have all four permissions: `can_view`, `can_create`, `can_edit`, and `can_delete`.

## Views and Permissions
- The `book_list` view requires the `can_view` permission.
- The `create_book` view requires the `can_create` permission.
- The `edit_book` view requires the `can_edit` permission.
- The `delete_book` view requires the `can_delete` permission.

## Testing
- Create test users and assign them to different groups.
- Log in as users from different groups and verify that the permissions are correctly enforced in the views.

## How to Assign Permissions
- Assign permissions to groups via the Django admin interface under "Groups".
- Assign users to groups under the "Users" section in the admin interface.
