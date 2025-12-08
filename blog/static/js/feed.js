document.addEventListener('DOMContentLoaded', () => {
    loadPosts();

    // Event delegation for interactions
    document.getElementById('feed-container').addEventListener('click', (e) => {
        const target = e.target.closest('.action-btn');
        if (!target) return;

        const postId = target.dataset.id;
        if (target.classList.contains('like-btn')) {
            handleLike(postId, target);
        } else if (target.classList.contains('comment-btn')) {
            toggleComments(postId);
        }
    });
});

async function loadPosts() {
    const container = document.getElementById('feed-container');
    container.innerHTML = '<div class="text-center py-4"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';

    try {
        // Use authenticated fetch if possible to get correct 'is_liked' status
        let response;
        if (TokenManager.isAuthenticated()) {
            response = await TokenManager.authenticatedFetch('/api/blogs/');
        } else {
            response = await fetch('/api/blogs/');
        }

        if (!response.ok) throw new Error('Failed to load posts');

        const posts = await response.json();
        container.innerHTML = '';

        if (posts.length === 0) {
            container.innerHTML = '<div class="text-center py-5 text-muted">No posts yet. Be the first to share something!</div>';
            return;
        }

        posts.forEach(post => {
            container.appendChild(createPostElement(post));
        });

    } catch (error) {
        console.error('Error loading posts:', error);
        container.innerHTML = '<div class="alert alert-danger text-center">Failed to load feed. Please try again later.</div>';
    }
}

function createPostElement(post) {
    const div = document.createElement('div');
    div.className = 'post-card';

    // Format date
    const date = new Date(post.created_at).toLocaleDateString('en-US', {
        month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
    });

    // Author info
    const authorName = post.author.name || post.author.username;
    const authorAvatar = post.author.avatar || '/media/avatars/default/default.jpg';

    // Like button state
    const likeActive = post.is_liked ? 'liked' : '';
    const likeIcon = post.is_liked ? '❤️' : '🤍';

    // Check if current user is the author (compare usernames)
    const currentUserId = TokenManager.getUserId();
    const isAuthor = currentUserId && post.author.username === TokenManager.getUsername();

    // Edit/Delete buttons for author
    const authorActions = isAuthor ? `
        <div class="ms-auto">
            <button class="btn btn-sm btn-outline-secondary me-1" onclick="showEditPostModal(${post.id})" title="Edit post">
                <i class="bi bi-pencil"></i>
            </button>
            <button class="btn btn-sm btn-outline-danger" onclick="showDeleteModal(${post.id})" title="Delete post">
                <i class="bi bi-trash"></i>
            </button>
        </div>
    ` : '';

    div.innerHTML = `
        <div class="post-header">
            <a href="/accounts/profile/${post.author.username}/" style="text-decoration: none;">
                <img src="${authorAvatar}" alt="${authorName}" class="post-avatar">
            </a>
            <div class="post-info">
                <a href="/accounts/profile/${post.author.username}/" style="text-decoration: none; color: inherit;">
                    <h5>${authorName}</h5>
                </a>
                <p class="post-time">${date}</p>
            </div>
            ${authorActions}
        </div>
        <div class="post-content">
            <a href="/baseapp/blog/${post.slug}/" style="text-decoration: none; color: inherit;">
                <h3 class="post-title">${escapeHtml(post.title)}</h3>
            </a>
            <p class="post-text">
                ${post.description.length > 200
                    ? escapeHtml(post.description.substring(0, 200)) + '... <a href="/baseapp/blog/' + post.slug + '/" class="read-more-link" style="color:#007bff;text-decoration:underline;">Read more</a>'
                    : escapeHtml(post.description)}
            </p>
            ${post.image ? `<a href="/baseapp/blog/${post.slug}/"><img src="${post.image}" alt="Post image" class="post-image rounded"></a>` : ''}
        </div>
        <div class="post-stats">
            <span class="likes-count">${post.likes_count} Likes</span>
            <span class="comments-count">Comments</span> 
        </div>
        <div class="post-actions">
            <button class="action-btn like-btn ${likeActive}" data-id="${post.id}">
                <span class="like-icon">${likeActive ? '❤️' : '👍'}</span> Like
            </button>
            <button class="action-btn comment-btn" data-id="${post.id}">
                💬 Comment
            </button>
        </div>
        <div class="comments-section" id="comments-${post.id}" style="display: none; padding: 10px 16px; background: #f7f8fa;">
            <!-- Comments will be loaded here -->
            <div class="comments-list mb-3"></div>
            <div class="comment-input-wrapper d-flex">
                <input type="text" class="form-control rounded-pill comment-input" placeholder="Write a comment..." data-id="${post.id}">
                <button class="btn btn-primary btn-sm ms-2 rounded-pill send-comment-btn" data-id="${post.id}">Post</button>
            </div>
        </div>
    `;

    // Add event listener for comment input
    const sendBtn = div.querySelector('.send-comment-btn');
    const input = div.querySelector('.comment-input');

    sendBtn.addEventListener('click', () => submitComment(post.id, input));
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') submitComment(post.id, input);
    });

    return div;
}

async function handleLike(postId, btn) {
    if (!TokenManager.isAuthenticated()) {
        window.location.href = '/accounts/login/';
        return;
    }

    try {
        const response = await TokenManager.authenticatedFetch('/api/likes/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ blog: postId })
        });

        if (response.ok) {
            const data = await response.json();
            const postCard = btn.closest('.post-card');
            const likesCountEl = postCard.querySelector('.likes-count');
            const likeIcon = btn.querySelector('.like-icon');

            // Toggle like state
            if (data.status === 'unliked') {
                // User unliked the post
                btn.classList.remove('liked');
                likeIcon.textContent = '👍';
                const currentCount = parseInt(likesCountEl.textContent);
                likesCountEl.textContent = `${currentCount - 1} Likes`;
            } else {
                // User liked the post
                btn.classList.add('liked');
                likeIcon.textContent = '❤️';
                const currentCount = parseInt(likesCountEl.textContent);
                likesCountEl.textContent = `${currentCount + 1} Likes`;
            }
        }
    } catch (error) {
        console.error('Error liking post:', error);
    }
}

function toggleComments(postId) {
    const section = document.getElementById(`comments-${postId}`);
    if (section.style.display === 'none') {
        section.style.display = 'block';
        loadComments(postId);
    } else {
        section.style.display = 'none';
    }
}

async function loadComments(postId) {
    const section = document.getElementById(`comments-${postId}`);
    const list = section.querySelector('.comments-list');
    list.innerHTML = '<small class="text-muted">Loading comments...</small>';

    try {
        // Fetch comments for this blog
        // Note: The API /api/comments/ returns ALL comments. We need to filter by blog.
        // Ideally the API should support filtering ?blog=ID
        // Let's assume it does or we filter client side (not efficient but works for small scale)
        const response = await fetch(`/api/comments/?blog=${postId}`); // Assuming filter exists or we get all
        // If filter doesn't work, we might get all. Let's check api/views.py later.

        if (response.ok) {
            const allComments = await response.json();
            // Filter client side if needed (safe fallback)
            const comments = allComments.filter(c => c.blog == postId);

            list.innerHTML = '';
            if (comments.length === 0) {
                list.innerHTML = '<small class="text-muted">No comments yet.</small>';
                return;
            }

            comments.forEach(comment => {
                const commentDiv = document.createElement('div');
                commentDiv.className = 'mb-2 p-2 bg-white rounded';
                commentDiv.innerHTML = `
                    <strong>${escapeHtml(comment.user)}</strong> 
                    <span class="text-muted small ms-2">${new Date(comment.created_at).toLocaleDateString()}</span>
                    <p class="mb-0 small">${escapeHtml(comment.message)}</p>
                `;
                list.appendChild(commentDiv);
            });
        }
    } catch (error) {
        list.innerHTML = '<small class="text-danger">Error loading comments.</small>';
    }
}

async function submitComment(postId, input) {
    if (!TokenManager.isAuthenticated()) {
        window.location.href = '/accounts/login/';
        return;
    }

    const message = input.value.trim();
    if (!message) return;

    try {
        const response = await TokenManager.authenticatedFetch('/api/comments/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                blog: postId,
                message: message
            })
        });

        if (response.ok) {
            input.value = '';
            loadComments(postId); // Reload comments
        }
    } catch (error) {
        console.error('Error posting comment:', error);
        alert('Failed to post comment');
    }
}

function escapeHtml(text) {
    if (!text) return '';
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Search posts function
async function searchPosts(query) {
    const container = document.getElementById('feed-container');
    container.innerHTML = '<div class="text-center py-4"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Searching...</span></div></div>';

    try {
        // Use the API's search parameter
        let response;
        const searchUrl = `/api/blogs/?search=${encodeURIComponent(query)}`;

        if (TokenManager.isAuthenticated()) {
            response = await TokenManager.authenticatedFetch(searchUrl);
        } else {
            response = await fetch(searchUrl);
        }

        if (!response.ok) throw new Error('Failed to search posts');

        const posts = await response.json();
        container.innerHTML = '';

        if (posts.length === 0) {
            container.innerHTML = `<div class="text-center py-5 text-muted">No posts found for "${escapeHtml(query)}". <a href="#" onclick="loadPosts(); return false;">Show all posts</a></div>`;
            return;
        }

        // Add search results header
        const header = document.createElement('div');
        header.className = 'alert alert-info mb-3';
        header.innerHTML = `Found ${posts.length} post(s) for "${escapeHtml(query)}". <a href="#" onclick="loadPosts(); document.getElementById('searchInput').value=''; return false;" class="alert-link">Clear search</a>`;
        container.appendChild(header);

        posts.forEach(post => {
            container.appendChild(createPostElement(post));
        });

    } catch (error) {
        console.error('Error searching posts:', error);
        container.innerHTML = '<div class="alert alert-danger text-center">Failed to search. Please try again later.</div>';
    }
}

// Make searchPosts available globally
window.searchPosts = searchPosts;

// ========== BLOG CRUD FUNCTIONS ==========

let categories = [];
let postModalInstance = null;
let deleteModalInstance = null;
let currentDeletePostId = null;

// Load categories on page load
document.addEventListener('DOMContentLoaded', async () => {
    // Initialize Bootstrap modals
    const postModalEl = document.getElementById('postModal');
    const deleteModalEl = document.getElementById('deleteModal');

    if (postModalEl) {
        postModalInstance = new bootstrap.Modal(postModalEl);
    }
    if (deleteModalEl) {
        deleteModalInstance = new bootstrap.Modal(deleteModalEl);
    }

    // Load categories
    await loadCategories();

    // Set up submit post handler
    const submitBtn = document.getElementById('submitPost');
    if (submitBtn) {
        submitBtn.addEventListener('click', handleSubmitPost);
    }

    // Set up delete confirmation handler
    const confirmDeleteBtn = document.getElementById('confirmDelete');
    if (confirmDeleteBtn) {
        confirmDeleteBtn.addEventListener('click', handleConfirmDelete);
    }
});

// Load categories from API
async function loadCategories() {
    try {
        const response = await fetch('/api/categories/');
        if (response.ok) {
            categories = await response.json();
            const categorySelect = document.getElementById('postCategory');
            if (categorySelect) {
                categorySelect.innerHTML = '<option value="">Select a category...</option>';
                categories.forEach(cat => {
                    const option = document.createElement('option');
                    option.value = cat.name;
                    option.textContent = cat.name;
                    categorySelect.appendChild(option);
                });
            }
        }
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

// Show create post modal
function showCreatePostModal() {
    if (!TokenManager.isAuthenticated()) {
        window.location.href = '/accounts/login/';
        return;
    }

    // Reset form
    document.getElementById('postForm').reset();
    document.getElementById('postId').value = '';
    document.getElementById('postModalLabel').textContent = 'Create Post';
    document.getElementById('currentImage').innerHTML = '';

    if (postModalInstance) {
        postModalInstance.show();
    }
}

// Show edit post modal
async function showEditPostModal(postId) {
    if (!TokenManager.isAuthenticated()) {
        window.location.href = '/accounts/login/';
        return;
    }

    try {
        // Fetch post details
        const response = await TokenManager.authenticatedFetch(`/api/blogs/${postId}/`);
        if (response.ok) {
            const post = await response.json();

            // Populate form
            document.getElementById('postId').value = post.id;
            document.getElementById('postTitle').value = post.title;
            document.getElementById('postDescription').value = post.description;
            document.getElementById('postCategory').value = post.category;

            // Show current image if exists
            const currentImageDiv = document.getElementById('currentImage');
            if (post.image) {
                currentImageDiv.innerHTML = `
                    <div class="alert alert-info">
                        Current image: <img src="${post.image}" alt="Current" style="max-width: 100px; max-height: 100px;">
                    </div>
                `;
            } else {
                currentImageDiv.innerHTML = '';
            }

            document.getElementById('postModalLabel').textContent = 'Edit Post';

            if (postModalInstance) {
                postModalInstance.show();
            }
        }
    } catch (error) {
        console.error('Error loading post for edit:', error);
        alert('Failed to load post details');
    }
}

// Handle submit post (create or update)
async function handleSubmitPost() {
    const postId = document.getElementById('postId').value;
    const title = document.getElementById('postTitle').value.trim();
    const description = document.getElementById('postDescription').value.trim();
    const category = document.getElementById('postCategory').value;
    const imageFile = document.getElementById('postImage').files[0];

    if (!title || !description || !category) {
        alert('Please fill in all required fields');
        return;
    }

    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
    formData.append('category', category);

    if (imageFile) {
        formData.append('image', imageFile);
    }

    try {
        let response;
        if (postId) {
            // Update existing post
            response = await TokenManager.authenticatedFetch(`/api/blogs/${postId}/`, {
                method: 'PATCH',
                body: formData
            });
        } else {
            // Create new post
            response = await TokenManager.authenticatedFetch('/api/blogs/', {
                method: 'POST',
                body: formData
            });
        }

        if (response.ok) {
            if (postModalInstance) {
                postModalInstance.hide();
            }
            loadPosts(); // Reload feed
            alert(postId ? 'Post updated successfully!' : 'Post created successfully!');
        } else {
            const error = await response.json();
            alert('Failed to save post: ' + JSON.stringify(error));
        }
    } catch (error) {
        console.error('Error saving post:', error);
        alert('Failed to save post');
    }
}

// Show delete confirmation
function showDeleteModal(postId) {
    currentDeletePostId = postId;
    if (deleteModalInstance) {
        deleteModalInstance.show();
    }
}

// Handle confirm delete
async function handleConfirmDelete() {
    if (!currentDeletePostId) return;

    try {
        const response = await TokenManager.authenticatedFetch(`/api/blogs/${currentDeletePostId}/`, {
            method: 'DELETE'
        });

        if (response.ok || response.status === 204) {
            if (deleteModalInstance) {
                deleteModalInstance.hide();
            }
            loadPosts(); // Reload feed
            alert('Post deleted successfully!');
        } else {
            alert('Failed to delete post');
        }
    } catch (error) {
        console.error('Error deleting post:', error);
        alert('Failed to delete post');
    }

    currentDeletePostId = null;
}

// Make functions available globally
window.showCreatePostModal = showCreatePostModal;
window.showEditPostModal = showEditPostModal;
window.showDeleteModal = showDeleteModal;
