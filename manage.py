import subprocess
import fire
from typing import NoReturn


def migrate() -> NoReturn:
    """
    Executes Alembic's 'upgrade' command to migrate the database to the latest revision.
    """
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("Migration successful.")
    except subprocess.CalledProcessError as e:
        print(f"Migration failed with error: {e}")


def auto_migration() -> NoReturn:
    """
    Generates a new Alembic migration script automatically from the changes detected in the models.
    """
    try:
        subprocess.run(["alembic", "revision", "--autogenerate"], check=True)
        print("Automatic migration script generation successful.")
    except subprocess.CalledProcessError as e:
        print(f"Automatic migration script generation failed with error: {e}")


if __name__ == "__main__":
    fire.Fire({
        "migrate": migrate,
        "auto_migration": auto_migration,
    })
