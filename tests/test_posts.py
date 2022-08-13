import pytest
from app import schemas

#no tiene mucho sentido este test porque ya estoy dejando hacer get sin autorizacion
def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    def validate(post):
        return schemas.PostVote(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

# def test_unauthorized_user_get_all_posts(client):
#     res = client.get('/posts/')
#     assert res.status_code == 401

#no tiene mucho sentido este test porque ya estoy dejando hacer get sin autorizacion
# def test_unauthorized_user_get_one_post(client, test_posts):
#     res = client.get(f'/posts/{test_posts[0].id}')
#     assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/888")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f'/posts/{test_posts[0].id}')
    post = schemas.PostVote(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content

@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "new content", True)
    # ("dfdsasd", "fhcchtgh", False),
    # ("dfgtesrge", "ngretent", True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post('/posts/', json={"title": title, "content": content, "published": published})
    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']

def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post('/posts/', json={"title": "fdfsfs", "content": "fdsfdsfsd"})
    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == "fdfsfs"
    assert created_post.content == "fdsfdsfsd"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']

def test_unauthorized_user_get_one_post(client):
    res = client.post('/posts/', json={"title": "fdfsfs", "content": "fdsfdsfsd"})
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f'/posts/88888')
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f'/posts/{test_posts[3].id}')
    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {
                "title" : "qqqqqqqqqqqqq",
                "content" : "aaaaaaaaa"
            }
    res = authorized_client.put(f'/posts/{test_posts[0].id}', json=data)
    updated_post = schemas.PostCreate(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_update_other_user_post(authorized_client, test_posts):
    data = {
                "title" : "qqqqqqqqqqqqq",
                "content" : "aaaaaaaaa"
            }
    res = authorized_client.put(f'/posts/{test_posts[3].id}', json=data)
    assert res.status_code == 403

def test_unauthorized_user_update_post(client, test_posts):
    data = {
                "title" : "qqqqqqqqqqqqq",
                "content" : "aaaaaaaaa"
            }
    res = client.put(f'/posts/{test_posts[0].id}', json=data)
    assert res.status_code == 401

def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
                "title" : "qqqqqqqqqqqqq",
                "content" : "aaaaaaaaa"
            }
    res = authorized_client.put(f'/posts/88888', json=data)
    assert res.status_code == 404