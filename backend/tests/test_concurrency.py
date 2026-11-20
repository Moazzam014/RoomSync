
from concurrent.futures import ThreadPoolExecutor
from threading import Event, Lock
import time

from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from app.engine import rotation_engine
from app.models import Room, Member, Task, Rotation


def test_simultaneous_assignment_creates_only_one_rotation(
    test_engine,
    monkeypatch,
):
    TestingSessionLocal = sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )

    # Create committed test records so both independent
    # database sessions can see them.
    setup_db = TestingSessionLocal()

    try:
        room = Room(
            name="Concurrency Test Room",
            description="Temporary concurrency test",
        )
        setup_db.add(room)
        setup_db.flush()

        member = Member(
            name="Concurrency Test Member",
            room_id=room.id,
            role="owner",
            is_active=True,
        )
        setup_db.add(member)
        setup_db.flush()

        task = Task(
            room_id=room.id,
            name="Concurrency Test Task",
            frequency="daily",
            is_active=True,
        )
        setup_db.add(task)
        setup_db.commit()

        room_id = room.id
        member_id = member.id
        task_id = task.id

    finally:
        setup_db.close()

    first_selection_started = Event()
    release_first_selection = Event()
    second_request_started = Event()

    counter_lock = Lock()
    selection_calls = 0

    def controlled_select_member(db, room_id, task_id):
        nonlocal selection_calls

        with counter_lock:
            selection_calls += 1
            current_call = selection_calls

        # Hold the first request after it has acquired
        # the task row lock.
        if current_call == 1:
            first_selection_started.set()

            if not release_first_selection.wait(timeout=10):
                raise TimeoutError(
                    "First assignment was not released."
                )

        return db.get(Member, member_id)

    monkeypatch.setattr(
        rotation_engine,
        "select_member",
        controlled_select_member,
    )

    def run_assignment():
        with TestingSessionLocal() as db:
            rotation = rotation_engine.assign_task(
                db=db,
                room_id=room_id,
                task_id=task_id,
            )

            return rotation.id if rotation else None

    try:
        with ThreadPoolExecutor(max_workers=2) as executor:
            first_future = executor.submit(run_assignment)

            assert first_selection_started.wait(timeout=5), (
                "First request did not reach member selection."
            )

            def second_request():
                second_request_started.set()
                return run_assignment()

            second_future = executor.submit(second_request)

            assert second_request_started.wait(timeout=5), (
                "Second request did not start."
            )

            # Give the second request time to reach the
            # database while the first transaction holds
            # the task row lock.
            time.sleep(0.25)

            release_first_selection.set()

            first_rotation_id = first_future.result(timeout=10)
            second_rotation_id = second_future.result(timeout=10)

        assert first_rotation_id is not None
        assert second_rotation_id is not None

        # Both requests must return the same rotation.
        assert first_rotation_id == second_rotation_id

        # Verify the committed database state.
        with TestingSessionLocal() as verify_db:
            incomplete_count = (
                verify_db.query(func.count(Rotation.id))
                .filter(
                    Rotation.room_id == room_id,
                    Rotation.task_id == task_id,
                    Rotation.is_completed.is_(False),
                )
                .scalar()
            )

            assert incomplete_count == 1

    finally:
        release_first_selection.set()

        # Remove only the temporary test room and its
        # related records.
        with TestingSessionLocal() as cleanup_db:
            temporary_room = cleanup_db.get(Room, room_id)

            if temporary_room:
                cleanup_db.delete(temporary_room)
                cleanup_db.commit()
