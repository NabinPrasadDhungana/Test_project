// Admin Dashboard JavaScript

// Toggle user status (activate/deactivate)
async function toggleUserStatus(userId, activate) {
    const action = activate ? 'activate' : 'deactivate';
    const confirmMsg = `Are you sure you want to ${action} this user?`;

    if (!confirm(confirmMsg)) {
        return;
    }

    try {
        const token = TokenManager.getAccessToken();
        const response = await fetch(`/api/users/${userId}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                is_active: activate
            })
        });

        if (response.ok) {
            alert(`User ${action}d successfully!`);
            location.reload();
        } else {
            alert(`Failed to ${action} user. Please try again.`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    }
}

// Delete blog
async function deleteBlog(blogId, blogTitle) {
    const confirmMsg = `Are you sure you want to delete the blog "${blogTitle}"? This action cannot be undone.`;

    if (!confirm(confirmMsg)) {
        return;
    }

    try {
        const token = TokenManager.getAccessToken();
        const response = await fetch(`/api/blogs/${blogId}/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok || response.status === 204) {
            alert('Blog deleted successfully!');
            location.reload();
        } else {
            alert('Failed to delete blog. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    }
}

// Create category
document.addEventListener('DOMContentLoaded', function () {
    const createCategoryForm = document.getElementById('createCategoryForm');
    if (createCategoryForm) {
        createCategoryForm.addEventListener('submit', async function (e) {
            e.preventDefault();

            const name = document.getElementById('categoryName').value;
            const slug = document.getElementById('categorySlug').value;

            try {
                const token = TokenManager.getAccessToken();
                const response = await fetch('/api/categories/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ name, slug })
                });

                if (response.ok) {
                    alert('Category created successfully!');
                    location.reload();
                } else {
                    const data = await response.json();
                    alert('Failed to create category: ' + JSON.stringify(data));
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        });
    }
});

// Edit category
function editCategory(categoryId, categoryName, categorySlug) {
    document.getElementById('editCategoryId').value = categoryId;
    document.getElementById('editCategoryName').value = categoryName;
    document.getElementById('editCategorySlug').value = categorySlug;

    const modal = new bootstrap.Modal(document.getElementById('editCategoryModal'));
    modal.show();
}

// Save category
async function saveCategory() {
    const categoryId = document.getElementById('editCategoryId').value;
    const name = document.getElementById('editCategoryName').value;
    const slug = document.getElementById('editCategorySlug').value;

    try {
        const token = TokenManager.getAccessToken();
        const response = await fetch(`/api/categories/${categoryId}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ name, slug })
        });

        if (response.ok) {
            alert('Category updated successfully!');
            location.reload();
        } else {
            alert('Failed to update category. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    }
}

// Delete category
async function deleteCategory(categoryId, categoryName, blogCount) {
    let confirmMsg = `Are you sure you want to delete the category "${categoryName}"?`;
    if (blogCount > 0) {
        confirmMsg += `\n\nWarning: This category has ${blogCount} blog(s). Deleting it may affect those blogs.`;
    }

    if (!confirm(confirmMsg)) {
        return;
    }

    try {
        const token = TokenManager.getAccessToken();
        const response = await fetch(`/api/categories/${categoryId}/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok || response.status === 204) {
            alert('Category deleted successfully!');
            location.reload();
        } else {
            const data = await response.json();
            alert('Failed to delete category: ' + JSON.stringify(data));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    }
}

// Delete comment
async function deleteComment(commentId) {
    if (!confirm('Are you sure you want to delete this comment?')) {
        return;
    }

    try {
        const token = TokenManager.getAccessToken();
        const response = await fetch(`/api/comments/${commentId}/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok || response.status === 204) {
            // Remove the row from the table
            const row = document.getElementById(`comment-${commentId}`);
            if (row) {
                row.remove();
            }
            alert('Comment deleted successfully!');
        } else {
            alert('Failed to delete comment. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    }
}

// Show full comment
function showFullComment(commentId, commentText) {
    document.getElementById('fullCommentText').textContent = commentText;
    const modal = new bootstrap.Modal(document.getElementById('fullCommentModal'));
    modal.show();
}
