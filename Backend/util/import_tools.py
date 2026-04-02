import csv
import sys
from decimal import Decimal
from pathlib import Path

from sqlalchemy.orm import Session

from Backend.core.database import SessionLocal
from Backend.crud.tool.crud_tool import tool_crud
from Backend.model.tools.tools_model import Tool


VALID_CONDITIONS = {
    "Neu",
    "Minimal abgenutzt",
    "Gebraucht",
    "Gut abgenutzt",
    "Defekt",
}


def parse_decimal(value: str) -> Decimal:
    normalized = (value or "").strip().replace(",", ".")
    return Decimal(normalized)


def read_image_bytes(image_path: Path) -> bytes:
    if not image_path.exists():
        raise FileNotFoundError(f"Bild nicht gefunden: {image_path}")

    return image_path.read_bytes()


def import_tools(csv_path: Path, images_dir: Path, replace_existing: bool = False) -> int:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV nicht gefunden: {csv_path}")

    if not images_dir.exists():
        raise FileNotFoundError(f"Bilder-Ordner nicht gefunden: {images_dir}")

    imported_count = 0
    db: Session = SessionLocal()

    try:
        with csv_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
            reader = csv.DictReader(csv_file)

            required_columns = {
                "image_filename",
                "name",
                "description",
                "base_price",
                "tool_condition",
                "created_by",
            }

            missing_columns = required_columns.difference(reader.fieldnames or [])
            if missing_columns:
                raise ValueError(f"Fehlende CSV-Spalten: {', '.join(sorted(missing_columns))}")

            for line_number, row in enumerate(reader, start=2):
                image_filename = (row.get("image_filename") or "").strip()
                name = (row.get("name") or "").strip()
                description = (row.get("description") or "").strip()
                tool_condition = (row.get("tool_condition") or "").strip()
                created_by_raw = (row.get("created_by") or "").strip()

                if not image_filename or not name or not description or not created_by_raw:
                    raise ValueError(f"Zeile {line_number}: Pflichtfeld fehlt.")

                if tool_condition not in VALID_CONDITIONS:
                    raise ValueError(
                        f"Zeile {line_number}: Ungueltige Kondition '{tool_condition}'."
                    )

                base_price = parse_decimal(row.get("base_price") or "")
                created_by = int(created_by_raw)

                existing_tool = db.query(Tool).filter(
                    Tool.name == name,
                    Tool.created_by == created_by,
                    Tool.deleted == 0,
                ).first()

                if existing_tool and not replace_existing:
                    print(f"Uebersprungen: {name} (existiert bereits)")
                    continue

                raw_image_bytes = read_image_bytes(images_dir / image_filename)
                compressed_image_bytes = tool_crud.compress_image_bytes(raw_image_bytes)
                deposit = tool_crud.calculate_deposit(float(base_price), tool_condition)

                if existing_tool and replace_existing:
                    existing_tool.description = description
                    existing_tool.base_price = base_price
                    existing_tool.deposit = deposit
                    existing_tool.tool_condition = tool_condition
                    existing_tool.tool_image = compressed_image_bytes
                    db.add(existing_tool)
                else:
                    db.add(
                        Tool(
                            name=name,
                            description=description,
                            base_price=base_price,
                            deposit=deposit,
                            tool_condition=tool_condition,
                            tool_image=compressed_image_bytes,
                            created_by=created_by,
                        )
                    )

                imported_count += 1

        db.commit()
        return imported_count
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def main() -> int:
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("DB/init_tools.csv")
    images_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("DB/tool_images")
    replace_existing = "--replace" in sys.argv[3:]

    imported_count = import_tools(csv_path, images_dir, replace_existing=replace_existing)
    print(f"{imported_count} Tools importiert.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
