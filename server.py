from flask import Flask, render_template, redirect, url_for

from forms import TeamForm, ProjectForm

from model import db, connect_to_db, User, Team, Project

USER_ID = 1

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route("/")
def home():
    team_form = TeamForm()
    project_form = ProjectForm()
    project_form.update_teams(User.query.get(USER_ID).teams)
    return render_template("home.html", team_form=team_form, project_form=project_form)

@app.route("/add-new-team")
def add_new_team():
    team_form = TeamForm()
    return render_template("add-team.html", team_form=team_form)

@app.route("/add-team", methods=["GET", "POST"])
def add_team():
    team_form = TeamForm()

    if team_form.validate_on_submit():
        team_name = team_form.team_name.data

        new_team = Team(team_name, USER_ID)
        db.session.add(new_team)
        db.session.commit()
    return redirect(url_for("show_teams"))

@app.route("/add-new-project")
def add_new_project():
    project_form = ProjectForm()
    project_form.update_teams(User.query.get(USER_ID).teams)
    return render_template("add-project.html", project_form=project_form)

@app.route("/add-project", methods=["POST"])
def add_project():
    project_form = ProjectForm()
    project_form.update_teams(User.query.get(USER_ID).teams)

    if project_form.validate_on_submit():
        project_name = project_form.project_name.data
        description = project_form.description.data
        completed = project_form.completed.data
        team_selection = project_form.team_selection.data

        new_project = Project(project_name, description, completed, team_selection)
        db.session.add(new_project)
        db.session.commit()
    return redirect(url_for("show_projects"))

@app.route("/teams")
def show_teams():
    user = User.query.get(USER_ID)
    return render_template("teams.html", teams = user.teams)

@app.route("/projects")
def show_projects():
    user = User.query.get(USER_ID)
    projects = user.get_all_projects()
    return render_template("projects.html", projects = projects)


@app.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    project = Project.query.get(project_id)
    if project:
        db.session.delete(project)
        db.session.commit()
    return redirect(url_for("show_projects"))

@app.route('/delete_team/<int:team_id>', methods=['POST'])
def delete_team(team_id):
    team = Team.query.get(team_id)
    if team:
        db.session.delete(team)
        db.session.commit()
    return redirect(url_for("show_teams"))

if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True)