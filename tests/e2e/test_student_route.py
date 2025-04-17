import pytest
from app.models import Student, Subscription
from datetime import datetime, timedelta


def test_add_student_end_to_end(client, session, login_as_admin):
    """
    Test end-to-end : Ajout d'un étudiant via POST /students/add
    """
    response = client.post("/students/add", data={
        "name": "Lucine Giraud",
        "email": "lucine@example.com",
        "credit_balance": 5
    }, follow_redirects=True)

    assert response.status_code == 200

    student = session.query(Student).filter_by(email="lucine@example.com").first()
    assert student is not None
    assert student.name == "Lucine Giraud"
    assert student.credit_balance == 5

def test_add_credits_end_to_end(client, session, login_as_admin):
    """
    Test end-to-end : Ajouter des crédits à un étudiant via POST /students/<id>/add_credits
    """
    student = Student(name="Lucine Giraud", email="lucine@example.com", credit_balance=5)
    session.add(student)
    session.commit()

    response = client.post(f"/students/{student.id}/add_credits", json={
        "amount": 10
    })

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {"success": True}

    updated_student = session.query(Student).filter_by(id=student.id).first()
    assert updated_student.credit_balance == 15


def test_add_subscription_end_to_end(client, session, login_as_admin):
    """
    Test end-to-end : Ajouter un abonnement à un étudiant via POST /students/<id>/add_subscription
    """
    # Créer un étudiant
    student = Student(name="Lucine Giraud", email="lucine@example.com")
    session.add(student)
    session.commit()

    # Préparer les données pour l'abonnement
    start_date = "2025-04-20"
    months = 3
    weekly_limit = 2

    response = client.post(f"/students/{student.id}/add_subscription", json={
        "start_date": start_date,
        "months": months,
        "weekly_limit": weekly_limit
    })

    # Vérifie que la requête a réussi
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {"success": True}

    # Vérifie que l'abonnement a bien été ajouté en BDD
    sub = session.query(Subscription).filter_by(student_id=student.id).first()
    assert sub is not None
    assert sub.start_date == datetime.strptime(start_date, "%Y-%m-%d")
    expected_end_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(weeks=months*4)
    assert sub.end_date == expected_end_date
    assert sub.weekly_limit == weekly_limit
