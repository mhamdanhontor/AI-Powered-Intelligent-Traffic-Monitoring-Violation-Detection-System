from fastapi import APIRouter

from app.database import SessionLocal
from app.models.violation_model import Violation

router = APIRouter(
    prefix="/api",
    tags=["Dashboard"],
)


@router.get("/health")
def health():

    return {
        "status": "ok"
    }


@router.get("/violations")
def get_violations():

    db = SessionLocal()

    try:

        violations = db.query(
            Violation
        ).all()

        return violations

    finally:

        db.close()


@router.get("/statistics")
def statistics():

    db = SessionLocal()

    try:

        violations = db.query(
            Violation
        ).all()

        overspeed = 0
        wrong_way = 0
        helmet = 0

        for v in violations:

            if v.violation_type == "overspeed":
                overspeed += 1

            elif v.violation_type == "wrong_way":
                wrong_way += 1

            elif v.violation_type == "no_helmet":
                helmet += 1

        return {

            "total": len(violations),

            "overspeed": overspeed,

            "wrong_way": wrong_way,

            "no_helmet": helmet,

        }

    finally:

        db.close()


@router.get("/vehicles")
def vehicles():

    db = SessionLocal()

    try:

        violations = db.query(
            Violation
        ).all()

        ids = []

        for violation in violations:

            if violation.track_id not in ids:

                ids.append(
                    violation.track_id
                )

        return {

            "vehicles": len(ids)

        }

    finally:

        db.close()