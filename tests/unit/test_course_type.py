from app.models import CourseType

def test_create_course_type():
    """
    Test unitaire : création d'un objet CourseType
    Scénario :
        - Créer un objet CourseType avec des attributs valides
    Résultat attendu :
        - Les attributs sont bien initialisés
    """
    ct = CourseType(
        name="Pole Flow",
        description="Cours de fluidité et transitions",
        duration=60,
        credit=1,
        places=12
    )

    assert ct.name == "Pole Flow"
    assert ct.description == "Cours de fluidité et transitions"
    assert ct.duration == 60
    assert ct.credit == 1
    assert ct.places == 12
