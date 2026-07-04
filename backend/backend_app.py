from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."}
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    # catch what fields missing
    missing_fields = []
    if "title" not in data or data["title"] is None or str(data["title"]).strip() == "":
        missing_fields.append("title")
    if "content" not in data or data["content"] is None or str(data["content"]).strip() == "":
        missing_fields.append("content")

    # 400 for missing fields
    if missing_fields:
        return jsonify({
            "error": "Bad Request",
            "message": f"Missing required field(s): {', '.join(missing_fields)}"
        }), 400

    new_post = {
        "id": data.get("id"),
        "title": data["title"].strip(),
        "content": data["content"].strip()
    }
    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route('/api/posts/<id>', methods=['DELETE'])
def delete_post(id):
    post_to_delete = next((post for post in POSTS if str(post["id"]) == str(id)), None)

    if not post_to_delete:
        return jsonify({"error": "Post not found"}), 404

    POSTS.remove(post_to_delete)

    return jsonify({
        "deleted_post": post_to_delete,
        "message": f"Post with id {id} has been deleted successfully."
    }), 200


@app.route('/api/posts/<id>', methods=['PUT'])
def update_post(id):
    post = next((p for p in POSTS if str(p.get("id")) == str(id)), None)

    if not post:
        return jsonify({"error": "Post not found"}), 404
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    if "title" in data:
        post["title"] = data["title"]
    if "content" in data:
        post["content"] = data["content"]

    return jsonify(post), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
