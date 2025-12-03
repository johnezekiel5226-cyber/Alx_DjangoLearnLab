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

Comment System — README (Blog app)
=================================

Overview
--------
This comment system allows authenticated users to leave comments on posts, and allows comment authors to edit/delete their own comments.

Models
------
- Comment:
  - post: FK to Post
  - author: FK to User
  - content: TextField
  - created_at: DateTimeField(auto_now_add=True)
  - updated_at: DateTimeField(auto_now=True)

Forms
-----
- CommentForm: ModelForm for Comment. Validates non-empty content and minimum length.

Views / URLs
------------
- Add comment (POST): `/posts/<post_id>/comments/new/` -> `add_comment`
  - Requires login. Accepts POST with `content`.
- Edit comment: `/posts/<post_id>/comments/<comment_id>/edit/` -> `CommentEditView`
  - Only comment author may edit.
- Delete comment: `/posts/<post_id>/comments/<comment_id>/delete/` -> `CommentDeleteView`
  - Only comment author may delete.

Templates
---------
- `_comments.html`: lists comments for a post (include this in `post_detail.html`)
- `comment_form.html`: used for adding/editing comments
- `comment_confirm_delete.html`: used to confirm deletion

How to use (example)
--------------------
On a post detail page, authenticated users can submit the comment form (posts to `/posts/<id>/comments/new/`). After adding a comment, the user is redirected back to the post detail page where their new comment appears.

Permissions
-----------
- Only authenticated users can post comments.
- Only the comment's author can edit or delete it.

Admin / Maintenance
-------------------
- To add fields to Comment, update model and run `makemigrations` and `migrate`.
- To change ordering (newest first), set `class Meta: ordering = ['-created_at']` in the model.

Notes
-----
- Adjust template markup and CSS classes to match your blog theme.
- Consider adding comment moderation or flagging if needed (future enhancement).
