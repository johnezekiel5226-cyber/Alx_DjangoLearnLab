# Blog Post CRUD (Overview)


This adds a Post model and full Create-Read-Update-Delete functionality using Django class-based views.


Usage:
- Browse all posts: /posts/
- View a post: /posts/<pk>/
- Create (auth users): /posts/new/
- Edit (author only): /posts/<pk>/edit/
- Delete (author only): /posts/<pk>/delete/


Permissions:
- Creating posts requires login. Ensure `LOGIN_URL` is configured in settings.
- Editing and deleting are restricted to the original author via `UserPassesTestMixin`.


Notes:
- Forms automatically set the author in the view's `form_valid` method.
- Add `posts` templates to your template directory and include base navigation links to the posts list and login/logout.
