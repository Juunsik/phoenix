from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "database.db"
)

db = SQLAlchemy(app)


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(10000), nullable=False)
    mbti = db.Column(db.String(100), nullable=False)
    collabo_style = db.Column(db.String(100), nullable=False)
    advantage = db.Column(db.String(100), nullable=False)
    blog_url = db.Column(db.String(10000), nullable=False)

    def __repr__(self):
        return f"{self.username}"


with app.app_context():
    db.create_all()


@app.route("/")
def members():
    member_list = Member.query.all()
    return render_template("phoenix.html", data=member_list)


@app.route("/members/<username>/", methods=["GET"])
def render_member_filter(username):
    get_list = Member.query.filter_by(username=username).first()
    return render_template("phoenix.html", data=get_list)


@app.route("/members/create/", methods=["POST", "GET"])
def member_create():
    username_receive = request.form["username"]
    image_url_receive = request.form["image_url"]
    mbti_receive = request.form["mbti"]
    collabo_style_receive = request.form["collabo_style"]
    advantage_receive = request.form["advantage"]
    blog_url_receive = request.form["blog_url"]

    if request.method == "POST":
        if Member.query.filter_by(username=username_receive).first():
            object = Member.query.filter_by(username=username_receive).first()
            object.image_url = request.form["image_url"]
            object.mbti = request.form["mbti"]
            object.collabo_style = request.form["collabo_style"]
            object.advantage = request.form["advantage"]
            object.blog_url = request.form["blog_url"]
        else:
            member = Member(
                username=username_receive,
                image_url=image_url_receive,
                mbti=mbti_receive,
                collabo_style=collabo_style_receive,
                advantage=advantage_receive,
                blog_url=blog_url_receive,
            )
            db.session.add(member)
        db.session.commit()

    return redirect(url_for("members"))


#details
@app.route("/members/<username>/details", methods=["GET"])
def member_details(username):
    member = Member.query.filter_by(username=username).first_or_404()
    return jsonify({
        "username": member.username,
        "image_url": member.image_url,
        "mbti": member.mbti,
        "collabo_style": member.collabo_style,
        "advantage": member.advantage,
        "blog_url": member.blog_url
    })

#delete
@app.route("/members/<username>/delete", methods=["POST"])
def member_delete(username):
    member = Member.query.filter_by(username=username).first()
    if member:
        db.session.delete(member)
        db.session.commit()
        return jsonify({"success": "Member deleted successfully"}), 200
    else:
        return jsonify({"error": "Member not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
